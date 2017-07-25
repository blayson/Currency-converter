from flask import Flask, jsonify, request
from schema import Schema, Or, Use, SchemaError

from converter import CurrencyConverter, Validator

app = Flask(__name__)


@app.route('/currency_converter', methods=['GET'])
def get_resp():
    query = {
        'amount': request.args.get('amount'),
        'input_currency': request.args.get('input_currency'),
        'output_currency': request.args.get('output_currency')
    }
    #  Argument validation
    v = Validator()
    schema = Schema({
        'amount': Use(float),
        'input_currency':  Or(v.validate_currency_code, lambda s: len(s) == 3 and s.isalpha()),
        'output_currency': Or(None, v.validate_currency_code, lambda s: len(s) == 3 and s.isalpha()),
    })
    try:
        query = schema.validate(query)
    except SchemaError:
        return '', 400

    c = CurrencyConverter()
    try:
        return jsonify(c.exchange(query['amount'],
                                  v.convert_currency_code(query['input_currency']),
                                  v.convert_currency_code(query['output_currency'])))
    except (TypeError, KeyError):
        return '', 400


if __name__ == '__main__':
    app.run()
