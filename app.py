# 06-09-21
from flask import Flask, render_template, request, make_response
from decimal import Decimal


number = ''  # основная переменная для хранения выражения(экрана калькулятора)
actions = ['+', '-', '*', '/']
app = Flask(__name__)


def calculating(number):
    """операции вычисления"""
    actions = ['+', '-', '*', '/']

    try:
        if number[-1] in actions:  # если выражение вида только 'число' и 'действие'
            number = number + number[:-1]

        if '.' in number:  # вычисления для чисел с точкой
            for action in actions:
                if action in number:
                    number = number.split(action)
                    dec1 = Decimal(number[0])
                    dec2 = Decimal(number[1])
                    if action == '+':
                        number = str(dec1 + dec2)
                    elif action == '-':
                        number = str(dec1 - dec2)
                    elif action == '*':
                        number = str(dec1 * dec2)
                    elif action == '/':
                        if number[1] == '0':
                            number = 'ERROR'
                        else:
                            number = str(dec1 / dec2)
            if number[-1] == '0' and number[-2] == '.':  # если после точки только ноль - вывод числа без дробной части
                number = number[:-2]
        else:  # вычисления для целых чисел
            for action in actions:
                if action in number:
                    number = number.split(action)
                    if action == '+':
                        number = str(int(number[0]) + int(number[1]))
                    elif action == '-':
                        number = str(int(number[0]) - int(number[1]))
                    elif action == '*':
                        number = str(int(number[0]) * int(number[1]))
                    elif action == '/':
                        if number[1] == '0':
                            number = 'ERROR'
                        else:
                            number = str(int(number[0]) / int(number[1]))
                        if number[-1] == '0' and number[-2] == '.': # если после точки только ноль - вывод числа без дробной части
                            number = number[:-2]

    except:
        number = 'ERROR'
    print(number)
    return number


def responser(result):
    resp = make_response(render_template('indicator.html', number=result))
    resp.set_cookie('calc_cook', result)
    return resp


@app.route('/')
def calculator():
    resp = make_response(render_template('calc.html'))
    resp.set_cookie('calc_cook', number)
    return resp


@app.route('/count', methods=['POST'])  # web application calculator
def count():
    global number
    data = request.form.get('number')
    number = request.cookies.get('calc_cook')
    if number == 'HELLO':
        number = ''
    if data == 'C':
        number = 'HELLO'
        return responser(number)
    elif data == '<':
        number = number[:-1]
    elif data == '.':  # TODO доработать ввод чисел с точкой
        if '.' in number:
            dot = number.count('.')
            for act in actions:
                if act in number and dot < 2:
                    number += data
            return responser(number)
        else:
            number += data
    elif data == '=':
        number = calculating(number)
        result = number
        number = ''
        resp = make_response(render_template('indicator.html', number=result))
        resp.set_cookie('calc_cook', number)
        return resp
    elif data == '+' or data == '-' or data == '*' or data == '/':  # TODO обсчет длинных выражений
        number = calculating(number)+data
        return responser(number)
    else:
        number += data
    return responser(number)


if __name__ == '__main__':
    app.run(port=80)
