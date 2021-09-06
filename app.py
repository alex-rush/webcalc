# 06-09-21
from flask import Flask, render_template, request, make_response
from decimal import Decimal


number = ''  # основная переменная для хранения выражения(экрана калькулятора)
actions = ['+', '-', '*', '/']
app = Flask(__name__)


def calculating(tally):
    """операции вычисления"""
    global actions

    try:
        if tally[-1] in actions:  # если выражение вида только 'число' и 'действие'
            tally = tally + tally[:-1]

        if '.' in tally:  # вычисления для чисел с точкой
            for action in actions:
                if action in tally:
                    tally = tally.split(action)
                    dec1 = Decimal(tally[0])
                    dec2 = Decimal(tally[1])
                    if action == '+':
                        tally = str(dec1 + dec2)
                    elif action == '-':
                        tally = str(dec1 - dec2)
                    elif action == '*':
                        tally = str(dec1 * dec2)
                    elif action == '/':
                        if tally[1] == '0':
                            tally = 'ERROR'
                        else:
                            tally = str(dec1 / dec2)
            if tally[-1] == '0' and tally[-2] == '.':  # если после точки только ноль - вывод числа без дробной части
                tally = tally[:-2]
        else:  # вычисления для целых чисел
            for action in actions:
                if action in tally:
                    tally = tally.split(action)
                    if action == '+':
                        tally = str(int(tally[0]) + int(tally[1]))
                    elif action == '-':
                        tally = str(int(tally[0]) - int(tally[1]))
                    elif action == '*':
                        tally = str(int(tally[0]) * int(tally[1]))
                    elif action == '/':
                        if tally[1] == '0':
                            tally = 'ERROR'
                        else:
                            tally = str(int(tally[0]) / int(tally[1]))
                        if tally[-1] == '0' and tally[-2] == '.': # если после точки только ноль - вывод числа без дробной части
                            tally = tally[:-2]  # TODO нолей может быть много

    except Exception:
        tally = 'ERROR'
        print('произошла ошибка')
    return tally


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
    elif data == '.':
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
    elif data == '+' or data == '-' or data == '*' or data == '/':
        number = calculating(number)+data
        return responser(number)
    else:
        number += data
    return responser(number)


if __name__ == '__main__':
    app.run(port=80)
