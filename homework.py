import os
import sys
import logging
import time
import requests
from http import HTTPStatus

from dotenv import load_dotenv
from telebot import TeleBot

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
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler) 

def check_tokens():
    """Проверка доступности переменных окружения."""
    if not TELEGRAM_TOKEN:
        logger.critical('Отсутствует переменная TELEGRAM_TOKEN.')
    if not TELEGRAM_CHAT_ID:
        logger.critical('Отсутствует переменная TELEGRAM_CHAT_ID.')
    if not PRACTICUM_TOKEN:
        logger.critical('Отсутствует переменная PRACTICUM_TOKEN.')
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправка сообщения в Telegram-чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.debug('Сообщение отправлено.')
    except Exception as error:
        logger.error(f'Ошибка при отправке сообщения: {error}.')


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except requests.exceptions.RequestException:
        logging.error('Ошибка эндпоинта.')
    finally:
        status = response.status_code
        if status != HTTPStatus.OK:
            raise AssertionError(response)
        else:
            return response.json()


def check_response(response):
    """Проверка ответа API на соответствие документации."""
    if not isinstance(response, dict):
        logger.error('В ответе API нет словаря.')
        raise TypeError('В ответе API нет словаря.')
    if 'homeworks' not in response:
        logger.error('Отсутствует ключ "homeworks".')
        raise KeyError
    if not isinstance(response['homeworks'], list):
        logger.error('В ответе API нет списка.')
        raise TypeError('В ответе API нет списка.')
    if 'current_date' not in response:
        logger.error('Отсутствует ключ "current_date".')
        raise KeyError('Отсутствует ключ "current_date".')
    return response


def parse_status(homework):
    """Извлекает статус конкретной домашней работы из ответа API."""
    if 'homework_name' not in homework:
        logger.error('В ответе API нет ключа "homework_name".')
        raise KeyError('В ответе API нет ключа "homework_name".')
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status not in HOMEWORK_VERDICTS:
        logger.error('Неожиданный статус домашней работы.')
        raise Exception('Неожиданный статус домашней работы.')
    verdict = HOMEWORK_VERDICTS.get(homework_status)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical(
            'Отсутствуют переменные окружения.'
            'Программа принудительно остановлена.'
            )
        sys.exit()
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())


    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                send_message(bot, message)
                logging.debug('Отправлено сообщение о новом статусе.')
            else:
                 logger.debug('Статусы работ не изменились.')
            timestamp = response.get('current_date')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(error)
            send_message(bot, message)
        finally:
             time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
