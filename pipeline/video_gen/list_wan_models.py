from gradio_client import Client

client = Client("numanajmal0/wan-video-api")

print("Checking available Wan models...")
result = client.predict(api_name="/list_models")

print("\n=== AVAILABLE MODELS ===")
print(result)
