from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
import asyncio

app = FastAPI()

@app.websocket("/ws/audio")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    # FIX: periodic ping to keep the connection alive through Docker's network
    async def keepalive():
        while True:
            await asyncio.sleep(20)
            await websocket.send_text("ping")

    keepalive_task = asyncio.create_task(keepalive())

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

    finally:
        keepalive_task.cancel()