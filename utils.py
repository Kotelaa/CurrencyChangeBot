import requests, json

from config import KEYS


class ConvertionException(Exception):
    pass


class Convertion:
    @staticmethod
    def convert(base: str, currency_change: str, amount: str):
        if currency_change == base:
            raise ConvertionException (f"Нельзя перевести {KEYS[base]} "
                                       f"в {KEYS[currency_change]}")

        try:
            currency_change_ticker = KEYS[currency_change]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту '{currency_change}'.")

        try:
            base_ticker = KEYS[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту '{base}'.")

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество '{amount}'.")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?"
                         f"fsym={currency_change_ticker}&tsyms={base_ticker}")

        currency_data = json.loads(r.content)[base_ticker]
        exchange_rate = float(amount) * currency_data
        return exchange_rate

