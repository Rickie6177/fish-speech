import torch
total = torch.cuda.get_device_properties(0).total_memory
alloc = torch.cuda.memory_allocated()
resv = torch.cuda.memory_reserved()
free = total - resv
print(f'GPU total: {total / 1024**3:.2f} GB')
print(f'GPU allocated (model weights): {alloc / 1024**3:.2f} GB')
print(f'GPU reserved (PyTorch cache): {resv / 1024**3:.2f} GB')
print(f'GPU free for KV cache + compute: {free / 1024**3:.2f} GB')
