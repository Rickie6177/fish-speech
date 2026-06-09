import torch
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    t = torch.zeros(1, device="cuda")
    print("Tensor on GPU OK")
    print("VRAM allocated:", round(torch.cuda.memory_allocated()/1024**2), "MB")
else:
    print("NO CUDA!")
