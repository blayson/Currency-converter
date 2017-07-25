"""
Usage:
  book_flight.py --amount SUM --input_currency CURR [--output_currency CURR]
  book_flight.py (-h | --help)
  book_flight.py --version

Options:
  -h --help                 Show this screen.
  --amount SUM              Total amount
  --input_currency CURR
  --output_currency CURR
  --version                 Version of the application
"""
from docopt import docopt
from schema import Schema, Or, Use, SchemaError

import json

from converter import CurrencyConverter, Validator


def main():
    arguments = docopt(__doc__, version='1.0.0')
    #  Argument validation
    v = Validator()
    schema = Schema({
        '--amount': Use(float),
        '--input_currency': Or(v.validate_currency_code, lambda s: len(s) == 3 and s.isalpha()),
        '--output_currency': Or(None, v.validate_currency_code, lambda s: len(s) == 3 and s.isalpha()),
        '--help': bool,
        '--version': bool,
    })
    try:
        arguments = schema.validate(arguments)
    except SchemaError as e:
        exit('{0}\n'
             'currency_converter.py --help or -h for help message'.format(e))

    c = CurrencyConverter()
    try:
        return json.dumps(c.exchange(arguments['--amount'],
                                     v.convert_currency_code(arguments['--input_currency']),
                                     v.convert_currency_code(arguments['--output_currency'])),
                          indent=4, sort_keys=True)
    except (TypeError, KeyError):
        return {'error': 'unsupported currency'}

if __name__ == '__main__':
    print(main())
