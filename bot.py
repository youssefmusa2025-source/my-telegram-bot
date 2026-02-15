import telebot
import requests
import time

BOT_TOKEN = "7950652552:AAFB2HBT2nQ47iOq9YwZMgnTvomeE7_tXFA"
REMOVE_BG_API = "yRw82RZfmdmDPWeLCEyPAU6t"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['photo'])
def remove_background(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("input.png", "wb") as f:
            f.write(downloaded_file)

        with open("input.png", "rb") as img_file:
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": img_file},
                data={"size": "auto"},
                headers={"X-Api-Key": REMOVE_BG_API},
            )

        if response.status_code == 200:
            with open("output.png", "wb") as out:
                out.write(response.content)

            with open("output.png", "rb") as result:
                bot.send_photo(message.chat.id, result)
        else:
            bot.reply_to(message, f"حدث خطأ ❌\n{response.status_code}: {response.text}")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء المعالجة ❌\n{e}")

# تشغيل البوت بدون توقف
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
