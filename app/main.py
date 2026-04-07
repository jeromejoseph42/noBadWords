from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np

app = FastAPI()

@app.websocket("/ws/audio")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
            print(f"Received {len(audio_array)} samples")

            await websocket.send_text("OK")

    except WebSocketDisconnect:
        print("Client disconnected cleanly")

    except Exception as e:
        print("Unexpected error:", e)