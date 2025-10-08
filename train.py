import torch
import torch.nn.functional as F
from torch import optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from func import PicoGPT
from utils import build_dataset, get_batch
import os
import json, time

record_file = "data/record.json"

def load_record():
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            return json.load(f)
    else:
        return {"steps_trained": 0, "total_time_sec": 0, "loss": 5}

def save_record(step, start_time, loss, prev_record):
    elapsed = time.time() - start_time
    total_time = prev_record["total_time_sec"] + elapsed
    record = {
        "steps_trained": prev_record["steps_trained"] + step,
        "total_time_sec": total_time,
        "loss": loss,
    }
    with open(record_file, "w") as f:
        json.dump(record, f, indent=4)
    return record

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load data
train_data, val_data, vocab_size, encode, decode = build_dataset("data/dataset.txt")

# Create model
model = PicoGPT(vocab_size=vocab_size, emb_dim=128, n_heads=4, n_layers=2, block_size=64).to(device)

# --- Load checkpoint if it exists ---
optimizer = optim.AdamW(model.parameters(), lr=1e-4)
checkpoint_loaded = False

if os.path.exists("data/picoGPT.pt"):
    print("Loading checkpoint...")
    checkpoint = torch.load("data/picoGPT.pt", map_location=device)
    if isinstance(checkpoint, dict) and "model_state" in checkpoint:
        model.load_state_dict(checkpoint["model_state"])
        checkpoint_loaded = True
    else:
        model.load_state_dict(checkpoint)
        print("Loaded model weights only (no optimizer state).")
    print("Checkpoint loaded!")

# LR scheduler (will activate later)
scheduler = ReduceLROnPlateau(
    optimizer,
    mode='min',
    factor=0.5,
    patience=800,
    threshold=1e-4,
    cooldown=100,
    min_lr=5e-6
)

step = 1
start_time = time.time()
record = load_record()
max_loss = record['loss']

# Delay scheduler for a few thousand steps
SCHEDULER_START = 2000

while True:
    xb, yb = get_batch(train_data, model.block_size)
    xb, yb = xb.to(device), yb.to(device)

    logits = model(xb)
    loss = F.cross_entropy(logits.view(-1, vocab_size), yb.view(-1))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Activate scheduler only after warm-up phase
    if step > SCHEDULER_START:
        scheduler.step(loss)
    
    print(f"Step {record['steps_trained'] + step} | Loss {loss.item():.4f}")

    # Save on improvement
    if loss.item() < max_loss:
        max_loss = loss.item()
        record = save_record(step, start_time, max_loss, record)
        start_time = time.time()
        torch.save({
            "model_state": model.state_dict(),
            "optim_state": optimizer.state_dict()
        }, "data/picoGPT.pt")

    step += 1
