import os
from flask import Flask
import redis


REDIS_HOST = os.environ.get('REDIS_HOST')
redis_client = redis.Redis(host=REDIS_HOST)


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))


def get_fibonacci(num):
    if (num == 0) or (num == 1): 
        return num
    return get_fibonacci(num-1) + get_fibonacci(num-2)


@app.route('/')
def hello():
    return 'Привет!'


@app.route('/<n>', methods=['GET'])
def get_fibonacci_api(n):
    n = int(n)
    if n > 30:
        return 'Диапазон принимаемых параметров ограничен числом 30, чтобы не перегружать слабую виртуальную машину.', 200
    stored_value = redis_client.get(n)
    if stored_value:
        return 'Для параметра {} использовано сохранённое значение: {}'.format(n, stored_value.decode("utf-8", errors="ignore")), 200
    new_value = get_fibonacci(n)
    redis_client.set(n, new_value)
    return 'Для параметра {} посчитано новое значение: {}'.format(n, new_value), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)