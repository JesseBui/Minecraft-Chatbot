local URL = "wss://cinema-descriptions-navigate-lesser.trycloudflare.com"

settings.load()

local TOKEN = settings.get("TOKEN")
if not TOKEN then
    error("No token configured. Run setup.lua first.")
end

local ws = nil
local box = nil

local function setupChatBox()
    box = peripheral.find("chat_box")

    if not box then 
        error("Chatbox not found", 0)
    end
    
    if box.peripheralDisabled then 
        error("Peripheral is Disabled", 0)  
    end

    print("chat box is ready")
end

local function connectWebSocket()
    print("Connecting...")

    local socket, err = http.websocket(URL)

    if not socket then
        error("Websocket connection failed:" .. tostring(err), 0)
    end

    ws = socket
    
    print ("connected")
end

local function authenticate()
    print("Checking...")

    ws.send(TOKEN)

    local response = ws.receive(5)

    if response ~= "AUTH_OK" then
        ws.close()
        error("Authenticating failed, check your token again", 0)
    end

    print("Welcome to Bp brother")
end


-- minecraft -> python
local function listenToMinecraft()

    while true do 
        local event,uuid,username,message,hidden = os.pullEvent("chat")

        print(username .. ": " .. message)

        ws.send(username .. ": " .. message)
    end
end

-- python -> minecraft
local function listenToPython()
    
    while true do
        local message, reason = ws.receive()
    
        --check if received message or websocket disconnect
        if not message then
            print("Websocket disconnected: " .. tostring(reason))
            return
        end

        print("Python:" .. message)


        --Name your bot whatever name you want here
        local ok, err = box.sendMessage(message,{
            prefix = "Verity" 
        })

        if not ok then 
            print("Chatbox error: " .. tostring(err))
        end
    end
end



local function main()
    setupChatBox()
    connectWebSocket()
    authenticate()

    parallel.waitForAny(
        listenToPython,
        listenToMinecraft
    )

    ws.close()

end

main()
