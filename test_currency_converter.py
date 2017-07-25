from schema import Schema, Or
import requests
import pytest

from converter import CurrencyConverter


@pytest.mark.parametrize('test_input', ['USD', 'EUR', 'CZK'])
def test_api(test_input):
    schema = Schema({
        'base': str,
        'date': str,
        'rates': {str: Or(float, int)}
    })

    convert_url = 'http://api.fixer.io/latest'
    api_resp = requests.get(convert_url, params={'base': test_input})
    validated = schema.validate(api_resp.json())

    assert api_resp.status_code == 200
    assert validated == api_resp.json()


@pytest.mark.parametrize('test_input', ['RUB', 'PHP', 'GBP'])
def test_currency_rates_response(test_input):
    schema = Schema({
        str: Or(float, int)
    })
    c = CurrencyConverter()
    response = c.get_currency_rates(test_input)
    validated = schema.validate(response)

    assert response == validated


@pytest.mark.parametrize('test_amount', [1, 100, 1000.0])
@pytest.mark.parametrize('test_input', ['USD', 'EUR', 'CZK'])
@pytest.mark.parametrize('test_output', ['USD', 'GBP', None])
def test_exchange(test_amount, test_input, test_output):
    schema = Schema({
        'input': {
            'amount': Or(float, int),
            'currency': str,
        },
        'output': {
            str: Or(float, int)
        }
    })
    c = CurrencyConverter()
    data = c.exchange(test_amount, test_input, test_output)
    validated = schema.validate(data)

    assert data == validated
