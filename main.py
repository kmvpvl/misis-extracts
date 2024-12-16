
import telebot
from telebot import types
import re
import os
from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.getenv("API_TOKEN"))

# Продукты и другие данные
products = {
    "group1": [
        {"name": "Пастернак полевой. Pastinaca sativa (семена) – сверхкритический CO2-экстракт.\n", "description": "Имеет сладковато-пряный, цветочный аромат. Богат активными веществами, благодаря чему эффективен при лечении псориаза, витилиго, некоторых видов облысения и диабета (в сочетании с УФ-облучением). Обладает также спазмолитическим, противовоспалительным и противогрибковым действием, укрепляет ногти.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Пихта.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Дудник лесной. Angelica sylvestris (корни) – сверхкритический CO2-экстракт.\n", "description": "Лекарственное средство с фурокумаринами, эффективное при псориазе, витилиго, облысении и диабете. Обладает обезболивающим, успокаивающим, потогонным, мочегонным, дезинфицирующим и антипаразитным действием.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Дудник.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Хмель обыкновенный. Humulus lupulus (шишки) – сверхкритический CO2-экстракт.\n", "description": "Богат фитостеринами, каротиноидами и др. антиоксидантами. Обладает антибактериальными, противовоспалительными и противогрибковыми свойствами. Улучшает состояние кожи, оказывает антивозрастной эффект. Положительно влияет на нервную систему (седативное, антидепрессантное действие, сон). Используется в косметике, ароматерапии и кулинарии.\n\nОбъём 1 (3 мл) - 645 руб.\nОбъём 2 (10 мл) - 1290 руб.", "image": "Хмель.jpg", "volumes": [(1, 645), (2, 1290)]},
        {"name": "Облепиха крушиновидная. Hippophae rhamnoides (косточки) – сверхкритический CO2-экстракт.\n", "description": "Оранжево-красная маслянистая жидкость с характерным запахом. Ускоряет заживление ран и повреждений кожи и слизистых, обладает противовоспалительным и антиоксидантным действием. Снижает уровень холестерина, осветляет пигментные пятна, укрепляет волосы и ногти.\n\nОбъём 1 (3 мл) - 445 руб.\nОбъём 2 (10 мл) - 890 руб.", "image": "Облепиха.jpg", "volumes": [(1, 445), (2, 890)]},
        {"name": "Морошка приземистая. Rubeus chamaemorus (косточки) – сверхкритический CO2-экстракт.\n", "description": "Имеет приятный, сладковатый аромат. Повышает упругость кожи, обладает противовоспалительным и заживляющим, увлажняющим и успокаивающим действием. Используется в косметических средствах (кремах, сыворотках, антицеллюлитных средствах).\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Морошка.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Земляника лесная. Fragaria vesca (семена) – сверхкритический CO2-экстракт.\n", "description": "Имеет ягодный, свежий аромат. Обладает антивозрастным, увлажняющим и питательным действием для кожи, укрепляет волосы и устраняет перхоть. В ароматерапии – расслабляет и нормализует сон. При массаже – улучшает кровообращение и снимает боль и отёки.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Земляника.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Малина лесная. Rubus idaeus (косточки) – сверхкритический CO2-экстракт.\n", "description": "Имеет нежный, сладковатый аромат. Очищает, защищает и питает кожу благодаря содержанию активных природных антиоксидантов, антиканцерогенови антимутагенов. Оказывает противовоспалительное и ранозаживляющее действие. Устраняет ломкость волос, делает их блестящими и шелковистыми.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Малина.jpg", "volumes": [(1, 845), (2, 1690)]},

    ],
    "group2": [
        {"name": "Пижма обыкновенная. Tanacetum vulgare (цветки) – эфирное масло.\n", "description": "Приятный травянистый аромат. Обладает антисептическим, обезболивающим, противовоспалительным действием, ускоряет регенерацию кожи, укрепляет иммунитет и успокаивает. Проявляет сильное антидепрессивное действие. Применяется в ароматерапии, косметологии и при массаже.\n\nОбъём 1 (3 мл) - 645 руб.\nОбъём 2 (10 мл) - 1290 руб.", "image": "Пижма.jpg", "volumes": [(1, 645), (2, 1290)]},
        {"name": "Ель обыкновенная. Picea abies (хвоя) – эфирное масло.\n", "description": "Обладает резким, свежим, смолисто-горьким ароматом. Содержит в составе до 50% борнилацетата, а также сантен, пинен, камфен, фелландрен, лимонен, камфару, борнеол, кадинен. Обладает отхаркивающим, спазмолитическим действием, повышает иммунитет, улучшает состояние кожи и снимает стресс. Применяется в ароматерапии, для массажа и принятия ванн.\n\nОбъём 1 (3 мл) - 445 руб.\nОбъём 2 (10 мл) - 890 руб.", "image": "Ель.jpg", "volumes": [(1, 445), (2, 890)]},
        {"name": "Пихта сибирская. Abies sibirica (хвоя) – эфирное масло.\n", "description": "Имеет свежий, сладковатый хвойный аромат. Тонизирует, снимает стресс при ароматерапии. Очищает и разглаживает кожу, устраняет запах пота. Используется как лечебно-профилактическое средство для улучшения общего состояния организма.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Пихта2.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Сосна обыкновенная. Pinus sylvestris (хвоя) – эфирное масло.\n", "description": "Имеет глубокий смолистый аромат. Повышает иммунитет, успокаивает, стимулирует умственную активность, перебивает неприятные запахи. Омолаживает и успокаивает кожу, укрепляет волосы. Используется в косметике и отлично подходит для ароматизации саун/бань.\n\nОбъём 1 (3 мл) - 645 руб.\nОбъём 2 (10 мл) - 1290 руб.", "image": "Сосна.jpg", "volumes": [(1, 645), (2, 1290)]},
        {"name": "Полынь австрийская. Artemisia austriaca (листья) – эфирное масло.\n", "description": "Имеет горьковато-свежий, камфорный аромат. Снимает стресс, повышает концентрацию и сексуальную активность. Используется для ароматизации, дезинфекции, отпугивания насекомых, повышения иммунитета и нормализации обмена веществ.\n\nОбъём 1 (3 мл) - 645 руб.\nОбъём 2 (10 мл) - 1290 руб.", "image": "Полынь.jpg", "volumes": [(1, 645), (2, 1290)]},
        {"name": "Лавр благородный. Laurus nobilis (листья) – эфирное масло.\n", "description": "Имеет смолистый, сладкий аромат. Обладает противовоспалительным и бактерицидным действием, улучшает пищеварение. Используется в косметике (против акне, перхоти, выпадения волос) и для улучшения состояния кожи, а также в кулинарии.\n\nОбъём 1 (3 мл) - 445 руб.\nОбъём 2 (10 мл) - 890 руб.", "image": "Лавр.jpg", "volumes": [(1, 445), (2, 890)]},
    ],
    "group3": [
        {"name": "Ель обыкновенная. Picea abies (хвоя) – воск.\n", "description": "Обладает свежим, смолисто-горьким хвойным ароматом. Имеет нежную, мягкую консистенцию, содержит в себе все полезные свойства елового масла. Используется как загуститель или стабилизатор. Применяется при изготовлении косметических средств, свечей и мыла. Возможно применение в качестве самостоятельного средства.\n\nОбъём 1 (3 мл) - 445 руб.\nОбъём 2 (10 мл) - 890 руб.", "image": "Ель.jpg", "volumes": [(1, 445), (2, 890)]},
        {"name": "Пихта сибирская. Abies sibirica (хвоя) – воск.\n", "description": "Обладает свежим, сладковатым, смолисто-хвойным, слегка терпким ароматом. Имеет нежную, мягкую консистенцию, содержит в себе все полезные свойства пихтового масла. Применяется как загуститель или стабилизатор. Используется при изготовлении косметических средств, свечей и мыла. Возможно применение в качестве самостоятельного средства.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Пихта2.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Сосна обыкновенная. Pinus sylvestris (хвоя) – воск.\n", "description": "Обладает глубоким, смолистым, горьковатым, прохладным ароматом. Имеет нежную, мягкую консистенцию, содержит в себе все полезные свойства соснового масла, но имеет иную текстуру. Применяется как загуститель или стабилизатор. Используется при изготовлении косметических средств, свечей и мыла. Возможно применение в качестве самостоятельного средства.\n\nОбъём 1 (3 мл) - 645 руб.\nОбъём 2 (10 мл) - 1290 руб.", "image": "Сосна.jpg", "volumes": [(1, 645), (2, 1290)]},
        {"name": "Морошка приземистая. Rubeus chamaemorus (косточки) – воск.\n", "description": "Имеет приятный, сладковатый, не очень яркий, ягодно-растительный аромат. Имеет нежную, мягкую консистенцию, содержит в себе все полезные свойства морошкового масла, но имеет иную текстуру. Применяется как загуститель или стабилизатор. Используется при изготовлении косметических средств - в бальзамах и губных помадах, а также в свече- и мыловарении. Возможно применение в качестве самостоятельного средства.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Морошка.jpg", "volumes": [(1, 845), (2, 1690)]},
        {"name": "Земляника лесная. Fragaria vesca (семена) – воск.\n", "description": "Аромат утончённый, ягодный, свежий, яркий. Имеет нежную, мягкую консистенцию, содержит в себе все полезные свойства морошкового масла, но имеет иную текстуру. Применяется как загуститель или стабилизатор. Используется при изготовлении косметических средств - в бальзамах и губных помадах, а также в свече- и мыловарении. Возможно применение в качестве самостоятельного средства.\n\nОбъём 1 (3 мл) - 845 руб.\nОбъём 2 (10 мл) - 1690 руб.", "image": "Земляника.jpg", "volumes": [(1, 845), (2, 1690)]},
    ]
}

cart = {}
admin_chat_id = os.getenv("ADMIN")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("CO2-экстракты", callback_data="group1")
    button2 = types.InlineKeyboardButton("Эфирные масла", callback_data="group2")
    button3 = types.InlineKeyboardButton("Воска", callback_data="group3")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, f"""<b>Добро пожаловать!</b> 🎉

Здесь вы можете найти широкий ассортимент товаров, которые помогут вам сделать вашу жизнь удобнее и ярче. 🛍️

Для просмотра корзины воспользуйтесь: /cart
""", reply_markup=markup, parse_mode='HTML')


@bot.message_handler(commands=['cart'])
def show_cart(message):
    user_cart = cart.get(str(message.chat.id), [])
    if not user_cart:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
        return

    cart_details = "Ваша корзина:\n"
    total_price = 0
    cart_items = []
    for group in user_cart:
        for i, item in enumerate(user_cart[group]):
            product = item["product"]
            cart_details += f"{i + 1}. {product['name']} - Объем {item['volume']} - Количество: {item['quantity']}\n"
            total_price += item["quantity"] * product['volumes'][item["volume"] - 1][1]
            cart_items.append(f"{i + 1}")

    cart_details += f"\nОбщая стоимость: {total_price} руб."

    markup = types.InlineKeyboardMarkup()
    button_clear = types.InlineKeyboardButton("Очистить корзину", callback_data="clear_cart")
    markup.add(button_clear)

    for item_num in cart_items:
        button_remove = types.InlineKeyboardButton(f"Удалить товар {item_num}", callback_data=f"remove_{item_num}")
        markup.add(button_remove)
    button2 = types.InlineKeyboardButton("Оформить", callback_data="checkout")
    markup.add(button2)
    bot.send_message(message.chat.id, cart_details, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "clear_cart")
def clear_cart(call):
    cart[str(call.message.chat.id)] = []
    bot.send_message(call.message.chat.id, "Ваша корзина очищена.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
def remove_item(call):
    item_num = int(call.data.split('_')[1]) - 1
    user_cart = cart.get(str(call.message.chat.id), [])

    if not user_cart:
        bot.send_message(call.message.chat.id, "Ваша корзина пуста.")
        return

    # Удаляем товар
    for group in user_cart:
        if item_num < len(user_cart[group]):
            removed_item = user_cart[group].pop(item_num)
            bot.send_message(call.message.chat.id, f"Товар {removed_item['product']['name']} удален из корзины.")
            break

    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_cart(call.message)


@bot.callback_query_handler(func=lambda call: call.data in ["group1", "group2", "group3"])
def group_selected(call):
    group = call.data
    markup = types.InlineKeyboardMarkup()

    for i, product in enumerate(products.get(group, [])):
        button = types.InlineKeyboardButton(product['name'], callback_data=f"product_{group}_{i}")
        markup.add(button)

    back_button = types.InlineKeyboardButton("Назад к группам", callback_data="back_to_groups")
    markup.add(back_button)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Выберите продукт:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def product_selected(call):
    group, idx = call.data.split('_')[1:3]
    idx = int(idx)
    product = products[group][idx]
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup()

    for vol in product['volumes']:
        volume_button = types.InlineKeyboardButton(f"Объём {vol[0]} / {vol[1]} руб.",
                                                   callback_data=f"volume_{group}_{idx}_{vol[0]}")
        markup.add(volume_button)

    back_button = types.InlineKeyboardButton("Назад", callback_data=f"back_{group}")
    markup.add(back_button)

    with open(product['image'], 'rb') as photo:
        bot.send_photo(call.message.chat.id, photo, caption=f"{product['name']}\n{product['description']}",
                       reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("volume_"))
def volume_selected(call):
    group, idx, volume = call.data.split('_')[1:4]
    idx = int(idx)
    volume = int(volume)
    product = products[group][idx]
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        button = types.InlineKeyboardButton(str(i), callback_data=f"quantity_{group}_{idx}_{volume}_{i}")
        markup.add(button)

    bot.send_message(call.message.chat.id,
                     f"Выберите количество для {product['name']}\n\nОбъем {volume} - {product['volumes'][volume - 1][1]} руб.",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("quantity_"))
def quantity_selected(call):
    group, idx, volume, quantity = call.data.split('_')[1:5]
    idx = int(idx)
    volume = int(volume)
    quantity = int(quantity)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if str(call.message.chat.id) not in cart:
        cart[str(call.message.chat.id)] = {}

    if group not in cart[str(call.message.chat.id)]:
        cart[str(call.message.chat.id)][group] = []

    cart[str(call.message.chat.id)][group].append({"product": products[group][idx], "volume": volume, "quantity": quantity})

    bot.send_message(call.message.chat.id, f"Продукт добавлен в корзину: /cart.\n\nПродолжить заказ или перейти к оформлению?")

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Продолжить", callback_data="back_to_groups")
    button2 = types.InlineKeyboardButton("Оформить", callback_data="checkout")
    markup.add(button1, button2)

    bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def checkout(call):
    username = call.message.from_user.username
    if username:
        telegram_link = f"@{username}"
    else:
        telegram_link = "Не указан"

    bot.send_message(call.message.chat.id, "Введите ваше ФИО, которое указано на карте:")
    bot.register_next_step_handler(call.message, get_fio, telegram_link)


def get_fio(message, telegram_link):
    fio = message.text
    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", fio):  # ФИО должно содержать только буквы и пробелы
        bot.send_message(message.chat.id, "Пожалуйста, введите ФИО только с буквами и пробелами.")
        bot.register_next_step_handler(message, get_fio, telegram_link)
        return

    bot.send_message(message.chat.id, "Введите ваш номер телефона:\n(+7...")
    bot.register_next_step_handler(message, get_phone, fio, telegram_link)


def get_phone(message, fio, telegram_link):
    telegram_link = message.from_user.username
    phone = message.text
    if not re.match(r"^[+0-9]{10,15}$", phone):  # Телефон должен содержать только цифры и знак "+"
        bot.send_message(message.chat.id, "Пожалуйста, введите номер телефона только с цифрами и знаком +.")
        bot.register_next_step_handler(message, get_phone, fio, telegram_link)
        return

    order = f"Новый заказ:\nФИО: {fio}\nТелефон: {phone}\nTelegram: @{telegram_link}\n\nКорзина:\n"
    total_price = 0
    for group in cart[str(message.chat.id)]:
        for item in cart[str(message.chat.id)][group]:
            product = item["product"]
            order += f"{product['name']} - Объем {item['volume']} - Количество: {item['quantity']}\n"
            total_price += item["quantity"] * product['volumes'][item["volume"] - 1][1]

    order += f"\nОбщая стоимость: {total_price} руб."

    bot.send_message(admin_chat_id, order)

    bot.send_message(message.chat.id, "Ваш заказ оформлен.🎉 \nСкоро с вами свяжется менеджер.👩‍💼\n\nИспользуйте /start, чтобы продолжить пользоваться ботом.")
    cart.clear()


@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
def go_back(call):
    if call.data == "back_to_groups":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        group = call.data.split('_')[1]
        group_selected(call)


if __name__ == '__main__':
    bot.polling(none_stop=True)






#
# import telebot
# from telebot import types
# import re
#
# bot = telebot.TeleBot('7703925926:AAGztDvZ371QzKE0G-WRyd5UDbbtAqv0Yvs')
#
# # Продукты и другие данные
# products = {
#     "group1": [
#         {"name": "Пастернак полевой.\n", "description": "Имеет сладковато-пряный, цветочный аромат. Богат активными веществами, благодаря чему эффективен при лечении псориаза, витилиго, некоторых видов облысения и диабета (в сочетании с УФ-облучением). Обладает также спазмолитическим, противовоспалительным и противогрибковым действием, укрепляет ногти.\n\nОбъём 1 - 3мл\nОбъём 2 - 10мл", "image": "Пихта.jpg", "volumes": [(1, 845), (2, 150)]},
#         {"name": "Дудник лесной.", "description": "Описание продукта 2", "image": "чашки.jpeg", "volumes": [(1, 120), (2, 170)]},
#         {"name": "Хмель обыкновенный.", "description": "Описание продукта 3", "image": "чашки.jpeg", "volumes": [(1, 130), (2, 180)]},
#         {"name": "Облепиха крушиновидная.", "description": "Описание продукта 4", "image": "чашки.jpeg", "volumes": [(1, 140), (2, 190)]},
#         {"name": "Морошка приземистая.", "description": "Описание продукта 4", "image": "чашки.jpeg", "volumes": [(1, 150), (2, 200)]},
#         {"name": "Земляника лесная.", "description": "Описание продукта 4", "image": "чашки.jpeg", "volumes": [(1, 160), (2, 210)]},
#         {"name": "Малина лесная.", "description": "Описание продукта 4", "image": "чашки.jpeg", "volumes": [(1, 160), (2, 210)]},
#
#     ],
#     "group2": [
#         {"name": "Продукт 7", "description": "Описание продукта 5", "image": "чашки.jpeg", "volumes": [(1, 110), (2, 160)]},
#         {"name": "Продукт 8", "description": "Описание продукта 6", "image": "чашки.jpeg", "volumes": [(1, 125), (2, 175)]},
#         {"name": "Продукт 9", "description": "Описание продукта 7", "image": "чашки.jpeg", "volumes": [(1, 135), (2, 185)]},
#         {"name": "Продукт 10", "description": "Описание продукта 8", "image": "чашки.jpeg", "volumes": [(1, 145), (2, 195)]},
#         {"name": "Продукт 11", "description": "Описание продукта 8", "image": "чашки.jpeg", "volumes": [(1, 145), (2, 195)]},
#         {"name": "Продукт 12", "description": "Описание продукта 8", "image": "чашки.jpeg", "volumes": [(1, 145), (2, 195)]},
#     ],
#     "group3": [
#         {"name": "Продукт 13", "description": "Описание продукта 9", "image": "чашки.jpeg", "volumes": [(1, 150), (2, 200)]},
#         {"name": "Продукт 14", "description": "Описание продукта 10", "image": "чашки.jpeg", "volumes": [(1, 160), (2, 210)]},
#         {"name": "Продукт 15", "description": "Описание продукта 11", "image": "чашки.jpeg", "volumes": [(1, 170), (2, 220)]},
#         {"name": "Продукт 16", "description": "Описание продукта 12", "image": "чашки.jpeg", "volumes": [(1, 180), (2, 230)]},
#         {"name": "Продукт 17", "description": "Описание продукта 12", "image": "чашки.jpeg", "volumes": [(1, 180), (2, 230)]},
#         {"name": "Продукт 18", "description": "Описание продукта 12", "image": "чашки.jpeg", "volumes": [(1, 180), (2, 230)]},
#     ]
# }
#
# cart = {}
# admin_chat_id = 1159478117
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("CO2-экстракты", callback_data="group1")
#     button2 = types.InlineKeyboardButton("Эфирные масла", callback_data="group2")
#     button3 = types.InlineKeyboardButton("Воска", callback_data="group3")
#     markup.add(button1)
#     markup.add(button2)
#     markup.add(button3)
#     bot.send_message(message.chat.id, f"""<b>Добро пожаловать!</b> 🎉
#
# Здесь вы можете найти широкий ассортимент товаров, которые помогут вам сделать вашу жизнь удобнее и ярче. 🛍️
#
# Для просмотра корзины воспользуйтесь: /cart
# """, reply_markup=markup, parse_mode='HTML')
#
#
# @bot.message_handler(commands=['cart'])
# def show_cart(message):
#     user_cart = cart.get(str(message.chat.id), [])
#     if not user_cart:
#         bot.send_message(message.chat.id, "Ваша корзина пуста.")
#         return
#
#     cart_details = "Ваша корзина:\n"
#     total_price = 0
#     cart_items = []
#     for group in user_cart:
#         for i, item in enumerate(user_cart[group]):
#             product = item["product"]
#             cart_details += f"{i + 1}. {product['name']} - Объем {item['volume']} - Количество: {item['quantity']}\n"
#             total_price += item["quantity"] * product['volumes'][item["volume"] - 1][1]
#             cart_items.append(f"{i + 1}")
#
#     cart_details += f"\nОбщая стоимость: {total_price} руб."
#
#     markup = types.InlineKeyboardMarkup()
#     button_clear = types.InlineKeyboardButton("Очистить корзину", callback_data="clear_cart")
#     markup.add(button_clear)
#
#     for item_num in cart_items:
#         button_remove = types.InlineKeyboardButton(f"Удалить товар {item_num}", callback_data=f"remove_{item_num}")
#         markup.add(button_remove)
#     button2 = types.InlineKeyboardButton("Оформить", callback_data="checkout")
#     markup.add(button2)
#     bot.send_message(message.chat.id, cart_details, reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "clear_cart")
# def clear_cart(call):
#     cart[str(call.message.chat.id)] = []
#     bot.send_message(call.message.chat.id, "Ваша корзина очищена.")
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
# def remove_item(call):
#     item_num = int(call.data.split('_')[1]) - 1
#     user_cart = cart.get(str(call.message.chat.id), [])
#
#     if not user_cart:
#         bot.send_message(call.message.chat.id, "Ваша корзина пуста.")
#         return
#
#     # Удаляем товар
#     for group in user_cart:
#         if item_num < len(user_cart[group]):
#             removed_item = user_cart[group].pop(item_num)
#             bot.send_message(call.message.chat.id, f"Товар {removed_item['product']['name']} удален из корзины.")
#             break
#
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     show_cart(call.message)
#
#
# @bot.callback_query_handler(func=lambda call: call.data in ["group1", "group2", "group3"])
# def group_selected(call):
#     group = call.data
#     markup = types.InlineKeyboardMarkup()
#
#     for i, product in enumerate(products.get(group, [])):
#         button = types.InlineKeyboardButton(product['name'], callback_data=f"product_{group}_{i}")
#         markup.add(button)
#
#     back_button = types.InlineKeyboardButton("Назад к группам", callback_data="back_to_groups")
#     markup.add(back_button)
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     bot.send_message(call.message.chat.id, "Выберите продукт:", reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
# def product_selected(call):
#     group, idx = call.data.split('_')[1:3]
#     idx = int(idx)
#     product = products[group][idx]
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     markup = types.InlineKeyboardMarkup()
#
#     for vol in product['volumes']:
#         a = vol[0]
#
#
#         volume_button = types.InlineKeyboardButton(f"Объём {a}/{vol[1]} руб.",
#                                                    callback_data=f"volume_{group}_{idx}_{vol[0]}")
#         markup.add(volume_button)
#
#     back_button = types.InlineKeyboardButton("Назад", callback_data=f"back_{group}")
#     markup.add(back_button)
#
#     with open(product['image'], 'rb') as photo:
#         bot.send_photo(call.message.chat.id, photo, caption=f"{product['name']}\n{product['description']}",
#                        reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("volume_"))
# def volume_selected(call):
#     group, idx, volume = call.data.split('_')[1:7]
#     idx = int(idx)
#     volume = int(volume)
#     product = products[group][idx]
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     markup = types.InlineKeyboardMarkup(row_width=5)
#     for i in range(1, 6):
#         button = types.InlineKeyboardButton(str(i), callback_data=f"quantity_{group}_{idx}_{volume}_{i}")
#         markup.add(button)
#
#     bot.send_message(call.message.chat.id,
#                      f"Выберите количество для {product['name']}\n\nОбъем {volume} - {product['volumes'][volume - 1][1]} руб.",
#                      reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("quantity_"))
# def quantity_selected(call):
#     group, idx, volume, quantity = call.data.split('_')[1:5]
#     idx = int(idx)
#     volume = int(volume)
#     quantity = int(quantity)
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     if str(call.message.chat.id) not in cart:
#         cart[str(call.message.chat.id)] = {}
#
#     if group not in cart[str(call.message.chat.id)]:
#         cart[str(call.message.chat.id)][group] = []
#
#     cart[str(call.message.chat.id)][group].append({"product": products[group][idx], "volume": volume, "quantity": quantity})
#
#     bot.send_message(call.message.chat.id, f"Продукт добавлен в корзину: /cart.\n\nПродолжить заказ или перейти к оформлению?")
#
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("Продолжить", callback_data="back_to_groups")
#     button2 = types.InlineKeyboardButton("Оформить", callback_data="checkout")
#     markup.add(button1, button2)
#
#     bot.send_message(call.message.chat.id, "Что хотите сделать?", reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "checkout")
# def checkout(call):
#     username = call.message.from_user.username
#     if username:
#         telegram_link = f"@{username}"
#     else:
#         telegram_link = "Не указан"
#
#     bot.send_message(call.message.chat.id, "Введите ваше ФИО, которое указано на карте:")
#     bot.register_next_step_handler(call.message, get_fio, telegram_link)
#
#
# def get_fio(message, telegram_link):
#     fio = message.text
#     if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", fio):  # ФИО должно содержать только буквы и пробелы
#         bot.send_message(message.chat.id, "Пожалуйста, введите ФИО только с буквами и пробелами.")
#         bot.register_next_step_handler(message, get_fio, telegram_link)
#         return
#
#     bot.send_message(message.chat.id, "Введите ваш номер телефона:")
#     bot.register_next_step_handler(message, get_phone, fio, telegram_link)
#
#
# def get_phone(message, fio, telegram_link):
#     telegram_link = message.from_user.username
#     phone = message.text
#     if not re.match(r"^[+0-9]{10,15}$", phone):  # Телефон должен содержать только цифры и знак "+"
#         bot.send_message(message.chat.id, "Пожалуйста, введите номер телефона только с цифрами и знаком +.")
#         bot.register_next_step_handler(message, get_phone, fio, telegram_link)
#         return
#
#     order = f"Новый заказ:\nФИО: {fio}\nТелефон: {phone}\nTelegram: @{telegram_link}\n\nКорзина:\n"
#     total_price = 0
#     for group in cart[str(message.chat.id)]:
#         for item in cart[str(message.chat.id)][group]:
#             product = item["product"]
#             order += f"{product['name']} - Объем {item['volume']} - Количество: {item['quantity']}\n"
#             total_price += item["quantity"] * product['volumes'][item["volume"] - 1][1]
#
#     order += f"\nОбщая стоимость: {total_price} руб."
#
#     bot.send_message(admin_chat_id, order)
#
#     bot.send_message(message.chat.id, "Ваш заказ оформлен.🎉 \nСкоро с вами свяжется менеджер.👩‍💼\n\nИспользуйте /start, чтобы продолжить пользоваться ботом.")
#     cart.clear()
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
# def go_back(call):
#     if call.data == "back_to_groups":
#         bot.delete_message(call.message.chat.id, call.message.message_id)
#         start(call.message)
#     else:
#         group = call.data.split('_')[1]
#         group_selected(call)
#
#
# bot.polling()
#









