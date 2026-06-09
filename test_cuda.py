import torch
print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM total:", torch.cuda.get_device_properties(0).total_memory // 1024**2, "MB")
    # Try a small tensor allocation
    x = torch.zeros(1, device='cuda')
    print("CUDA tensor OK:", x)
