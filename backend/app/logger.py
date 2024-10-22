import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from backend.app.config import settings

logger = logging.getLogger()

# устанавливаем хендлеры - это то, куда будет писаться лог
# пишем в консоль
logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Форматтер форматирует лог"""

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

logHandler.setFormatter(formatter)  # к хэндлеру прикрепляем форматтер
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)
