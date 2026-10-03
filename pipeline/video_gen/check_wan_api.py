from gradio_client import Client

SPACE = "numanajmal0/wan-video-api"

print(f"Connecting to {SPACE}...")
client = Client(SPACE)

print("\n=== AVAILABLE WAN API ===")
client.view_api()
