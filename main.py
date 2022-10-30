from email import message
from catalog import cart_Main_Item,cart_Main_Name
import telebot
from telebot import types
import emoji
import openpyxl

bot = telebot.TeleBot('5413159629:AAHieK0bNLkm339Y53OMzPF5-jmJCOwZfW8',parse_mode='Markdown')

admins = [1413828191,]
joinedFile = open('joined.txt','r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

cart = [] # корзина
setOfProd = []
prodStatus = False
fromCart = False
price_Main = 0 # итоговая цена в корзине
txt123 =  ""
proverka = 0
item1=types.KeyboardButton('Записаться')
item2=types.KeyboardButton('Контакты')
mainMenu = [item1,item2]

def extract_arg(arg):
    arg = arg[1:]
    return arg

@bot.message_handler(commands=["start"])
def start(m, res=False):
        global mainMenu
        if not str(m.chat.id) in joinedUsers:
            joinedFile = open('joined.txt','a')
            joinedFile.write(str(m.chat.id) +'\n')
            joinedUsers.add(m.chat.id)

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(mainMenu[0],mainMenu[1])
        bot.send_sticker(m.chat.id, 'CAACAgIAAxkBAAEQzXBiyXiYI-aPg0pXuxfmRxCT8XUGGwAC9AwAAsmkKUqt14TvU6ZpwykE')
        bot.send_message(m.chat.id, 'Нажми: \nЗаписаться — для онлайн записи\nКонтакты — для контактной информации ',  reply_markup=markup)



@bot.message_handler(commands=['entry','contacts','catalog','cart','send'])
def handle_text(message):
    status = extract_arg(message.text)
    if status == 'entry':

          bot.send_message(message.from_user.id, "Введите имя(ФИО):", reply_markup=types.ReplyKeyboardRemove())
          bot.register_next_step_handler(message, get_name)

    elif status == 'contacts':
            answer = emoji.emojize(":house:")+"- г. Тюмень, ул. Рижская, д. 72 корп.3 \n " + emoji.emojize(":telephone:")+" - 89505103231"
            bot.send_message(message.chat.id, answer)
            bot.send_message(message.chat.id,"<a href='http://ab72.ru/'>Перейти на сайт</a>", parse_mode='HTML')
    elif status == 'catalog':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text='Просмотр каталога', callback_data='CATA')
        keyboard.add(key_1) #добавляем кнопку в клавиатуру
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAESfQFjTZyGo5xVPC3VXjVv0kN0Qonn-wACfAADLEIhDMHqBHJjFv4PKgQ')
        bot.send_message(message.chat.id,'Наш товар к вашим услугам:',reply_markup=keyboard)
    elif status == 'cart':
        global cart
        global price_Main
        global cart_Main_Item
        global cart_Main_Name
        for a in cart:
            msg = str(cart_Main_Name[a])+'-'+ str(cart_Main_Item.get(cart_Main_Name[a]))+'₽\n'
            bot.send_message(message.chat.id,msg)
            msg = ''
        msg2 = 'Итог: '+str(price_Main)+'₽'
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='Очистка корзины', callback_data='CLEAR')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Оформление заказа', callback_data='PAID')
        keyboard.add(key_2)
        bot.send_message(message.chat.id,msg2,reply_markup=keyboard) 
    elif status[0:4] == 'send':
        command_sender = message.from_user.id
        if command_sender in admins:
            with open(r'joined.txt') as ids:
                for line in ids:
                    user_id = int(line.strip("\n"))
                    try:
                        command = 'Важная информация от фирмы:' + message.text.split(maxsplit=1)[1]
                        bot.send_sticker(user_id, 'CAACAgIAAxkBAAESg_ljUCMli_inY5Zr7w9WHZnoLZwvEgACvB8AAs4wwEkg6Xo5Q0HNoCoE')
                        bot.send_message(user_id, command)
                    except Exception as e:
                        bot.send_message(command_sender, f'ошибка отправки сообщения юзеру - {user_id}')
        else:
            bot.send_message(command_sender, f'у вас нет прав для запуска команды')

            

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.strip() == 'Записаться' :

          bot.send_message(message.from_user.id, "Введите имя(ФИО):", reply_markup=types.ReplyKeyboardRemove())
          bot.register_next_step_handler(message, get_name)

    elif message.text.strip() == 'Контакты':
            answer = emoji.emojize(":house:")+"- г. Тюмень, ул. Рижская, д. 72 корп.3 \n " + emoji.emojize(":telephone:")+" - 89505103231"
            bot.send_message(message.chat.id, answer)
            bot.send_message(message.chat.id,"<a href='http://ab72.ru/'>Перейти на сайт</a>", parse_mode='HTML')

@bot.message_handler(content_types=['text'])
def get_name(message):
    if message.text.strip() == 'Контакты':
        bot.register_next_step_handler(message, start)
    global txt123
    global FN
    FN = message.text.strip()
    if  proverka == 1:
        txt123 = ''
    txt123 += 'ФИО:'
    txt123 += message.text
    txt123 += ' \n'
    bot.send_message(message.from_user.id, "Введите номер:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_num)

@bot.message_handler(content_types=['text'])
def get_num(message):
    global NUMB
    global fromCart
    # test_1 = int(message.text.strip())
    NUMB = message.text.strip()
    if message.text.strip() == 'Контакты':
        bot.register_next_step_handler(message, start)
    global txt123
    txt123 += 'Номер:'
    txt123 += message.text
    txt123 += " \n"
    if fromCart == False:
        bot.send_message(message.from_user.id, "Введите услугу:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_serv)
    elif fromCart == True:
        bot.send_message(message.from_user.id, "Введите услугу:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_serv)


def get_serv(message):
    if message.text.strip() == 'Контакты':
        bot.register_next_step_handler(message, start)
    global txt123
    global SN
    global cart
    global price_Main
    global cart_Main_Item
    global cart_Main_Name
    global setOfProd
    if fromCart == False:
        SN = message.text.strip()
        txt123 += 'Услуга:'
        txt123 += message.text
        txt123 += " \n"
        emsg = "Заявка составлена: \n" + txt123+ " \n(Отправить заявку? Да/Нет)"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.row(item1,item2)
        bot.send_message(message.from_user.id, emsg ,reply_markup=markup)
    elif fromCart == True:
        for a in cart:
            msg = str(cart_Main_Name[a])+'-'+ str(cart_Main_Item.get(cart_Main_Name[a]))+'₽'
            setOfProd.append(msg)
        msg2 = 'Итог: '+str(price_Main)+'₽'
        setOfProd.append(msg2)
        for a in setOfProd:
            SN+=a
            SN+=' '
        emsg = "Заявка составлена:\n(Отправить заявку? Да/Нет)"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.row(item1,item2)
        bot.send_message(message.from_user.id, emsg ,reply_markup=markup)
    bot.register_next_step_handler(message, ending)


def ending(message):
    global txt123
    global prodStatus
    global fromCart
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(mainMenu[0],mainMenu[1])
    if message.text.strip() == 'Контакты':
        bot.register_next_step_handler(message, start)
    if message.text.strip() == 'Нет':
         proverka = 1
         txt123 = ''
         bot.send_message(message.from_user.id, "Ваша заявка отменена",reply_markup=markup)
         bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAESSJFjOuHAujA7SXKr790cUj2tgStt-AACIgEAAixCIQzD75jbbLDogCoE')
         bot.register_next_step_handler(message, start)

    if message.text.strip() == 'Да':

        doc = openpyxl.load_workbook(filename='Data.xlsx')
        sheet = doc['INFO']

        rows = (
            (FN, NUMB,SN),
        )

        for row in rows:
            sheet.append(row)
        doc.save('Data.xlsx')
        txt123 = ''
        ans2 = "Благодарим за обращение, надемся мы смогли решить ваш вопрос"
        bot.send_message(message.from_user.id, ans2)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEQzYZiyXrR7d6drGl_cxub4lOtKJn2xQAC5g4AAkFyKEraBMBMl5EVaSkE',reply_markup=markup)
    txt123 = ''
    prodStatus = False
    fromCart = False


# метод обработчик
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global cart
    global price_Main
    global cart_Main_Item
    global cart_Main_Name
    global fromCart
    global prodStatus
    if call.data =='CATA':
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='BLUETOOTH адаптеры / FM модуляторы', callback_data='BLUE')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Акустика', callback_data='AKU')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Кабель AUX / USB / VIDEO', callback_data='CAB')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='ПОДОГРЕВЫ / ОТОПИТЕЛИ / АВТОТЕПЛО', callback_data='POD')
        keyboard.add(key_4)
        bot.send_photo(call.message.chat.id,open('avtMAIN.png', 'rb'),reply_markup=keyboard)
    elif call.data == 'CLEAR':
        cart = []
        price_Main = 0
    elif call.data == 'PAID':
        fromCart = True
        prodStatus = True
        # bot.register_next_step_handler(call.message, handle_text)
    elif call.data == "BLUE": #call.data это callback_data, которую мы указали при объявлении кнопки
       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_1 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show1')
       keyboard.add(key_1) 
       msg = cart_Main_Name[1]+'-'+str(cart_Main_Item[cart_Main_Name[1]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_2 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show2')
       keyboard.add(key_2) 
       msg = cart_Main_Name[2]+'-'+str(cart_Main_Item[cart_Main_Name[2]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_3 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show3')
       keyboard.add(key_3) 
       back = types.InlineKeyboardButton(text='НАЗАД В КАТАЛОГ', callback_data='CATA')
       keyboard.add(back)
       msg = cart_Main_Name[3]+'-'+str(cart_Main_Item[cart_Main_Name[3]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard) 
#/////////////////////////////
    elif call.data == 'show1':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add1')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='BLUE')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/1.jpeg','rb'))
        msg = cart_Main_Name[1]+'-'+str(cart_Main_Item[cart_Main_Name[1]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add1':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(1)
        back = types.InlineKeyboardButton(text='Назад', callback_data='BLUE')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[1]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show2':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add2')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='BLUE')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/2.jpeg','rb'))
        msg = cart_Main_Name[2]+'-'+str(cart_Main_Item[cart_Main_Name[2]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add2':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(2)
        back = types.InlineKeyboardButton(text='Назад', callback_data='BLUE')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[2]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show3':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add3')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='BLUE')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/3.jpeg','rb'))
        msg = cart_Main_Name[3]+'-'+str(cart_Main_Item[cart_Main_Name[3]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add3':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(3)
        back = types.InlineKeyboardButton(text='Назад', callback_data='BLUE')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[3]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')
    

    elif call.data == "AKU": #call.data это callback_data, которую мы указали при объявлении кнопки
       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_1 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show21')
       keyboard.add(key_1) 
       msg = cart_Main_Name[4]+'-'+str(cart_Main_Item[cart_Main_Name[4]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_2 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show22')
       keyboard.add(key_2) 
       msg = cart_Main_Name[5]+'-'+str(cart_Main_Item[cart_Main_Name[5]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_3 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show23')
       keyboard.add(key_3) 
       back = types.InlineKeyboardButton(text='НАЗАД В КАТАЛОГ', callback_data='CATA')
       keyboard.add(back) 
       msg = cart_Main_Name[6]+'-'+str(cart_Main_Item[cart_Main_Name[6]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
       
#/////////////////////////////
    elif call.data == 'show21':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add21')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='AKU')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/4.jpeg','rb'))
        msg = cart_Main_Name[4]+'-'+str(cart_Main_Item[cart_Main_Name[4]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add21':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(4)
        back = types.InlineKeyboardButton(text='Назад', callback_data='AKU')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[4]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show22':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add22')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='AKU')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/5.jpeg','rb'))
        msg = cart_Main_Name[5]+'-'+str(cart_Main_Item[cart_Main_Name[5]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add22':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(5)
        back = types.InlineKeyboardButton(text='Назад', callback_data='AKU')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[5]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show23':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add23')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='AKU')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/6.jpeg','rb'))
        msg = cart_Main_Name[6]+'-'+str(cart_Main_Item[cart_Main_Name[6]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add23':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(6)
        back = types.InlineKeyboardButton(text='Назад', callback_data='AKU')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[6]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

#//////////////////////////////////////
    elif call.data == "CAB": #call.data это callback_data, которую мы указали при объявлении кнопки
       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_1 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show31')
       keyboard.add(key_1) 
       msg = cart_Main_Name[7]+'-'+str(cart_Main_Item[cart_Main_Name[7]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_2 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show32')
       keyboard.add(key_2) 
       msg = cart_Main_Name[8]+'-'+str(cart_Main_Item[cart_Main_Name[8]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_3 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show33')
       keyboard.add(key_3) 
       back = types.InlineKeyboardButton(text='НАЗАД В КАТАЛОГ', callback_data='CATA')
       keyboard.add(back) 
       msg = cart_Main_Name[9]+'-'+str(cart_Main_Item[cart_Main_Name[9]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
       
#/////////////////////////////
    elif call.data == 'show31':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add31')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='CAB')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/7.png','rb'))
        msg = cart_Main_Name[7]+'-'+str(cart_Main_Item[cart_Main_Name[7]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add31':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(7)
        back = types.InlineKeyboardButton(text='Назад', callback_data='CAB')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[7]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show32':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add32')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='CAB')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/8.jpeg','rb'))
        msg = cart_Main_Name[8]+'-'+str(cart_Main_Item[cart_Main_Name[8]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add32':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(8)
        back = types.InlineKeyboardButton(text='Назад', callback_data='CAB')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[8]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show33':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add33')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='CAB')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/9.jpeg','rb'))
        msg = cart_Main_Name[9]+'-'+str(cart_Main_Item[cart_Main_Name[9]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add33':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(9)
        back = types.InlineKeyboardButton(text='Назад', callback_data='CAB')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[9]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')
#//////////////////////////////////////
    elif call.data == "POD": #call.data это callback_data, которую мы указали при объявлении кнопки
       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_1 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show41')
       keyboard.add(key_1) 
       msg = cart_Main_Name[10]+'-'+str(cart_Main_Item[cart_Main_Name[10]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_2 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show42')
       keyboard.add(key_2) 
       msg = cart_Main_Name[11]+'-'+str(cart_Main_Item[cart_Main_Name[11]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)

       keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
       key_3 = types.InlineKeyboardButton(text = 'Просмотр', callback_data ='show43')
       keyboard.add(key_3) 
       back = types.InlineKeyboardButton(text='НАЗАД В КАТАЛОГ', callback_data='CATA')
       keyboard.add(back) 
       msg = cart_Main_Name[12]+'-'+str(cart_Main_Item[cart_Main_Name[12]])+'₽;\n'
       bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
       
#/////////////////////////////
    elif call.data == 'show41':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add41')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='POD')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/10.jpeg','rb'))
        msg = cart_Main_Name[10]+'-'+str(cart_Main_Item[cart_Main_Name[10]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add41':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(10)
        back = types.InlineKeyboardButton(text='Назад', callback_data='POD')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[10]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show42':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add42')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='POD')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/11.jpeg','rb'))
        msg = cart_Main_Name[11]+'-'+str(cart_Main_Item[cart_Main_Name[11]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add42':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(11)
        back = types.InlineKeyboardButton(text='Назад', callback_data='POD')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[11]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')

    elif call.data == 'show43':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_1 = types.InlineKeyboardButton(text = 'Добавить в корзину', callback_data ='add43')
        keyboard.add(key_1) 
        back = types.InlineKeyboardButton(text='Назад', callback_data='POD')
        keyboard.add(back) 
        bot.send_photo(call.message.chat.id,open('img/12.jpeg','rb'))
        msg = cart_Main_Name[12]+'-'+str(cart_Main_Item[cart_Main_Name[12]])+'₽;\n'
        bot.send_message(call.message.chat.id,msg,reply_markup=keyboard)
    elif call.data == 'add43':
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        cart.append(12)
        back = types.InlineKeyboardButton(text='Назад', callback_data='POD')
        keyboard.add(back) 
        price_Main += cart_Main_Item[cart_Main_Name[12]]
        bot.send_message(call.message.chat.id,'Добавлено!',parse_mode='Markdown')
#//////////////////////////////////////
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True,interval=0)
    except Exception as e:
        pass
bot.polling(none_stop=True, interval=0)