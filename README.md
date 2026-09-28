# AI

Chatbot built by using CC, Advance Peripherals, and Python. Go crazy with it, make Verity or something.

Minecraft chat messages are captured by Lua, sent to the Python backend through a WebSocket connection, forwarded to DeepSeek, and then sent back into Minecraft through an Advanced Peripherals Chat Box.

## Requirements

### Minecraft

- Minecraft with CC
- Advanced Peripherals
- A Computer or Advanced Computer
- Advanced Peripherals Chat Box
- HTTP/WebSocket access enabled in CC

### Backend

- Python 3.10+
- DeepSeek API key
- `websockets`
- `python-dotenv`
- `openai`

Install the Python dependencies with:

```bash
pip install websockets python-dotenv openai
```

Alternatively:

```bash
pip install -r requirements.txt
```

## Backend Setup

Navigate to the `backend` folder.

Create a `.env` file:

```env
TOKEN=your_minecraft_authentication_token
DEEPSEEK_API_KEY=your_deepseek_api_key
```

`TOKEN` is used to authenticate the Minecraft Lua client with your Python backend.

`DEEPSEEK_API_KEY` is only used by the Python backend to communicate with DeepSeek.

## Create `prompt.txt`

Inside the `backend` folder, manually create:

```text
prompt.txt
```

Your folder should look like:

```text
backend/
├── server.py
├── prompt.txt
├── .env
└── requirements.txt
```

Put system prompt inside `prompt.txt`.

## Minecraft Authentication Token

The Minecraft authentication token should not be hardcoded inside `main.lua`.

Instead, use CC's local settings system.

Run `setup.lua` once and enter the same `TOKEN` that you placed inside the backend `.env` file.

CC stores this locally in `.settings`.

## WebSocket URL

Inside the Minecraft Lua client, configure the WebSocket URL:

```lua
local URL = "wss://your-domain.example.com"
```

If the Python backend is running locally behind a Cloudflare Tunnel, use the HTTPS/WSS address provided by Cloudflare.

For local testing, the Python backend may run on:

```text
ws://127.0.0.1:8765
```

However, Minecraft running on another machine will not be able to connect to your computer using `127.0.0.1`.

## Starting the Backend

From the `backend` folder:

```bash
python server.py
```

You should see something similar to:

```text
Vindeus server running on ws://127.0.0.1:8765
```

When Minecraft connects:

```text
Client connected, waiting for token...
Client authenticated!
```

## Future Ideas

idk will add along the way

## FAQ

### Why not call deepseek directly from lua?

Honestly, my original idea was to build an application that could communicate between Discord to Minecraft, but my friend suggest that I should build verity in minecraft instead so here we are. Plus it's probably a lot safer storing your API keys in a .env file instead of directly on the minecraft server anyway.

### Why deepseek ?

Cuz it's cheap.

### Does it remember conversation ?

Yes, if you keep the python backend running.

### You already know there's a gazillion other project with the same idea right ?

shut up
