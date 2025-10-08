# utils.py
import torch

def build_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Fixed vocab size = 256
    vocab_size = 256

    # byte-level encoding
    encode = lambda s: list(s.encode("utf-8"))
    decode = lambda l: bytes(l).decode("utf-8", errors="ignore")

    data = torch.tensor(encode(text), dtype=torch.long)

    # 90% train, 10% val
    n = int(0.9 * len(data))
    train_data = data[:n]
    val_data = data[n:]

    return train_data, val_data, vocab_size, encode, decode

def get_batch(data, block_size, batch_size=32):
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y
