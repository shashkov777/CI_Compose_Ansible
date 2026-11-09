import telebot
import db 
from telebot import types 
from yookassa import Configuration, Payment
import uuid
from datetime import datetime, timedelta
import threading


def send_feedback(chat_id, order_id):

    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton("1", callback_data=f'feedback_{order_id}_1'),
        types.InlineKeyboardButton("2", callback_data=f'feedback_{order_id}_2'),
        types.InlineKeyboardButton("3", callback_data=f'feedback_{order_id}_3'),
        types.InlineKeyboardButton("4", callback_data=f'feedback_{order_id}_4'),
        types.InlineKeyboardButton("5", callback_data=f'feedback_{order_id}_5')
    )

    bot.send_message(chat_id, "Оцените заказ:", reply_markup=markup)


bot = telebot.TeleBot("8573939809:AAE-sW3ZzmUVpCPX-axSO6ryeoyQFWkXaEM")

name = None; 
ratio_name_new = None; modifier_id_new = None



@bot.message_handler(commands=['start'])
def start(message):

    db.create_tables()
    db.products_in()

    users_back = db.get_callback("users", message.from_user.id, "user_tg_id")

    if users_back:
        bot.send_message(message.chat.id, f"Рады снова вас видеть, {users_back['user_name']}!")
        main_menu(message)
    else:
        bot.send_message(message.chat.id, "Здравствуйте. Это бот проще. Давайте знакомится. Введите ваше имя: ")
        bot.register_next_step_handler(message, login_first)

def login_first(message):
    global name
    
    name = message.text.strip()
    user_id = message.from_user.id


    db.data_in("users", phone = "+72238222813", user_name = name, user_tg_id = user_id)
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}")    
    main_menu(message)


def main_menu(message):

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton("ЛЕНПОЛИГРАФМАШ", url='https://yandex.ru/maps/org/proshche/211188027241/?ll=30.317764%2C59.968660&utm_source=share&z=16'))
    markup.add(types.InlineKeyboardButton("У КАРАНДАША", url='https://yandex.ru/maps/org/proshche/216836401698/?ll=30.334473%2C59.983504&utm_source=share&z=16')) 
    markup.add(types.InlineKeyboardButton("ПОСМОТРЕТЬ НАШЕ МЕНЮ", callback_data='showmenu'))
    markup.add(types.InlineKeyboardButton("TELEGRAM", url='https://t.me/+ZrS7-0eYuDYwNDMy'))
    markup.add(types.InlineKeyboardButton("INSTAGRAM", url='https://www.instagram.com/proschee__?igsh=MTF4NjdjZ2lzMjQ4MA=='))
    markup.add(types.InlineKeyboardButton("ГРУППА ВКОНТАКТЕ", url='https://vk.com/proshecoffee'))
    markup.add(types.InlineKeyboardButton("ПЛЕЙСЛИСТ ПРОЩЕ", url='https://music.yandex.ru/playlists/e3a190f8-1952-6064-b9b6-8e5da157bcc0?utm_medium=copy_link'))
 
    bot.send_message(message.chat.id, "Познакомьтесь с нами! У нас много интересного!", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):

    global current_product, ratio_name_new, modifier_id_new, product_variant_table, cart_table_id 


    # bot.answer_callback_query(callback.id)
    # chat_id = callback.message.chat.id
    # msg_id = callback.message.message_id

    # try:
    #     bot.delete_message(chat_id, msg_id)
    # except:
    #     pass



    if callback.data == 'showmenu':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("ЛЕНПОЛИГРАФМАШ", callback_data='101'))
        markup.add(types.InlineKeyboardButton("У КАРАНДАША", callback_data='102'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        bot.send_message(callback.message.chat.id, "Выберите кофейню, а я покажу, что есть для вас в нашем меню", reply_markup=markup)        


    if callback.data == '101':

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("САМОВЫВОЗ", callback_data='pickup_len'))
        markup.add(types.InlineKeyboardButton("ДОСТАВКА", callback_data='delivery_len'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='showmenu'))

        bot.send_message(callback.message.chat.id, "Выберите способ получения вкусняшек", reply_markup=markup)        


    if callback.data == '102':

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("САМОВЫВОЗ", callback_data='pickup_kar'))
        #markup.add(types.InlineKeyboardButton("ДОСТАВКА", callback_data='delivery_kar'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='showmenu'))

        bot.send_message(callback.message.chat.id, "Выберите способ получения вкусняшек", reply_markup=markup)


    if callback.data == 'pickup_len':

        cart_table_id = db.data_in("carts", customer_id = callback.from_user.id, pickup_point_id = 101, pickup_type = 'pickup_lenpoligrafmash')

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("НАПИТКИ", callback_data='showdrink'))
        markup.add(types.InlineKeyboardButton("ЕДА", callback_data='showfood'))
        markup.add(types.InlineKeyboardButton("ДОПОЛНИТЕЛЬНЫЕ ТОВАРЫ", callback_data='showextra'))
        markup.add(types.InlineKeyboardButton("КОРЗИНА", callback_data='cart'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='101'))

        bot.send_message(callback.message.chat.id, "Наше меню", reply_markup=markup)

    if callback.data == 'delivery_len':

        cart_table_id = db.data_in("carts", customer_id = callback.from_user.id, pickup_point_id = 101, pickup_type = 'delivery_lenpoligrafmash')

        with open('delivery.jpg', 'rb') as file:
            bot.send_photo (
                callback.message.chat.id,
                file,
                caption="Внимание! \n \n" \
                "Мы осуществляем доставку только в пределах выделенной зоны.",
            )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("НАПИТКИ", callback_data='showdrink'))
        markup.add(types.InlineKeyboardButton("ЕДА", callback_data='showfood'))
        markup.add(types.InlineKeyboardButton("ДОПОЛНИТЕЛЬНЫЕ ТОВАРЫ", callback_data='showextra'))
        markup.add(types.InlineKeyboardButton("КОРЗИНА", callback_data='cart'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='101'))

        bot.send_message(callback.message.chat.id, "Наше меню", reply_markup=markup)

    if callback.data == 'pickup_kar':
        cart_table_id = db.data_in("carts", customer_id = callback.from_user.id, pickup_point_id = 102, pickup_type = 'pickup_karandash')

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("НАПИТКИ", callback_data='showdrink'))
        markup.add(types.InlineKeyboardButton("ЕДА", callback_data='showfood'))
        markup.add(types.InlineKeyboardButton("ДОПОЛНИТЕЛЬНЫЕ ТОВАРЫ", callback_data='showextra'))
        markup.add(types.InlineKeyboardButton("КОРЗИНА", callback_data='cart'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='102'))

        bot.send_message(callback.message.chat.id, "Наше меню", reply_markup=markup)

    if callback.data == 'showdrink':
        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("Американо", callback_data='1'))
        markup.add(types.InlineKeyboardButton("Эспрессо", callback_data='2'))
        markup.add(types.InlineKeyboardButton("Фильтр-кофе", callback_data='3'))
        markup.add(types.InlineKeyboardButton("Капучино", callback_data='4'))
        markup.add(types.InlineKeyboardButton("Латте", callback_data='5'))
        markup.add(types.InlineKeyboardButton("Флэт Уайт", callback_data='6'))
        markup.add(types.InlineKeyboardButton("Раф", callback_data='7'))
        markup.add(types.InlineKeyboardButton("Матча", callback_data='8'))
        markup.add(types.InlineKeyboardButton("Какао", callback_data='9'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        bot.send_message(callback.message.chat.id, "Напитки", reply_markup=markup)


    if callback.data == 'showfood':
        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("Бабка с шоколадом и вишней", callback_data='10'))
        markup.add(types.InlineKeyboardButton("Сэндвич с мясом", callback_data='11'))
        markup.add(types.InlineKeyboardButton("Краффин с соленой карамелью", callback_data='12'))
        markup.add(types.InlineKeyboardButton("Канеле", callback_data='13'))
        markup.add(types.InlineKeyboardButton("Ржаной даниш с брынзой", callback_data='14'))
        markup.add(types.InlineKeyboardButton("Круассан с сыром", callback_data='15'))
        markup.add(types.InlineKeyboardButton("Пан шоколя", callback_data='16'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        bot.send_message(callback.message.chat.id, "Еда", reply_markup=markup)


    if callback.data == 'showextra':

        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("Проще не бывает! термокружка", callback_data='17'))
        markup.add(types.InlineKeyboardButton("Матча-зона футболка", callback_data='18'))
        markup.add(types.InlineKeyboardButton("Coffee Starter Kit", callback_data='19'))
        markup.add(types.InlineKeyboardButton("Персональная подставка", callback_data='20'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))
        bot.send_message(callback.message.chat.id, "Дополнительные товары", reply_markup=markup)
  

    if callback.data.isdigit() and callback.data not in ("101", "102", "1001", "1002", "1003", "1004", "1005", "1006", "1007"):
        current_product = db.data_in("current_product", user_tg_id = callback.from_user.id, current_product_id = callback.data)
        current_product_back = db.get_callback_last1("current_product", callback.from_user.id, "user_tg_id")

        products = db.get_callback("products", current_product_back['current_product_id'], "id")
        products_variants = db.get_callback("product_variants", current_product_back['current_product_id'], "product_id")

        if products and products_variants["variant_name"] != 'onesize':

            #products = db.get_callback("products", current_product_back['current_product_id'], "id")

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Маленький", callback_data='Small'))
            markup.add(types.InlineKeyboardButton("Большой", callback_data='Big'))
            markup.add(types.InlineKeyboardButton("Назад", callback_data='showdrink'))

            with open(products['photo_path'], 'rb') as file:
                bot.send_photo(
                    callback.message.chat.id,
                    file,
                    caption=products['product_name'] + "\n\n" + products['desc'],
                    reply_markup=markup
                )

        if products and products_variants["variant_name"] == 'onesize':
            global product_variant_table
            product_variant_table = products_variants

            markup = types.InlineKeyboardMarkup()

            if products['category'] == "food" or products['category'] == "merch":
                ratio_name_new = "not"
                #modifier_id_new = "1007"

                modifier_id_new = db.data_in("current_modifiers", user_tg_id = callback.from_user.id, product_id = current_product_back['current_product_id'], modifier_id = 1007)
                modifier_id_new_back = db.get_callback_last1("current_modifiers", callback.from_user.id, "user_tg_id")

                products = db.get_callback("products", current_product_back['current_product_id'], "id")

                markup.add(types.InlineKeyboardButton(f"Добавить в корзину", callback_data='add_food'))

                if products['category'] == "food":
                    markup.add(types.InlineKeyboardButton("Назад", callback_data='showfood'))

                if products['category'] == "merch":
                    markup.add(types.InlineKeyboardButton("Назад", callback_data='showmerch'))

                with open(products['photo_path'], 'rb') as file:    
                    bot.send_photo(
                        callback.message.chat.id,
                        file,
                        caption=products['product_name'] + "\n\n" + products['desc'] + " " + str(products_variants['price']) + "₽",
                        reply_markup=markup
                    )

            if products['category'] == "drinks":

                #products = db.get_callback("products", current_product, "id")

                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("50% на 50%", callback_data='fiftyfifty'))

                markup.row (
                    types.InlineKeyboardButton("30% на 70%", callback_data='threeseven'),
                    types.InlineKeyboardButton("70% на 30%", callback_data='seventhree')
                )

                markup.row (
                    types.InlineKeyboardButton("60% на 40%", callback_data='sixfour'),
                    types.InlineKeyboardButton("40% на 60%", callback_data='foursix')
                )

                markup.add(types.InlineKeyboardButton("Базовый рецепт", callback_data='base'))
                markup.add(types.InlineKeyboardButton("Назад", callback_data='showdrink'))

                with open(products['photo_path'], 'rb') as file:
                    bot.send_photo(
                        callback.message.chat.id,
                        file,
                        caption=products['product_name'] + "\n\n" + products['desc'],
                        reply_markup=markup
                    )   

    if callback.data == "Small":

        current_product_back = db.get_callback_last1("current_product", callback.from_user.id, "user_tg_id")
        products = db.get_callback("products", current_product_back['current_product_id'], "id")

        product_variant_table = db.get_callback("product_variants", current_product_back['current_product_id'], "product_id", callback.data, "variant_name")

        #products = db.get_callback("products", current_product, "id")

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("50% на 50%", callback_data='fiftyfifty'))

        markup.row (
            types.InlineKeyboardButton("30% на 70%", callback_data='threeseven'),
            types.InlineKeyboardButton("70% на 30%", callback_data='seventhree')
        )

        markup.row (
            types.InlineKeyboardButton("60% на 40%", callback_data='sixfour'),
            types.InlineKeyboardButton("40% на 60%", callback_data='foursix')
        )

        markup.add(types.InlineKeyboardButton("Базовый рецепт", callback_data='base'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        with open(products['photo_path'], 'rb') as file:
            bot.send_photo(
                callback.message.chat.id,
                file,
                caption=products['product_name'] + "\n\n" + products['desc'],
                reply_markup=markup
            )

    if callback.data == "Big":

        current_product_back = db.get_callback_last1("current_product", callback.from_user.id, "user_tg_id")
        products = db.get_callback("products", current_product_back['current_product_id'], "id")

        product_variant_table = db.get_callback("product_variants", current_product_back['current_product_id'], "product_id", callback.data, "variant_name")

        #products = db.get_callback("products", current_product, "id")

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("50% на 50%", callback_data='fiftyfifty'))

        markup.row (
            types.InlineKeyboardButton("30% на 70%", callback_data='threeseven'),
            types.InlineKeyboardButton("70% на 30%", callback_data='seventhree')
        )

        markup.row (
            types.InlineKeyboardButton("60% на 40%", callback_data='sixfour'),
            types.InlineKeyboardButton("40% на 60%", callback_data='foursix')
        )
        
        markup.add(types.InlineKeyboardButton("Базовый рецепт", callback_data='base'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        with open(products['photo_path'], 'rb') as file:
            bot.send_photo(
                callback.message.chat.id,
                file,
                caption=products['product_name'] + "\n\n" + products['desc'],
                reply_markup=markup
            )

    if callback.data == 'fiftyfifty' or callback.data == 'threeseven' or callback.data == 'seventhree' \
    or callback.data == 'sixfour' or callback.data == 'foursix' or callback.data == "base":
        
    
        ratio_name_new = callback.data

        #products = db.get_callback("products", current_product, "id")
        current_product_back = db.get_callback_last1("current_product", callback.from_user.id, "user_tg_id")
        products = db.get_callback("products", current_product_back['current_product_id'], "id")

        # бля может отражаться как продукт айдишник
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Сироп карамель", callback_data='1001'))
        markup.add(types.InlineKeyboardButton("Сироп ваниль", callback_data='1002'))
        markup.add(types.InlineKeyboardButton("Сироп орех", callback_data='1003'))
        markup.add(types.InlineKeyboardButton("Овсяное молоко", callback_data='1004'))
        markup.add(types.InlineKeyboardButton("Миндальное молоко", callback_data='1005'))
        markup.add(types.InlineKeyboardButton("Кокосовое молоко", callback_data='1006'))
        markup.add(types.InlineKeyboardButton("Без добавок", callback_data='1007'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        with open(products['photo_path'], 'rb') as file:
            bot.send_photo(
                callback.message.chat.id,
                file,
                caption=products['product_name'] + "\n\n" + products['desc'],
                reply_markup=markup
            )
        

    if callback.data == '1001' or callback.data == '1002' or callback.data == '1003' or callback.data == '1004' \
    or callback.data == '1005' or callback.data == '1006' or callback.data == '1007':
        
        #modifier_id_new = callback.data
        modifier_id_new = db.data_in("current_modifiers", user_tg_id = callback.from_user.id, product_id = current_product_back['current_product_id'], modifier_id = callback.data)
        modifier_id_new_back = db.get_callback_last1("current_modifiers", callback.from_user.id, "user_tg_id")

        #products = db.get_callback("products", current_product, "id")  
        current_product_back = db.get_callback_last1("current_product", callback.from_user.id, "user_tg_id")
        products = db.get_callback("products", current_product_back['current_product_id'], "id")
        products_variants = db.get_callback("product_variants", current_product_back['current_product_id'], "product_id")    

        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("Добавить в корзину", callback_data='add_food'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        with open(products['photo_path'], 'rb') as file:    
            bot.send_photo(
                callback.message.chat.id,
                file,
                # допилить чтобы продакт вэриантс работал при выборе большой или маленький доп фильтр так он просто первый берет
                caption=products['product_name'] + "\n\n" + products['desc'] + " " + str(products_variants['price']) + "₽",
                reply_markup=markup
            )     


    if callback.data == 'add_food':

        #products = db.get_callback("products", current_product, "id")
        current_product_back = db.get_callback_last1("current_product", callback.from_user.id, "user_tg_id")
        products = db.get_callback("products", current_product_back['current_product_id'], "id")

        products_variants = db.get_callback("product_variants", current_product_back['current_product_id'], "product_id")
        
        modifier_id_new_back = db.get_callback_last1("current_modifiers", callback.from_user.id, "user_tg_id")
        
        cart_items = db.data_in("cart_items", cart_id = cart_table_id, product_variant_id = product_variant_table['product_id'], quantity = 1, item_price = product_variant_table['price'], ratio_name = ratio_name_new)
        cart_item_modifiers = db.data_in("cart_item_modifiers", cart_item_id = cart_items, modifier_id = modifier_id_new_back['modifier_id'])

        cart_table_id_back = db.get_callback("carts", cart_table_id, "id")  
        cart_items_back = db.get_callback("cart_items", cart_items, "id") 
        cart_items_modifiers_back = db.get_callback("cart_item_modifiers", cart_item_modifiers, "cart_item_id") 

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("В корзину", callback_data='cart'))
        markup.add(types.InlineKeyboardButton("Назад", callback_data='exit'))

        bot.send_message(
            callback.message.chat.id,
            f"✅ {products['product_name']}\n" +
            f"ID: {cart_items_back['product_variant_id']}\n" +
            f"Кол-во: {cart_items_back['quantity']}\n" +
            f"Модефаер айди: {cart_items_modifiers_back['modifier_id']}\n" +
            f"Карт айтем айди: {cart_items_modifiers_back['cart_item_id']}\n" +
            f"Название соотношений: {cart_items_back['ratio_name']}\n" +
            f"Ваш айди: {cart_table_id_back['customer_id']}\n" +
            f"Айди корзины: {cart_table_id_back['id']}\n" +
            f"Айди корзины из таблицы картс: {cart_items_back['cart_id']}\n" +
            f"Точка забора: {cart_table_id_back['pickup_point_id']}\n" +
            f"Цена: {cart_items_back['item_price']}₽"
        )

    if callback.data == 'cart':

        cart_table_id_back = db.get_callback_last1("carts", callback.from_user.id, "customer_id")
        cart_items_back = db.get_callback_last2("cart_items", cart_table_id_back['id'], "cart_id") 
        
        
        markup = types.InlineKeyboardMarkup()  
        bot.send_message(callback.message.chat.id, "Ваша корзина:")

        global total_price
        total_price = 0

        for number in range(0, len(cart_items_back)):
            items = cart_items_back[number]

            total_price = total_price + (items['quantity'] * items['item_price'])

            cart_items_modifiers_back = db.get_callback("cart_item_modifiers", items['id'], "cart_item_id")
        
            item_markup = types.InlineKeyboardMarkup()
            item_markup.add(types.InlineKeyboardButton("Изменить количество", callback_data=f'edit_{items["id"]}'))
            item_markup.add(types.InlineKeyboardButton("Удалить", callback_data=f'delete_{items["id"]}'))

            bot.send_message(
                callback.message.chat.id,
                f"Cart_item_id: {cart_items_modifiers_back['cart_item_id']}\n" +
                f"Modefier_id: {cart_items_modifiers_back['modifier_id']}\n" +
                f"ID: {items['cart_id']}\n" +
                f"Product ID: {items['product_variant_id']}\n" +
                f"Кол-во: {items['quantity']}\n" +
                f"Название соотношений: {items['ratio_name']}\n" +
                f"Цена: {items['item_price']}₽",
                reply_markup=item_markup  
            )

        markup.add(types.InlineKeyboardButton(f"Оформить заказ {total_price}", callback_data='order'))
        markup.add(types.InlineKeyboardButton("Очистить корзину", callback_data='clear'))
        #markup.add(types.InlineKeyboardButton("Назад", callback_data='')) 
        bot.send_message(callback.message.chat.id, "Действия с корзиной:", reply_markup=markup)


    if callback.data == 'order':        
        markup = types.InlineKeyboardMarkup()

        now = datetime.now()
        close_time = now.replace(hour=21, minute=0)
        current = now + timedelta(minutes=30)

        while current < close_time:
            slot_text = current.strftime("%H:%M")
            markup.add(types.InlineKeyboardButton(slot_text, callback_data=slot_text))
            current += timedelta(minutes=30)

        bot.send_message(callback.message.chat.id, "Выберите время приготовления заказа", reply_markup=markup)


    if ':' in callback.data and len(callback.data) == 5:

        # Configuration.account_id = 'ТВОЙ_SHOP_ID'  
        # Configuration.secret_key = 'test_ТВОЙ_КЛЮЧ'

        # idempotence_key = str(uuid.uuid4())
        # payment = Payment.create({
        #     "amount": {
        #         "value": f"{total_price}", # формат 2.00
        #         "currency": "RUB"
        #     },
        #     "confirmation": {
        #         "type": "redirect",
        #         "return_url": "https://t.me/proshecoffee_bot"
        #     },
        #     "capture": True, # деньги сразу на счет False - в юкасса застревают
        #     "description": "Заказ №72"
        # }, idempotence_key)

        # confirmation_url = payment.confirmation.confirmation_url

        # markup = types.InlineKeyboardMarkup()
        # markup.add(types.InlineKeyboardButton(f"Оплатить {total_price}", url=confirmation_url))
        # markup.add(types.InlineKeyboardButton("Отмена", callback_data='cart'))
        # bot.send_message(callback.message.chat.id, f"Оплатить?", reply_markup=markup)


        # payment_id = payment.id
        # payment = Payment.find_one(payment_id)

        # if payment["status"] == "succeeded":

        if True:
            cart_table_id_back = db.get_callback_last1("carts", callback.from_user.id, "customer_id")
            cart_items_back = db.get_callback_last2("cart_items", cart_table_id_back['id'], "cart_id")

            #orders = db.data_in("orders", customer_id = cart_table_id_back['customer_id'], pickup_point_id = cart_table_id_back['pickup_point_id'], total_price = total_price, status = payment["status"], pickup_type = cart_table_id_back['pickup_type'])
            orders = db.data_in("orders", customer_id = cart_table_id_back['customer_id'], pickup_point_id = cart_table_id_back['pickup_point_id'], total_price = total_price, status = "заглушка", pickup_type = cart_table_id_back['pickup_type'], take_time = callback.data)
            
            for number in range(0, len(cart_items_back)):
                items = cart_items_back[number]

                cart_items_modifiers_back = db.get_callback("cart_item_modifiers", items['id'], "cart_item_id") 

                order_items = db.data_in("order_items", order_id = orders, product_name = 'name', variant_name = items['product_variant_id'], quantity = items['quantity'], item_price = items['item_price'], ratio_name = items['ratio_name'])
                order_items_modifiers = db.data_in("order_item_modifiers", order_item_id = order_items, modifier_name = 'name', price = 1)


            orders_back = db.get_callback_last1("orders", callback.from_user.id, "customer_id")
            order_items_back = db.get_callback_last2("order_items", orders_back['id'], "order_id") 
            
            for number in range(0, len(order_items_back)):
                items = order_items_back[number]
                order_items_modifiers_back = db.get_callback("order_item_modifiers", items['id'], "order_item_id")
            
                # bot.send_message(
                #     callback.message.chat.id,
                #     "<b>Готовим заказ!</b>\n" +
                #     "Детали вашего заказа:\n" +
                #     f"Order_item_id: {order_items_modifiers_back['order_item_id']}\n" +
                #     f"Modefier_id: {order_items_modifiers_back['modifier_name']}\n" +
                #     f"ID: {items['order_id']}\n" +
                #     f"Product name: {items['product_name']}\n" +
                #     f"Variant name: {items['variant_name']}\n" +
                #     f"Кол-во: {items['quantity']}\n" +
                #     f"Название соотношений: {items['ratio_name']}\n" +
                #     f"Цена: {items['item_price']}₽\n" +

                #     f"customer_id: {orders_back['customer_id']}\n" +
                #     f"picup_point {orders_back['pickup_point_id']}\n" +
                #     f"total_price: {orders_back['total_price']}\n" +
                #     f"status: {orders_back['status']}\n" +
                #     f"created at: {orders_back['created_at']}\n"
                #     #reply_markup=item_markup  
                # )

            bot.send_message(
                callback.message.chat.id,
                f"✅ Заказ #{orders} принят!\n\n"
                f"Итого: {orders_back['total_price']}₽\n\n"
                f"⏰ Время: {orders_back['take_time']}\n"
                f"📍 Точка: {orders_back['pickup_point_id']}\n\n"
                f"Готовим ваш заказ!"
            )

            ADMIN_ID = 6802378568

            if callback.from_user.id != ADMIN_ID:
                users_back = db.get_callback("users", callback.from_user.id, "user_tg_id")

                admin_message = (
                    f"🔔 НОВЫЙ ЗАКАЗ #{orders}\n\n"
                    f"💰 Сумма: {orders_back['total_price']}₽\n"
                    f"⏰ Время: {orders_back['take_time']}\n"
                    f"📍 Точка: {cart_table_id_back['pickup_type']}\n"
                    f"👤 Клиент: {users_back['user_name']} (ID: {callback.from_user.id})\n"
                    f"📅 {orders_back['created_at']}"
                )

                bot.send_message(ADMIN_ID, admin_message)            

            threading.Timer(
                10, #3600
                send_feedback, 
                args=[callback.message.chat.id, orders]).start()
            
    if callback.data.startswith("feedback_"):
        parts = callback.data.split("_")
        order_id = parts[1]
        rating = int(parts[2])
        
        feedback = db.data_in("feedback", order_id=order_id, rating=rating)

        feedback_back = db.get_callback("feedback", feedback, "order_id")
        bot.send_message(callback.message.chat.id, f"Спасибо за оценку {feedback_back['rating']} ⭐")

        # if payment["status"] == "canceled":
        #     pass
        # if payment["status"] == "pending":
        #     pass
        # if payment["status"] == "waiting_for_capture":
        #     pass


    if callback.data == 'clear':
        pass




bot.polling(non_stop=True)