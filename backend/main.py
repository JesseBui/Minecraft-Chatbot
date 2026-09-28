import asyncio
import hmac
import websockets
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

HOST = "127.0.0.1"
PORT = 8765


with open("prompt.txt", "r", encoding="utf-8") as file:
    PROMPT = file.read()

load_dotenv()

TOKEN = os.getenv("TOKEN")
AI_API_KEY= os.getenv("AI_API_KEY")

if not TOKEN:
    raise ValueError("TOKEN is missing from .env")

if not AI_API_KEY:
    raise ValueError("AI_API_KEY is missing from .env")

deepseek = AsyncOpenAI(
    api_key=AI_API_KEY,
    base_url="https://api.deepseek.com"
)

conversation = {
    "minecraft"[
        {
            "role":"system",
            "content": PROMPT
        }
    ]
}
async def ai(message):
    history = conversation["minecraft"]

    history.append({
        "role": "user",
        "content": message
    })

    try:
        response = await deepseek.chat.completions.create(
            model="deepseek-flash",
            messages=history
        )

        reply = response.choices[0].message.content

        history.append({
            "role":"assistant",
            "content": reply
        })

    except Exception:
        #delete user message if failed to reach deepseek
        history.pop()
        raise
    

async def handler(ws):
    print("Client connected, waiting for token...")

    try:
        # First message MUST be the token
        received_token = await asyncio.wait_for(ws.recv(), timeout=5)

        if not hmac.compare_digest(received_token, TOKEN):
            print("Invalid token!")
            await ws.close(
                code=4001, 
                reason="Unauthorized")
            
            return

        print("Client authenticated!")
        await ws.send("AUTH_OK")

        async for message in ws:
            print(f"\nMinecraft: {message}")

            try:
                reply = await ai(message)
                print (f"AI: {reply}")

                await ws.send(reply)
            
            except Exception as e:
                print (f"Deepseek error: {e}")

                await ws.send(
                    "ERROR ERROR ERROR"
                    "YOUR MESSAGE HAVE BEEN FLAGGED BY THE GOVERNMENT, AWAIT EXECUTION"
                )

    except asyncio.TimeoutError:
        print("Client did not authenticate in time.")
        await ws.close()

    except websockets.exceptions.ConnectionClosed:
        print("\nClient disconnected.")


async def main():
    async with websockets.serve(handler, 
                                HOST,
                                PORT):
        print(f"Server running on ws://{HOST}:{PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())