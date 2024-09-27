import telebot
import requests
import json

TOKEN = telebot.TeleBot('7377688530:AAHisaC8NdG0V5Hyt1LTzYdM3XByQzK8hy8')
API = 'aded1408985dd02715b736f41042eb33'

@TOKEN.message_handler(commands=['start'])
def start(message):
    TOKEN.send_message(message.chat.id, 'Наприши назву свого міста')

@TOKEN.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]

        TOKEN.reply_to(message, f'Погода зараз: {temp}°C')

        if temp >= 30.0:
            image = './very_hot.jpg'
        elif 18.0 <= temp < 30.0:
            image = './summer.png'
        elif 10.0 <= temp < 18.0:
            image = './mild.jpg'
        elif 0.0 <= temp < 10.0:
            image = './cool.jpg'
        elif -10.0 <= temp < 0.0:
            image = './cold.webp'
        elif -20.0 <= temp < -10.0:
            image = './very_cold.jpg'
        else:
            image = './hard_very_cold.webp'
    
        file = open(f'./photo/{image}', 'rb')
        TOKEN.send_photo(message.chat.id, file)
        file.close()
    else:
        TOKEN.reply_to(message, f'Місто вказано не правильно')

TOKEN.polling(non_stop=True)
