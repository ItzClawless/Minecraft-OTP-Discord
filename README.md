# Minecraft-OTP-Discord
SPOILER: I only fixed up the code and it's not mine.

# Disclaimer
he materials, guides, tutorials, and content shared here are intended strictly for educational, instructional, and informational purposes only. They are designed to help users learn, practice, or understand certain concepts, techniques, or tools. Under no circumstances should any content be used for illegal, unethical, harmful, or unauthorized activities.

The creator, platform, and contributors assume no responsibility or liability for any misuse, damages, losses, or legal consequences resulting from actions taken based on the information provided. Users are fully responsible for ensuring their actions comply with all applicable laws, regulations, and terms of service of any relevant platforms or services.

By accessing or using this content, you explicitly acknowledge and agree that it is your responsibility to act responsibly, ethically, and legally at all times.

# What does this code do?

First of all this code isn't mine, it's BackAgainSpin main code yet it was broken enough so i fixed it, This project demonstrates how Discord bots can be used to simulate social engineering techniques, such as impersonating account verification flows for platforms like Minecraft. It is designed to help developers, educators, and security professionals understand and visualize how deceptive user interfaces might trick users into sharing account information.

The bot can be configured to request a Minecraft username and email under the guise of "verification." It then simulates a login prompt through Microsoft’s authentication interface, showing how attackers might attempt to exploit trust and trick users into sharing login codes.

This simulation can be used in closed environments for security awareness training or ethical testing. No real account credentials should be collected or misused.

# How to use it

1. **Download Python** [Python](https://www.python.org/downloads/release/python-3110/)

2. **Create a Discord Bot**
 - When you create it make sure to grant it all intents and to put the bot token in `config.py `
 
3. **Get a MailSlurp API-Key**
  - [Here](https://www.mailslurp.com/) and put it in `config.py`
  
4. **OPTIONAL: Get Hypixel API for stats**
  - Visit [Hypixel Dashboard](https://developer.hypixel.net/) and register.

5. **Configuration of the code**
 - Open `bot.py` and put put your Discord ID in `self.admins = [YOUR DISCORD ID]`
 - Add the bot to the discord server
 - Open Command Prompt in your coding editor and write `pip install -r requirements.txt`
 - Run the Bot using python bot.py

# Use the bot

**To use the bot use type `/webhook` and then Set it up.**




