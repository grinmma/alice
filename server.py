import logging
from telegram.ext import Application, MessageHandler, filters
from config import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение '
                                    f'{update.message.text}')


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, echo))
    logger.info('Бот работает')
    app.run_polling()

main()
