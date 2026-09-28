print("Enter client token:")
local TOKEN = read()

settings.set("TOKEN", TOKEN)
settings.save()

print("Token saved.")