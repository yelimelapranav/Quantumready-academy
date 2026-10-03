from gradio_client import Client
import shutil
from pathlib import Path

client = Client("numanajmal0/wan-video-api")

prompt = """
A senior enterprise architect in a modern corporate technology office,
looking thoughtfully at a large wall display showing a complex enterprise
technology ecosystem: secure cloud infrastructure, interconnected business
systems, data flows, and a conceptual quantum computing service connected
to the architecture. The architect is evaluating security risks, technology
partners, and difficult business workloads that could benefit from new
computing technology. Professional enterprise architecture documentary,
realistic corporate environment, sophisticated but believable technology,
clean visual storytelling, slow subtle camera movement, stable composition,
natural human movement, no logos, no readable text, no science-fiction
fantasy, no holographic excess.
"""

negative_prompt = """
low quality, blurry, distorted face, deformed hands, extra fingers,
duplicate person, unstable scene, flickering, warped diagrams,
readable text, subtitles, watermark, logo, cartoon, anime,
fantasy, spaceship, futuristic city, excessive holograms,
rapid camera movement
"""

print("Generating Lesson 1.1 Scene 2 with Wan 2.1 T2V 1.3B...")
print("Please wait...")

result = client.predict(
    model_key="wan-base",
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=832,
    height=480,
    num_frames=81,
    steps=30,
    guidance_scale=5.0,
    seed=43,
    lora_scale=1.0,
    custom_ckpt="",
    api_name="/generate"
)

video_path = result[0]

output_dir = Path("pipeline/video_gen/output")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "lesson_1_1_wan_scene_02.mp4"
shutil.copy2(video_path, output_file)

print("\n=== SCENE 2 COMPLETE ===")
print(f"Video: {output_file.resolve()}")
