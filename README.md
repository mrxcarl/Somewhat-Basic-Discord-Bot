# 🎮 Somewhat Basic Discord Bot - Command Reference & Setup Guide

Welcome to the official documentation for the **Somewhat Basic Discord Bot**!  
This bot includes a variety of utility, moderation, and entertainment commands designed to enhance your server experience.

---

## 🚀 Getting Started

### 🔧 Requirements

- **Python 3.10+**

### 📦 Installation

1. Clone this repository:

```bash
git clone https://github.com/mrxcarl/Somewhat-Basic-Discord-Bot.git
cd Somewhat-Basic-Discord-Bot
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain the following:

```
aiohttp==3.11.11
config==0.5.1
discord.py==2.5.2
gTTS==2.5.4
Pillow==11.2.1
psutil==7.0.0
Requests==2.32.4
yt_dlp==2025.6.9
```

3. Run the bot:

```bash
py bot.py
```

## 📜 Commands

## Help - Available Commands

### Commands (1)

## 🛠️ Help - Available Commands
Use the commands below to interact with the bot's various features.

| Command | Description |
| :--- | :--- |
| **!help** | Shows this message |
| **/8ball** | Ask the magic 8-ball a question |
| **/about** | Information about the bot and its creator |
| **/add** | Add a bet to your betslip. |
| **/alarm** | Set a reminder/alarm. |
| **/albums** | Select an album to view songs |
| **/announce** | Send an embedded announcement to the announcements channel (**Admin only**) |
| **/avatar** | Get a user's avatar |
| **/betleaderboard** | Top bettors by profit |
| **/betstats** | View your betting statistics |
| **/betwin** | Record a winning bet |
| **/botinfo** | Displays information about the bot. |
| **/clear** | Clear a specified number of messages |
| **/clearslip** | Clear your entire betslip. |
| **/coinflip** | Flips a coin |
| **/dinnerprep** | Start or stop dinner prep status |
| **/embed** | Send a fancy embedded message to this channel. |
| **/github** | View the bot's GitHub repository. |
| **/help** | Lists all available commands with their descriptions |
| **/imggen** | Generate an image using Stable Diffusion Forge |
| **/imitate** | Send a message that looks like it's from another user using a webhook. |
| **/invite** | Get an invite link to add the bot to your server. |
| **/lat** | Check bot latency and Ubisoft server latency |
| **/mdia** | Announces a new movie or TV series. |
| **/mlbbox** | Show today's box score for a given MLB team |
| **/mlbscore** | Show today's MLB scores |
| **/music** | Play music from YouTube |
| **/news** | Get the latest news headlines. |
| **/nickname** | Change the bot's nickname |
| **/nickother** | Change another member's nickname. |
| **/pause** | Pause music |
| **/pbl** | Play a YouTube video in a voice channel by link. |
| **/ping** | Checks the bot's latency |
| **/play** | Play a local MP3 file in a voice channel. |
| **/playgame** | Announce the game you're about to play. |
| **/pm** | Send a private message to a user |
| **/rehash** | Reload all command modules |
| **/resume** | Resume music |
| **/rps** | Challenge another user to Rock-Paper-Scissors! |
| **/rpsstats** | Check your Rock-Paper-Scissors stats. |
| **/say** | Make the bot say whatever you want. |
| **/setstatus** | Set the bot's status and activity. |
| **/showoff** | Show off your betslip to the current channel. |
| **/showslip** | Show your current betslip. |
| **/shutdown** | Shutdown the bot (**Admin only**) |
| **/slap** | Slap a user with a rotting trout! |
| **/smoke** | Start or stop a smoke break |
| **/split** | Upload a .txt file and split its contents into messages |
| **/stop** | Stop music |
| **/stop_music** | Stop music and leave the voice channel |
| **/suggest** | Submit a suggestion to the bot owner. |
| **/tts** | Converts text to speech and plays it in a voice channel. |
| **/urban** | Look up a word on Urban Dictionary. |
| **/userinfo** | Get information about a user. |
| **/weather** | Get current weather by ZIP code (AccuWeather) |
| **/win** | Mark one of your bets as won. |
| **/wpost** | Post a welcome message in the welcome/welcome-and-rules channel |

## 🤖 Hosting Tips

* Consider using a process manager like [PM2](https://pm2.keymetrics.io/) or a systemd service to keep the bot running 24/7.
* Make sure to **never expose your bot token** publicly.
* Use `.env` files or a `config.json` to manage sensitive info securely.

---

## 📬 Contact

### 👤 Created by [**Jason C. Klein** *(mrxcarl)*](https://github.com/mrxcarl)

Feel free to reach out with any **questions**, **bug reports**, or **feature suggestions** via [GitHub Issues](https://github.com/mrxcarl) or contact me directly:

* 🗨️ **Discord**: `@erendreich`
* 📧 **Email**: [jethro8740@gmail.com](mailto:jethro8740@gmail.com)

---

### 🚀 See the Bot in Action!

You’re welcome to join one of my servers to try the bot live! It uses **slash commands**, so simply type `/help` once you're in.

🔗 **Join here**: [https://discord.gg/WQZpcuHy9s](https://discord.gg/WQZpcuHy9s)

---

## 📝 License

This project is open source under the [MIT License](LICENSE).
