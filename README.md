This Telegram bot connects users to your AI service.

📋 Requirements

Python 3.8 or higher

Telegram bot token (from @BotFather)

The address/IP of your AI service

🚀 Installation & Setup
1. Install Dependencies
pip install -r requirements.txt
2. Configure Token & IP

Open the file telegram_ai_bot.py and find this section:

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# IP or URL of your AI service
AI_SERVICE_IP = "YOUR_AI_SERVICE_IP_HERE"
Replace the values with your own:

TELEGRAM_BOT_TOKEN: Obtain your bot token from @BotFather

AI_SERVICE_IP: Enter the IP or URL of your AI backend

Examples:

TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
AI_SERVICE_IP = "http://192.168.1.100:8000"  # with http://
# or
AI_SERVICE_IP = "192.168.1.100:8000"  # without http:// (auto-detected)
# or
AI_SERVICE_IP = "https://api.myai.com"  # with https://

3. Run the Bot
python telegram_ai_bot.py

🔧 Additional Configuration
Change the Endpoint

If your AI service uses a different endpoint, update this line:

AI_ENDPOINT = "/chat"  # change to your endpoint

Request/Response Format

If your AI service uses a custom request/response format, edit the call_ai_service function accordingly.

Default request format:

{
  "message": "User message text"
}


Accepted response formats:
Your service may return any of the following:

{"response": "text"}

{"reply": "text"}

{"text": "text"}

{"answer": "text"}

Or a direct string: "text"

📱 How to Use

Find your bot on Telegram (using the username from BotFather)

Send the /start command

Send any message — the bot will forward it to your AI service and return the response

⚠️ Troubleshooting
Connection Error

If you see:

❌ Cannot connect to the AI service


Check the following:

Make sure the IP/URL is correct

Ensure your AI service is running

Check that the firewall allows access

Token Error

If you receive a token error:

Verify that your bot token is correct

You can generate a new token via @BotFather

📝 Full Example
TELEGRAM_BOT_TOKEN = "123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
AI_SERVICE_IP = "http://localhost:8000"
AI_ENDPOINT = "/api/chat"

🔒 Security Notice

⚠️ Warning: This file contains sensitive tokens.
Do NOT commit your token to Git or expose it publicly.

💡 Notes

The bot works in real-time using long polling

Long responses (over 4096 characters) are automatically split

Request timeout is set to 30 seconds

📞 Support

If you run into issues, check:

Console logs

Token and IP configuration

Internet connection and AI service availability
