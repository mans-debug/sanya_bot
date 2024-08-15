import telebot, io
from PyPDF2 import PdfReader

from utill import compare

# Токен вашего бота, который вы получили от @BotFather
API_TOKEN = '7463369543:AAF90Ol-BYuSqV0V3F0xemdosgGAYobf4K8'

# Создаем объект бота
bot = telebot.TeleBot(API_TOKEN)


# Обработчик для команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне PDF файл, и я проверю его метаданные.")


# Обработчик для получения PDF файла
@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        # Проверяем, что это PDF файл
        if message.document.mime_type != 'application/pdf':
            bot.reply_to(message, "Пожалуйста, отправьте PDF файл.")
            return

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with io.BytesIO(downloaded_file) as file:
            pdf_file = PdfReader(file)
            pdf_metadata = pdf_file.metadata
            version = pdf_file.pdf_header

        data = {
            "size": len(downloaded_file) // 1024,
            "ver": version[5:8],
            "creator": pdf_metadata.creator,
            "producer": pdf_metadata.producer,
            "creation_date": pdf_metadata.creation_date
        }
        compare_result = compare(data)

        bot.reply_to(message, form_pdf_response(compare_result, data))
    except Exception as e:
        print(e)
        bot.reply_to(message, f"Произошла ошибка: {str(e)}.\n Возможно, файл фейк.❌")


def form_pdf_response(compare_result, data):
    return (
        f"Результаты проверки файла:\n\n"
        f"🔸 Размер файла (КБ):  {data.get('size')}\n"
        f"🔸 Версия PDF: {data.get('ver')}\n"
        f"🔸 Создатель: {data.get('creator')}\n"
        f"🔸 Дата создания: {data.get('creation_date')}\n"
        f"🔸 Производитель: {data.get('producer')}\n\n"
        f"Сравнение с шаблонами:\n\n"
        f"{compare_result}"
    )


bot.polling()
