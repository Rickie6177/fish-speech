import torch, sys
sys.path.insert(0, '/app')

print("Free VRAM before:", torch.cuda.mem_get_info()[0] // 1024**2, "MB")

from fish_speech.models.text2semantic.inference import launch_thread_safe_queue
llama_queue = launch_thread_safe_queue(
    checkpoint_path='checkpoints/s2-pro',
    device='cuda',
    precision=torch.half,
    compile=False,
)
torch.cuda.synchronize()
free, total = torch.cuda.mem_get_info()
used = (total - free) // 1024**2
print(f"After LLAMA: {used} MB used / {total//1024**2} MB total, {free//1024**2} MB free")
