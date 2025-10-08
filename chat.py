import torch
from func import PicoGPT
from utils import build_dataset

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load dataset vocab
_, _, vocab_size, encode, decode = build_dataset("data/dataset.txt")

# Load trained model
model = PicoGPT(vocab_size=vocab_size, emb_dim=128, n_heads=4, n_layers=2, block_size=64).to(device)
checkpoint = torch.load("data/picoGPT.pt", map_location=device)
model.load_state_dict(checkpoint["model_state"]) 
model.eval()

print("Chatbot ready!")
history = "The following is a conversation:\n"

while True:
    user = input("You: ")

    history += f"You: {user}\nBot:"
    context = torch.tensor([encode(history)], dtype=torch.long, device=device)

    out = model.generate(context, max_new_tokens=100)[0].tolist()
    response = decode(out)[len(history):].split("\n")[0]  # first line
    print("Bot:", response.strip())

    history += response + "\n"
