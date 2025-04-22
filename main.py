import asyncio
import websockets
import warnings
from main_agent import ReActAgent

warnings.filterwarnings("ignore", message="The function `loads` is in beta")

# Introductory message
print("Welcome to our medical assistant.😊")

# Define the WebSocket handler
async def websocket_handler(websocket, path):
    print("Client connected")
    medical_assistant = ReActAgent(verbose=True)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            response = medical_assistant(message)
            await websocket.send(response)
            print(f"Sent response: {response}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")

# Run the WebSocket server
async def main():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8000)
    print("WebSocket server started on port 8000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
