import os
import telebot
import yt_dlp
import subprocess
import uuid

BOT_TOKEN = os.getenv("BOT_TOKEN") or "🔐YOUR_BOT_TOKEN🔐"
bot = telebot.TeleBot(BOT_TOKEN)

# ✨ /song command handler
@bot.message_handler(commands=['song'])
def download_song(message):
    try:
        url = message.text.split()[1]
        msg = bot.reply_to(message, f"🎶 Downloading your song...\n🔗 `{url}`\n⏳ Please wait...", parse_mode="Markdown")

        # Unique filename
        file_id = str(uuid.uuid4())
        output_path = f"{file_id}.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{file_id}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        filename = f"{file_id}.mp3"
        if os.path.exists(filename):
            bot.send_audio(message.chat.id, open(filename, 'rb'), caption="✅ *Song Downloaded Successfully!* 🎧", parse_mode="Markdown")
            os.remove(filename)
        else:
            bot.send_message(message.chat.id, "❌ Failed to download song.")

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"❌ *Error:*\n`{str(e)}`", parse_mode="Markdown")

# ✨ Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎵 *Welcome to FAST Song Downloader Bot!*\n\nSend:\n`/song <YouTube URL>` to get MP3 audio 🎧", parse_mode="Markdown")

# 🚀 Start bot
print("🤖 FAST Song Bot is running...")
bot.infinity_polling()
