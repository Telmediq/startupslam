import os

from flask import Flask, Response, request
from redis import StrictRedis

app = Flask(__name__)
app.url_map.strict_slashes = False

# region: Utils
def get_suffix(value):
    if value % 10 == 1:
        return 'st'
    elif value % 10 == 2:
        return 'nd'
    elif value % 10 == 3:
        return 'rd'
    else:
        return 'th'


def validate_content(content):
    if 'value' not in content:
        return None, "Request json must have 'value: <int>'"
    value = content['value']
    if not isinstance(value, int):
        return None, "value must be of type int"
    return value, None


# endregion

# region: /fib/<int>/ Resource Endpoint

@app.route('/fib/<int:fibonacci_number>', methods=['GET'])
def get_fibonacci(fibonacci_number):
    try:
        result = fibonacci(fibonacci_number)
    except RecursionError:
        return Response(status=500,
                        response=f'The requested Fibonacci number was too large. Try a smaller value.')
    return Response(status=200,
                    response=f'The {fibonacci_number}{get_suffix(fibonacci_number)} Fibonacci number is {result}')


def compare_nth_response(fibonacci_number, value):
    if fibonacci_number == value:
        return Response(status=200,
                        response=f'{value} is the {fibonacci_number}{get_suffix(fibonacci_number)} Fibonacci number')
    else:
        return Response(status=200,
                        response=f'{value} is not the {fibonacci_number}{get_suffix(fibonacci_number)} Fibonacci number')


@app.route('/fib/<int:fibonacci_number>', methods=['POST'])
def check_if_nth_fibonacci(fibonacci_number):
    content = request.json
    value, error = validate_content(content)
    if error:
        return Response(status=400,
                        response=error)
    try:
        fibonacci(fibonacci_number)
    except RecursionError:
        return Response(status=500,
                        response=f'The requested Fibonacci number was too large. Try a smaller value.')
    return compare_nth_response(fibonacci_number, value)


# endregion

# region: /fib/ Root Endpoint

def compare_response(value, result):
    if result:
        return Response(status=200,
                        response=f'{value} is a Fibonacci number')
    else:
        return Response(status=200,
                        response=f'{value} is not a Fibonacci number')


@app.route('/fib/', methods=['POST'])
def check_if_fibonacci():
    content = request.json
    value, error = validate_content(content)
    if error:
        return Response(status=400,
                        response=error)
    result = is_fibonacci(value)
    return compare_response(value, result)


# endregion

# region: Fibonacci Methods

# Iterative Fibonacci
def is_fibonacci(value):
    a = 0
    b = 1
    iteration = 0
    if value in (0, 1):
        return True
    iter_value = 2
    while iter_value < value:
        iter_value = a + b
        a = b
        b = iter_value
        iteration += 1
    return iter_value == value


lookup_table = {}


# Memoized recursive Fibonacci
def fibonacci(n):
    memoizer = MemoizerFactory.create()
    if n in (0, 1):
        return n
    if memoizer.exists(n):
        return memoizer.get(n)
    result = fibonacci(n - 1) + fibonacci(n - 2)
    memoizer.set(n, result)
    return result


# endregion M

# region Memoizers
class MemoizerFactory:
    @classmethod
    def create(cls):
        REDIS_ENABLED = bool(os.environ.get("REDIS_ENABLED", False))
        if REDIS_ENABLED:
            return RedisMemoizer()
        else:
            return DictMemoizer()


class RedisMemoizer:
    redis = StrictRedis(host='redis')

    def exists(self, n):
        return RedisMemoizer.redis.exists(n)

    def set(self, n, value):
        RedisMemoizer.redis.set(n, value)

    def get(self, n):
        return int(RedisMemoizer.redis.get(n))


class DictMemoizer:
    lookup_table = None

    def __init__(self):
        if not DictMemoizer.lookup_table:
            DictMemoizer.lookup_table = dict()

    def exists(self, n):
        return n in lookup_table

    def set(self, n, value):
        lookup_table[n] = value

    def get(self, n):
        return lookup_table[n]

# endregion
