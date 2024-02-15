import requests
from bs4 import BeautifulSoup as BS
import time
import telebot
import config


def finder(response):
    
    soup = BS(response.text, 'html.parser')
    titles = soup.findAll('a', class_='woocommerce-LoopProduct-link')
    products = []
    finds = ["Электронная книга", "Игровое кресло", "Графический планшет", "Рюкзак с LED-дисплеем"]
    
    for title in titles:
        for find in finds:
            if title.text.__contains__(find) and not title.text.__contains__("(скоро в наличии)"):
                products.append(title.text)
                
    return products



def parser(url1, url2):
    response_1 = requests.get(url=url1)

    if response_1.status_code == 200:
        products_1 = finder(response=response_1)   
    
        response_2 = requests.get(url=url2)
        if response_2.status_code == 200:
            products_2 = finder(response=response_2)      
        
        else:
           return f"Статус 2 {response_2.status_code}"
    
    else:
        return f"Статус 1 {response_1.status_code}"
    
    return "{}\n{}".format('\n'.join(products_1), '\n'.join(products_2))
    

    





bot = telebot.TeleBot(config.tokenTG)

@bot.message_handler(commands=['start'])
def send_info(message):
    bot.send_message(message.from_user.id, text="Привет, каждый час я буду слать инфо по товарам.")
    while True:
        bot.send_message(message.from_user.id, text=parser("https://znaniashop.ru/shop/page/2/", "https://znaniashop.ru/shop/page/3/"))
        time.sleep(3600)


bot.infinity_polling()