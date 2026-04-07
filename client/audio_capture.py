import asyncio
import websockets
import sounddevice as sd

uri = "ws://localhost:8000/ws/audio"

async def stream_audio():
    async with websockets.connect(uri) as websocket:
        print("Connected to server")

        queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        # AUDIO CALLBACK (REAL-TIME SAFE)
        def callback(indata, frames, time, status):
            if status:
                print(status)
            loop.call_soon_threadsafe(queue.put_nowait, indata.tobytes())

        # ASYNC SENDER TASK
        async def sender():
            while True:
                data = await queue.get()
                await websocket.send(data)

        # Start audio stream
        with sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype="int16",
            blocksize=1024,  #  Important
            callback=callback,
        ):
            print("Streaming audio...")
            await sender()

if __name__ == "__main__":
    try:
        asyncio.run(stream_audio())
    except KeyboardInterrupt:
        print("Stopped")