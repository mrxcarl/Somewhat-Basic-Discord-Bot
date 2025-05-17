# 🎮 Somewhat Basic Discord Bot - Command Reference & Setup Guide

Welcome to the official documentation for the **Discord Bot**!  
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
discord.py==2.4.0
gTTS==2.5.4
Pillow==11.2.1
psutil==6.1.1
Requests==2.32.3
yt_dlp==2025.4.30
```

3. Run the bot:

```bash
py bot.py
```

---

## 🛠️ Bot Commands

### 🎱 Fun & Utility

* `/8ball [question]` – Ask the magic 8-ball a question.
* `/avatar [user]` – Get a user's avatar.
* `/coinflip` – Flips a coin.
* `/ping` – Checks the bot's latency.
* `/say [message]` – Make the bot say whatever you want.
* `/slap [user]` – Slap a user with a rotting trout!
* `/tts [message]` – Converts text to speech and plays it in a voice channel.

### 👤 User & Bot Info

* `/about` – Information about the bot and its creator.
* `/botinfo` – Displays information about the bot.
* `/userinfo [user]` – Get information about a user.
* `/invite` – Get an invite link to add the bot to your server.

### 🧹 Moderation

* `/announce [message]` – Send an embedded announcement to the announcements channel. *(Admin only)*
* `/clear [amount]` – Clear a specified number of messages. *(Requires proper permissions)*
* `/nickname [name]` – Change the bot's nickname.
* `/shutdown` – Shutdown the bot. *(Admin only)*
* `/rehash` – Reload all command modules. *(Developer/Owner only)*

### 🎵 Music

* `/music [song name]` – Play any song by any artist from YouTube in a voice channel.
* `/play` – Play a local MP3 file in a voice channel.
* `/stop` – Stops the music and disconnects the bot from the voice channel.

### ✉️ Messaging

* `/pm [user] [message]` – Send a private message to a user.
* `/suggest [message]` – Submit a suggestion to the bot owner.

### 🆘 Help

* `/help` – Lists all available commands with their descriptions.

---

## 🤖 Hosting Tips

* Consider using a process manager like [PM2](https://pm2.keymetrics.io/) or a systemd service to keep the bot running 24/7.
* Make sure to **never expose your bot token** publicly.
* Use `.env` files or a `config.json` to manage sensitive info securely.

---

## 📬 Contact

Created by **\[Jason C. Klein (mrxcarl)]**
Feel free to reach out with questions, bugs, or suggestions via GitHub Issues or Discord.

---

## 📝 License

This project is open source under the [MIT License](LICENSE).
