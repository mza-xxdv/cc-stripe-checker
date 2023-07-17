import requests

def hit_sender(card,message,chat_id):
    bot_token = '6116552527:AAHlR_23YAZ9DIKhcc3maLfLA4Dv65qapAg' #ganti sesuai selera
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)
