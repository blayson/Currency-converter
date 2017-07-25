import requests


class CurrencyConverter(object):
    """Parent class"""

    convert_url = 'http://api.fixer.io/latest'

    def __init__(self):
        super(CurrencyConverter, self).__init__()

    def get_currency_rates(self, base_currency):
        # Send request to API with currency rates and return json
        return requests.get(self.convert_url, params={'base': base_currency}).json()['rates']

    def convert_currency(self, amount, base_currency, output_currency):
        rates = self.get_currency_rates(base_currency)
        # Output currency validation and convert currency
        if not output_currency:
            return {currency: round(rate * amount, 2) for currency, rate in rates.items()}
        elif base_currency == output_currency.upper():
            return {output_currency: amount}

        return {output_currency: round(rates.get(output_currency.upper()) * amount, 2)}

    def exchange(self, amount, input_currency, output_currency=None):
        # Create and return dict with converted currencies
        return {
            'input': {
                'amount': amount,
                'currency': input_currency,
            },
            'output': self.convert_currency(amount, input_currency.upper(), output_currency)
        }


class Validator(object):
    """Parent class"""
    currencies = {
        "BGN": 'лв',
        "BRL": 'R$',
        "CNY": '¥',
        "CZK": 'Kč',
        "DKK": 'kr',
        "GBP": '£',
        "HKD": 'HK$',
        "HRK": 'kn',
        "HUF": 'Ft',
        "IDR": 'Rp',
        "ILS": '₪',
        "INR": '₹',
        "KRW": '₩',
        "MYR": 'RM',
        "PHP": '₱',
        "PLN": 'zł',
        "RON": 'lei',
        "RUB": '₽',
        "THB": '฿',
        "USD": '$',
        "ZAR": 'R',
        "EUR": '€'
    }

    def __init__(self):
        super(Validator, self).__init__()

    def convert_currency_code(self, currency_code):
        """
        Convert currency name to currency symbol. Example: € - 'EUR'
        :param currency_code: input currency
        :return: currency code
        """
        for name, symbol in self.currencies.items():
            if currency_code in (name, symbol):
                return name
        return currency_code

    def validate_currency_code(self, currency_code):
        """Validate if currency code is supported"""
        return True if currency_code in self.currencies.values() else False
