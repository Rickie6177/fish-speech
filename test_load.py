import torch
import sys
sys.path.insert(0, '/app')

print("Torch:", torch.__version__)
print("CUDA:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM free:", torch.cuda.mem_get_info()[0] // 1024**3, "GB")

print("\nLoading LLAMA model...")
from fish_speech.models.text2semantic.inference import launch_thread_safe_queue
import torch

llama_queue = launch_thread_safe_queue(
    checkpoint_path='checkpoints/s2-pro',
    device='cuda',
    precision=torch.half,
    compile=False,
)
print("LLAMA loaded!")
print("VRAM after llama:", (torch.cuda.mem_get_info()[1] - torch.cuda.mem_get_info()[0]) // 1024**3, "GB used")

print("\nLoading decoder model...")
from fish_speech.models.dac.inference import load_model as load_decoder_model
decoder = load_decoder_model(
    config_name='modded_dac_vq',
    checkpoint_path='checkpoints/s2-pro/codec.pth',
    device='cuda',
)
print("Decoder loaded!")
print("VRAM after decoder:", (torch.cuda.mem_get_info()[1] - torch.cuda.mem_get_info()[0]) // 1024**3, "GB used")
