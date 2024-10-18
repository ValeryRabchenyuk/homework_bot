import os
import logging
from logging.handlers import StreamHandler


from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )

logger = logging.getLogger(__name__)
handler = StreamHandler()
logger.addHandler(handler) 

def check_tokens():
    """Проверяет доступность переменных окружения, необходимых для работы."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """
    Отправка сообщения в Telegram-чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса TeleBot и строку с текстом сообщения.
    """
    ...


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса. В случае успешного запроса должна вернуть ответ API, приведя его из формата JSON к типам данных Python."""
    ...


def check_response(response):
    """Проверка ответа API на соответствие документации из урока «API сервиса Практикум Домашка».
    В качестве параметра функция получает ответ API, приведённый к типам данных Python."""
    ...


def parse_status(homework):
    """извлекает из информации о конкретной домашней работе статус этой работы. 
    В качестве параметра функция получает только один элемент из списка домашних работ. 
    В случае успеха функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_VERDICTS."""
    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""

    ...

    # Создаем объект класса бота
    bot = ...
    timestamp = int(time.time())

    ...

    while True:
        try:

            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
        ...


if __name__ == '__main__':
    main()
