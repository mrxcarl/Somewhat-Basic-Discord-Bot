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

## 📜 Commands

### 🎮 General

| Command     | Description                                           |
| ----------- | ----------------------------------------------------- |
| `/8ball`    | Ask the magic 8-ball a question.                      |
| `/about`    | Information about the bot and its creator.            |
| `/avatar`   | Get a user's avatar.                                  |
| `/botinfo`  | Displays information about the bot.                   |
| `/coinflip` | Flips a coin.                                         |
| `/github`   | View the bot's GitHub repository.                     |
| `/help`     | Lists all available commands with their descriptions. |
| `/invite`   | Get an invite link to add the bot to your server.     |
| `/ping`     | Checks the bot's latency.                             |
| `/say`      | Make the bot say whatever you want.                   |
| `/slap`     | Slap a user with a rotting trout!                     |
| `/urban`    | Look up a word on Urban Dictionary.                   |
| `/userinfo` | Get information about a user.                         |

### 🧹 Moderation

| Command      | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| `/announce`  | Send an embedded announcement to the announcements channel. *(Admin only)* |
| `/clear`     | Clear a specified number of messages.                                      |
| `/nickname`  | Change the bot's nickname.                                                 |
| `/nickother` | Change another member's nickname.                                          |
| `/rehash`    | Reload all command modules.                                                |
| `/shutdown`  | Shutdown the bot. *(Admin only)*                                           |

### 🎵 Music

| Command  | Description                                                                     |
| -------- | ------------------------------------------------------------------------------- |
| `/music` | Search YouTube by artist and title, and play the top result in a voice channel. |
| `/pbl`   | Play a YouTube video in a voice channel by link.                                |
| `/play`  | Play a local MP3 file in a voice channel.                                       |
| `/stop`  | Stops the music and disconnects the bot from the voice channel.                 |
| `/tts`   | Converts text to speech and plays it in a voice channel.                        |

### 💬 Communication & Embeds

| Command    | Description                                                            |
| ---------- | ---------------------------------------------------------------------- |
| `/embed`   | Send a fancy embedded message to this channel.                         |
| `/imitate` | Send a message that looks like it's from another user using a webhook. |
| `/pm`      | Send a private message to a user.                                      |
| `/wpost`   | Post a welcome message in the welcome/welcome-and-rules channel.       |

### 🕹️ Gaming

| Command     | Description                             |
| ----------- | --------------------------------------- |
| `/playgame` | Announce the game you're about to play. |
| `/smoke`    | Start or stop a smoke break.            |

### 📈 Sports Betting

| Command      | Description                                   |
| ------------ | --------------------------------------------- |
| `/add`       | Add a bet to your betslip.                    |
| `/clearslip` | Clear your entire betslip.                    |
| `/showoff`   | Show off your betslip to the current channel. |
| `/showslip`  | Show your current betslip.                    |
| `/suggest`   | Submit a suggestion to the bot owner.         |



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
