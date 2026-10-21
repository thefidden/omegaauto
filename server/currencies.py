"""Курсы валют EUR / CNY / RUB к USD, конвертация и фоновое обновление."""

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

rates: dict[str, float] = {'EUR': 0.0, 'CNY': 0.0, 'RUB': 0.0}
_lock = threading.Lock()
_started = False


def _fetch_rub_rates() -> dict[str, float]:
    response = requests.get(CBR_URL, timeout = 10)
    response.raise_for_status()
    response.encoding = 'windows-1251'

    rub_rates = {'RUB': 1.0}

    for valute in ET.fromstring(response.text).findall('Valute'):
        code = valute.findtext('CharCode')
        nominal = int(valute.findtext('Nominal'))
        value = float(valute.findtext('Value').replace(',', '.'))
        rub_rates[code] = value / nominal

    return rub_rates


def _to_usd(code: str, rub_rates: dict[str, float]) -> float:
    usd_rub = rub_rates['USD']
    if code == 'RUB':
        return 1.0 / usd_rub
    return rub_rates[code] / usd_rub


def update_rate(code: str, rate_to_usd: float | None = None) -> None:
    """Обновляет курс одной валюты к USD (с ЦБ, если rate_to_usd не задан)."""
    code = code.upper()
    if code not in rates:
        raise ValueError(f'Unsupported currency: {code}')

    if rate_to_usd is None:
        rate_to_usd = _to_usd(code, _fetch_rub_rates())

    with _lock:
        rates[code] = float(rate_to_usd)


def update_all_rates() -> None:
    """Обновляет курсы EUR, CNY, RUB к USD по ЦБ РФ."""
    rub_rates = _fetch_rub_rates()
    with _lock:
        for code in rates:
            rates[code] = _to_usd(code, rub_rates)


def convert(amount: int | float, from_currency: str, to_currency: str) -> float:
    """Конвертирует сумму через USD."""
    from_code = from_currency.upper()
    to_code = to_currency.upper()

    if from_code == to_code:
        return float(amount)

    with _lock:
        current = dict(rates)

    if from_code not in current or to_code not in current:
        raise ValueError(f'Unsupported currency pair: {from_code} -> {to_code}')

    if current[from_code] <= 0 or current[to_code] <= 0:
        update_all_rates()
        with _lock:
            current = dict(rates)

    return float(amount) * current[from_code] / current[to_code]


def start_background_updates() -> None:
    """При старте сервера: сразу обновить курсы, затем каждый час."""
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
            update_all_rates()
            logger.info('Currency rates updated: %s', rates)
        except Exception:
            logger.exception('Failed to update currency rates')
        time.sleep(UPDATE_INTERVAL)
