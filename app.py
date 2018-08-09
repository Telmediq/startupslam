from flask import Flask, Response, request
from redis import StrictRedis

app = Flask(__name__)
app.url_map.strict_slashes = False
redis = StrictRedis()


def get_suffix(value):
    if value % 10 == 1:
        return 'st'
    else:
        return 'th'


def validate_content(content):
    if 'value' not in content:
        return None, "Request json must have a value"
    value = content['value']
    if not isinstance(value, int):
        return None, "Value must be of type int"
    return value, None


@app.route('/fib/<int:fibonacci_number>', methods=['GET'])
def get_fibonacii(fibonacci_number):
    try:
        result = fibonacci(fibonacci_number)
    except RecursionError:
        return Response(status=500,
                        response=f'The requested Fibonacci number was too large. Try a smaller value.')
    return Response(status=200,
                    response=f'The {fibonacci_number}{get_suffix(fibonacci_number)} Fibonacci number is {result}')


@app.route('/fib/<int:fibonacci_number>', methods=['POST'])
def is_nth_fibonacci(fibonacci_number):
    content = request.json
    value, error = validate_content(content)

    if error:
        return Response(status=400,
                        response=error)

    try:
        result = fibonacci(fibonacci_number)
    except RecursionError:
        return Response(status=500,
                        response=f'The requested Fibonacci number was too large. Try a smaller value.')
    
    return compare_response(fibonacci_number, value, result)


def compare_response(fibonacci_number, value, result):
    if result == value:
        return Response(status=200,
                        response=f'{value} is the {fibonacci_number}{get_suffix(fibonacci_number)} Fibonacci number')
    else:
        return Response(status=200,
                        response=f'{value} is not the {fibonacci_number}{get_suffix(fibonacci_number)} Fibonacci number')


lookup_table = {}


def cache_value(n, value):
    redis.set(n, value)


def get_cache_value(n):
    return redis.get(n)


def fibonacci(n):
    if n in (0, 1):
        return n
    if n in lookup_table:
        return lookup_table[n]
    result = fibonacci(n - 1) + fibonacci(n - 2)
    lookup_table[n] = result
    return result
