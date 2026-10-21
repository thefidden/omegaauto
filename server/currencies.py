"""Курсы валют EUR / CNY / RUB к российскому рублю, конвертация и фоновое обновление."""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
import xml.etree.ElementTree as ET

import requests

logger = logging.getLogger(__name__)

CBR_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
UPDATE_INTERVAL = 60 * 60 * 24

_rates: dict[str, float] = {'EUR': 0.0, 'CNY': 0.0, 'RUB': 1.0}
_lock = threading.Lock()
_started = False


def _load_rates_from_cbr() -> None:
    response = requests.get(CBR_URL, timeout = 10)
    response.raise_for_status()
    response.encoding = 'windows-1251'

    cbr = {'RUB': 1.0}
    for valute in ET.fromstring(response.text).findall('Valute'):
        code = valute.findtext('CharCode')
        nominal = int(valute.findtext('Nominal'))
        value = float(valute.findtext('Value').replace(',', '.'))
        cbr[code] = value / nominal

    with _lock:
        _rates['RUB'] = 1.0
        for code in ('EUR', 'CNY'):
            if code not in cbr:
                raise ValueError(f'Currency code "{code}" not found in CBR rates')
            _rates[code] = cbr[code]


def get_rates() -> dict[str, float]:
    """Возвращает курсы EUR / CNY / RUB к рублю (подтягивает с ЦБ, если ещё не загружены)."""
    with _lock:
        current = dict(_rates)

    if current['EUR'] <= 0 or current['CNY'] <= 0:
        _load_rates_from_cbr()
        with _lock:
            current = dict(_rates)

    return current


def convert(amount: int | float, from_currency: str, to_currency: str) -> float:
    """Конвертирует сумму через курсы к RUB."""
    from_code = from_currency.upper()
    to_code = to_currency.upper()

    if from_code == to_code:
        return float(amount)

    rates = get_rates()

    if from_code not in rates or to_code not in rates:
        raise ValueError(f'Unsupported currency pair: {from_code} -> {to_code}')

    return float(amount) * rates[from_code] / rates[to_code]


def start_background_updates() -> None:
    """При старте сервера: сразу обновить курсы, затем раз в сутки."""
    global _started

    if _started or not _should_run_updater():
        return

    _started = True
    threading.Thread(target = _update_loop, name = 'currency-updater', daemon = True).start()


def _should_run_updater() -> bool:
    skip = {'migrate', 'makemigrations', 'test', 'shell', 'collectstatic', 'createsuperuser'}

    if any(cmd in sys.argv for cmd in skip):
        return False

    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
        return False

    return True


def _update_loop() -> None:
    while True:
        try:
            _load_rates_from_cbr()
            logger.info('Currency rates updated: %s', get_rates())
        except Exception:
            logger.exception('Failed to update currency rates')

        time.sleep(UPDATE_INTERVAL)
