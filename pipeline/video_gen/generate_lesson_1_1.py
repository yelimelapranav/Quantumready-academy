from gradio_client import Client
import shutil
from pathlib import Path

client = Client("numanajmal0/wan-video-api")

prompt = """
A professional enterprise architect in a modern corporate strategy room,
studying a large technology architecture diagram displayed on a wall screen.
The diagram visually connects classical enterprise computing infrastructure
to a conceptual quantum computing service in the cloud.
The architect is carefully considering how quantum technology could fit into
existing enterprise systems.
Professional educational technology documentary style, realistic corporate
environment, clean composition, subtle cinematic lighting, slow deliberate
camera movement, natural human motion, stable scene, no logos, no readable text,
no exaggerated science-fiction effects.
"""

negative_prompt = """
low quality, blurry, distorted face, deformed hands, extra fingers,
duplicate person, unstable scene, excessive camera movement, flickering,
warped architecture diagram, readable text, subtitles, watermark, logo,
cartoon, anime, fantasy, science fiction spaceship
"""

print("Generating Lesson 1.1 visual with Wan 2.1 T2V 1.3B...")
print("This may take a few minutes.")

result = client.predict(
    model_key="wan-base",
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=832,
    height=480,
    num_frames=81,
    steps=30,
    guidance_scale=5.0,
    seed=42,
    lora_scale=1.0,
    custom_ckpt="",
    api_name="/generate"
)

video_path = result[0]
seed_used = result[1]

output_dir = Path("pipeline/video_gen/output")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "lesson_1_1_wan_scene_01.mp4"
shutil.copy2(video_path, output_file)

print("\n=== GENERATION COMPLETE ===")
print(f"Seed: {seed_used}")
print(f"Video: {output_file.resolve()}")
