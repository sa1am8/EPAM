from flask import render_template, Blueprint


main = Blueprint("main", __name__)
info = """Структура 2020/2021 навчального року

І семестр 

01.09.2020 – 24.12.2020    

Осінні канікули: 15.10.2020 - 30.10.2020

Зимові канікули: 26.12.2020 – 10.01.2021

ІІ семестр 

11.01.2021 – 28.05.2021      

Весняні канікули:      22.03.2020 – 28.03.2020

Всього навчальних днів – 168 

Святкові дні – 14.10, 25.12., 08.03., 03.05., 04.05, 10.05"""

@main.route("/")
def home():
    """Render home page"""
    return render_template("/html/home.html", title="Home", news=info.split('\n'))