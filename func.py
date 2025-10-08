import torch
import torch.nn as nn
import torch.nn.functional as F

class PicoGPT(nn.Module):
    def __init__(self, vocab_size, emb_dim=128, n_heads=4, n_layers=2, block_size=64):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, emb_dim)
        self.pos_embedding = nn.Embedding(block_size, emb_dim)

        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=emb_dim, nhead=n_heads, dim_feedforward=4*emb_dim)
            for _ in range(n_layers)
        ])

        self.ln_f = nn.LayerNorm(emb_dim)
        self.head = nn.Linear(emb_dim, vocab_size)

        self.block_size = block_size

    def forward(self, idx):
        B, T = idx.shape
        assert T <= self.block_size, "Sequence too long!"

        tok_emb = self.token_embedding(idx)      # (B,T,emb_dim)
        pos_emb = self.pos_embedding(torch.arange(T, device=idx.device)) # (T,emb_dim)
        x = tok_emb + pos_emb

        for layer in self.layers:
            x = layer(x)

        x = self.ln_f(x)
        logits = self.head(x)   # (B,T,vocab_size)
        return logits

    @torch.no_grad()
    def generate(self, idx, max_new_tokens=50):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]
            logits = self(idx_cond)
            logits = logits[:, -1, :]   # last token
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_token), dim=1)
        return idx
