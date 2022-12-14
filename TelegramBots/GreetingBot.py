import telebot
import config
import datetime

from telebot import types

bot = telebot.TeleBot(config.GreetingBotToken)

directionMessages = []
directioning = []

sendingAll = []

#sql
import sqlite3 as sql
conUsers = sql.connect('Users.db', check_same_thread=False)
conStat = sql.connect('Stat.db', check_same_thread=False)

def addUser(id):
    date = str(datetime.date.today())
    with conUsers:
        cur = conUsers.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `Users` (`id` STRING, `Date` STRING)")

        cur.execute("SELECT * FROM `Users`")
        rows = cur.fetchall()
        for row in rows:
            print(row[0])
            if row[0] == id:
                return

        cur.execute(f"INSERT INTO `Users` VALUES ('{id}', '{date}')")

        conUsers.commit()
        cur.close()

def removeUser(id):
    try:
        sqliteConnection = sql.connect('Users.db')
        cursor = sqliteConnection.cursor()

        # Deleting single record now
        sql_delete_query = f"""DELETE from Users where id = {id}"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sql.Error as error:
        print("Failed to delete record from sqlite table", error)

def addStatics(stat):
    with conStat:
        cur = conStat.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `Stat` (`Stickers` INT, `About` INT, `Directions` INT, `Why` INT, "
                    "`Become` INT, `Questions` INT)")

        cur.execute(f"SELECT `{stat}` FROM `Stat`")
        actual = cur.fetchall()[0][0]

        cur.execute(f"""
        UPDATE
          `Stat`
        SET
          `{stat}` = {actual + 1}
        """)

        conStat.commit()
        cur.close()


@bot.message_handler(commands=['start', 'sendall', 'stop'])
def commands(message):
    if message.text == '/start':
        addUser(message.chat.id)

        config.greetingUsers.append(message.chat.id)
        bot.send_message(message.chat.id, 'ππΠΡΠΈΠ²Π΅Ρ! ΠΠ° ΡΠ²ΡΠ·ΠΈ ΠΠΎΠ»ΡΠ±Ρ ΠΡΠΈΡΠ°. ΠΠΌΠ΅Π½Π½ΠΎ ΠΌΠ΅Π½Ρ ΡΡ Π²ΠΈΠ΄Π΅Π» Π½Π° Π»ΠΎΠ³ΠΎΡΠΈΠΏΠ΅ ΠΎΠ³ΡΠΎΠΌΠ½ΠΎΠ³ΠΎ ΠΡΠ΅ΡΠΎΡΡΠΈΠΉΡΠΊΠΎΠ³ΠΎ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΡ "ΠΠΎΠ»ΠΎΠ½ΡΡΡΡ ΠΠΎΠ±Π΅Π΄Ρ".', reply_markup=None)
        photo = open('GolubGrisha.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, 'Π§ΡΠΎΠ±Ρ ΠΎΡΠΏΠΈΡΠ°ΡΡΡΡ, Π½Π°ΠΏΠΈΡΠΈΡΠ΅ Π² ΡΡΠΎΡ ΡΠ°Ρ Β«/stopΒ».')

        markup = types.InlineKeyboardMarkup(row_width=1)

        item1 = types.InlineKeyboardButton("ΠΠΎΠ»ΡΡΠΈΡΡ ΡΡΠΈΠΊΠ΅ΡΡ", url='https://t.me/addstickers/vp_PresentStickers')
        item2 = types.InlineKeyboardButton("Π ΠΠΎΠ»ΠΎΠ½ΡΡΡΠ°Ρ ΠΠΎΠ±Π΅Π΄Ρ", callback_data='About')
        item3 = types.InlineKeyboardButton("ΠΠ°ΡΠΈ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ", callback_data='Directions')
        item4 = types.InlineKeyboardButton("ΠΠΎΡΠ΅ΠΌΡ ΠΌΡ?", callback_data='Why')
        item5 = types.InlineKeyboardButton("Π‘ΡΠ°ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΡΡΠΎΠΌ", callback_data='Reg')
        item6 = types.InlineKeyboardButton("ΠΡΡΠ°Π»ΠΈΡΡ Π²ΠΎΠΏΡΠΎΡΡ?", url='https://vk.com/im?sel=-71750281')

        markup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(message.chat.id, 'Π§ΡΠΎ ΡΡ ΡΠΎΡΠ΅ΡΡ ΡΠ·Π½Π°ΡΡ ΠΎ Π½Π°ΡΠ΅ΠΌ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΠΈ?', reply_markup=markup)

    elif message.text == '/sendall':
        bot.send_message(message.chat.id, 'ΠΡΠΏΡΠ°Π²ΡΡΠ΅ ΡΠΎΠΎΠ±ΡΠ΅Π½ΠΈΠ΅, ΠΊΠΎΡΠΎΡΠΎΠ΅ Π±ΡΠ΄Π΅Ρ ΠΎΡΠΏΡΠ°Π²Π»Π΅Π½Π½ΠΎ Π²ΡΠ΅ΠΌ')
        sendingAll.append(message.chat.id)

    elif message.text == '/stop':
        config.greetingUsers.remove(message.chat.id)
        removeUser(message.chat.id)



@bot.message_handler(content_types=['text', 'photo'])
def lalala(message):
    if message.chat.id in sendingAll:
        for chatID in config.greetingUsers:
            bot.forward_message(chatID, message.chat.id, message.message_id)

        bot.send_message(message.chat.id, 'Π‘ΠΎΠΎΠ±ΡΠ΅Π½ΠΈΠ΅ ΠΎΡΠΏΡΠ°Π²Π»Π΅Π½Π½ΠΎ')

    elif message.chat.type == 'private':
        if message.text == 'Π ΠΠΎΠ»ΠΎΠ½ΡΡΡΠ°Ρ ΠΠΎΠ±Π΅Π΄Ρ':
            bot.send_message(message.chat.id, f'π¨βπ©βπ§ΠΠΎΠ»ΠΎΠ½ΡΠ΅ΡΡ ΠΠΎΠ±Π΅Π΄Ρ - ΡΡΠΎ Π½Π΅ ΠΏΡΠΎΡΡΠΎ ΠΎΠ±ΡΠ΅ΡΡΠ²Π΅Π½Π½ΠΎΠ΅ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΠ΅, Π° ΡΠ΅Π»Π°Ρ ΠΆΠΈΠ·Π½Ρ ΠΈ ΡΠ΅ΠΌΡΡ. ΠΠΎ Π²ΡΠ΅ΠΉ ΡΡΡΠ°Π½Π΅ ΠΈ Π΄Π°ΠΆΠ΅ Π·Π° ΡΡΠ±Π΅ΠΆΠΎΠΌ Π½Π°Π»Π°ΠΆΠΈΠ²Π°Π΅ΡΡΡ ΡΠ²ΡΠ·Ρ ΠΏΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ ΠΌΠ΅ΠΆΠ΄Ρ ΠΌΠΎΠ»ΠΎΠ΄Π΅ΠΆΡΡ ΠΈ ΠΏΠΎΠΆΠΈΠ»ΡΠΌΠΈ Π»ΡΠ΄ΡΠΌΠΈ, Π±ΠΎΠ»ΡΡΠΎΠ΅ ΠΊΠΎΠ»ΠΈΡΠ΅ΡΡΠ²ΠΎ ΠΌΠΎΠ»ΠΎΠ΄ΡΡ Π»ΡΠ΄Π΅ΠΉ Π²ΠΎΠ²Π»Π΅ΠΊΠ°Π΅ΡΡΡ Π² Π²ΠΎΠ»ΠΎΠ½ΡΠ΅ΡΡΠΊΡΡ Π΄Π΅ΡΡΠ΅Π»ΡΠ½ΠΎΡΡΡ. ΠΠ° 7 Π»Π΅Ρ Π² ΠΠΈΠΆΠ΅Π³ΠΎΡΠΎΠ΄ΡΠΊΠΎΠΉ ΠΎΠ±Π»Π°ΡΡΠΈ Π±ΡΠ»ΠΎ ΠΏΡΠΎΠ²Π΅Π΄Π΅Π½ΠΎ Π±ΠΎΠ»Π΅Π΅ 4500 ΠΌΠ΅ΡΠΎΠΏΡΠΈΡΡΠΈΠΉ ΡΠ°Π·Π½ΡΡ ΡΠ΅ΠΌΠ°ΡΠΈΠΊ ΠΈΠ½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΠΉ. \nΠ₯ΠΎΡΠ΅ΡΡ ΡΠ·Π½Π°ΡΡ Π½Π΅ΠΌΠ½ΠΎΠ³ΠΎ ΠΏΠΎΠ΄ΡΠΎΠ±Π½Π΅Π΅?)')

        elif message.text == 'ΠΠ°ΡΠΈ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π°", callback_data='1')
            item2 = types.InlineKeyboardButton("Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ", callback_data='2')
            item3 = types.InlineKeyboardButton("ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π°", callback_data='3')
            item4 = types.InlineKeyboardButton("ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ", callback_data='4')
            item5 = types.InlineKeyboardButton("ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π°", callback_data='5')
            item6 = types.InlineKeyboardButton("ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ", callback_data='6')

            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, 'ΠΠ°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ ΠΠ²ΠΈΠΆΠ΅Π½ΠΈΡ: \n'
                                              '\1) ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π° -  ΡΠΎΠΏΡΠΎΠ²ΠΎΠΆΠ΄Π΅Π½ΠΈΠ΅ ΠΠ°ΡΠ°Π΄ΠΎΠ² ΠΠΎΠ±Π΅Π΄Ρ ΠΈ ΠΠ΅ΡΡΠΌΠ΅ΡΡΠ½ΠΎΠ³ΠΎ ΠΠΎΠ»ΠΊΠ°, ΠΏΠΎΡΠΈΡΠ°Π½ΠΈΠ΅ ΠΏΠ°ΠΌΡΡΠΈ Π³Π΅ΡΠΎΠ΅Π² ΠΠΠ ΠΈ Π΄Ρ. '
                                              '\n2) Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ - ΠΏΠΎΠΌΠΎΡΡ Π²Π΅ΡΠ΅ΡΠ°Π½Π°ΠΌ ΠΠΠ, Π°ΠΊΡΠΈΡ "ΠΡΠ°ΡΠ½Π°Ρ ΠΠ²ΠΎΠ·Π΄ΠΈΠΊΠ°" ΠΈ Π΄Ρ. '
                                              '\n3) ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π° - ΠΎΠ±ΡΡΠ΅Π½ΠΈΠ΅ Π½ΠΎΠ²ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΠ΅ΡΠΎΠ² ΠΏΠΎ ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΠΎΠΉ ΠΏΡΠΎΠ³ΡΠ°ΠΌΠΌΠ΅, ΠΏΡΠΈΠ»ΠΎΠΆΠ΅Π½ΠΈΠ΅ Skill cup ΠΈ Π΄Ρ.  '
                                              '\n4) ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ - ΡΠ°ΡΡΠΊΠ°Π· ΠΎ Π²Π΅Π»ΠΈΠΊΠΈΡ ΠΏΠΎΠ΄Π²ΠΈΠ³Π°Ρ Π² ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΡΡ ΡΠΎΡΠΌΠ°ΡΠ°Ρ (ΠΠ²Π΅ΡΡΡ, ΠΈΠ³ΡΡ, ΠΊΠ²ΠΈΠ·Ρ) '
                                              '\n5) ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π° - ΠΠ΅Π΄ΠΈΠ° ΠΏΡΠΎΡΡΡΠ°Π½ΡΡΠ²ΠΎ, SMM -  ΡΠΏΠ΅ΡΠΈΠ°Π»ΠΈΡΡΡ ΠΈ ΡΠ΄. '
                                              '\n6) ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ - ΡΠΎΡΡΠ°Π²Π»Π΅Π½ΠΈΠ΅ ΡΠ΅ΠΌΠ΅ΠΉΠ½ΠΎΠ³ΠΎ Π΄ΡΠ΅Π²Π°, ΡΠ°Π±ΠΎΡΠ° Ρ Π°ΡΡΠΈΠ²ΠΎΠΌ.', reply_markup=markup)


        elif message.text == 'ΠΠΎΡΠ΅ΠΌΡ ΠΌΡ?':
            bot.send_message(message.chat.id, 'Π‘ Π½Π°ΠΌΠΈ ΡΡ ΠΌΠΎΠΆΠ΅ΡΡ ΠΏΠΎΠ»ΡΡΠΈΡΡ:\n- ΠΠ°Π»Π»Ρ ΠΏΡΠΈ ΠΏΠΎΡΡΡΠΏΠ»Π΅Π½ΠΈΠ΅ Π² ΡΡΠ΅Π±Π½ΡΠΉ Π·Π°Π²Π΅Π΄Π΅Π½ΠΈΡ; \n- ΠΡΡΡ Π²ΠΎΠ·ΠΌΠΎΠΆΠ½ΠΎΡΡΡ Π΅Π·Π΄ΠΈΡΡ Π½Π° ΠΏΠΎΠ·Π½Π°Π²Π°ΡΠ΅Π»ΡΠ½ΡΠ΅ ΡΠΎΡΡΠΌΡ Π² ΡΠ°Π·Π½ΡΠ΅ Π³ΠΎΡΠΎΠ΄Π°; \n- Π£ΡΠ°ΡΡΠ²ΠΎΠ²Π°ΡΡ Π² ΠΊΠΎΠ½ΠΊΡΡΡΠ°Ρ; \n- Π‘ΠΎΠ·Π΄Π°Π²Π°ΡΡ ΡΠ²ΠΎΠΈ ΠΏΡΠΎΠ΅ΠΊΡΡ \n- ΠΠΎΠ»ΡΡΠΈΡΡ ΠΊΠ»Π°ΡΡΠ½ΡΡ Π°ΡΡΠΈΠ±ΡΡΠΈΠΊΡ \n- Π‘ΡΠ°ΡΡ ΡΠ°ΡΡΡΡ Π±ΠΎΠ»ΡΡΠΎΠΉ, Π΄ΡΡΠΆΠ½ΠΎΠΉ ΡΠ΅ΠΌΡΠΈ \n- Π ΠΌΠΎΡΠ΅ ΠΊΠ»Π°ΡΡΠ½ΡΡ Π²ΠΎΡΠΏΠΎΠΌΠΈΠ½Π°Π½ΠΈΠΉ, ΠΎΠΏΡΡΠ° ΠΈ ΠΏΠΎΠ·ΠΈΡΠΈΠ²Π½ΡΡ ΡΠΌΠΎΡΠΈΠΉ; \n- Π Π΄Π»Ρ ΡΡΠ°ΡΡΠ½ΠΈΠΊΠΎΠ²(!)Π½Π°ΡΠ΅Π³ΠΎ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΡ ΠΌΠ»Π°Π΄ΡΠ΅ 18 Π»Π΅Ρ Π΅ΡΡΡ ΡΠ½ΠΈΠΊΠ°Π»ΡΠ½Π°Ρ Π²ΠΎΠ·ΠΌΠΎΠΆΠ½ΠΎΡΡΡ ΠΏΠΎΠΏΠ°ΡΡΡ Π² ΡΠΎΠΏΠΎΠ²ΡΠ΅ Π»Π°Π³Π΅ΡΡ Π‘Π’Π ΠΠΠ«! π·πΊ)')


        elif message.text == 'ΠΠ°Π·Π°Π΄':

            markup = types.InlineKeyboardMarkup(row_width=1)

            item1 = types.InlineKeyboardButton("ΠΠΎΠ»ΡΡΠΈΡΡ ΡΡΠΈΠΊΠ΅ΡΡ", url='https://t.me/addstickers/vp_PresentStickers')
            item2 = types.InlineKeyboardButton("Π ΠΠΎΠ»ΠΎΠ½ΡΡΡΠ°Ρ ΠΠΎΠ±Π΅Π΄Ρ", callback_data='About')
            item3 = types.InlineKeyboardButton("ΠΠ°ΡΠΈ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ", callback_data='Directions')
            item4 = types.InlineKeyboardButton("ΠΠΎΡΠ΅ΠΌΡ ΠΌΡ?", callback_data='Why')
            item5 = types.InlineKeyboardButton("Π‘ΡΠ°ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΡΡΠΎΠΌ", callback_data='Reg')
            item6 = types.InlineKeyboardButton("ΠΡΡΠ°Π»ΠΈΡΡ Π²ΠΎΠΏΡΠΎΡΡ?", url='https://vk.com/im?sel=-71750281')
            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, 'Π§ΡΠΎ ΡΡ ΡΠΎΡΠ΅ΡΡ ΡΠ·Π½Π°ΡΡ ΠΎ Π½Π°ΡΠ΅ΠΌ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΠΈ?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "About":
                addStatics('About')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄')
                markup.add(item1)

                bot.send_message(call.message.chat.id,
                                 f'π¨βπ©βπ§ΠΠΎΠ»ΠΎΠ½ΡΠ΅ΡΡ ΠΠΎΠ±Π΅Π΄Ρ - ΡΡΠΎ Π½Π΅ ΠΏΡΠΎΡΡΠΎ ΠΎΠ±ΡΠ΅ΡΡΠ²Π΅Π½Π½ΠΎΠ΅ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΠ΅, Π° ΡΠ΅Π»Π°Ρ ΠΆΠΈΠ·Π½Ρ ΠΈ ΡΠ΅ΠΌΡΡ. ΠΠΎ Π²ΡΠ΅ΠΉ ΡΡΡΠ°Π½Π΅ ΠΈ Π΄Π°ΠΆΠ΅ Π·Π° ΡΡΠ±Π΅ΠΆΠΎΠΌ Π½Π°Π»Π°ΠΆΠΈΠ²Π°Π΅ΡΡΡ ΡΠ²ΡΠ·Ρ ΠΏΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ ΠΌΠ΅ΠΆΠ΄Ρ ΠΌΠΎΠ»ΠΎΠ΄Π΅ΠΆΡΡ ΠΈ ΠΏΠΎΠΆΠΈΠ»ΡΠΌΠΈ Π»ΡΠ΄ΡΠΌΠΈ, Π±ΠΎΠ»ΡΡΠΎΠ΅ ΠΊΠΎΠ»ΠΈΡΠ΅ΡΡΠ²ΠΎ ΠΌΠΎΠ»ΠΎΠ΄ΡΡ Π»ΡΠ΄Π΅ΠΉ Π²ΠΎΠ²Π»Π΅ΠΊΠ°Π΅ΡΡΡ Π² Π²ΠΎΠ»ΠΎΠ½ΡΠ΅ΡΡΠΊΡΡ Π΄Π΅ΡΡΠ΅Π»ΡΠ½ΠΎΡΡΡ. ΠΠ° 7 Π»Π΅Ρ Π² ΠΠΈΠΆΠ΅Π³ΠΎΡΠΎΠ΄ΡΠΊΠΎΠΉ ΠΎΠ±Π»Π°ΡΡΠΈ Π±ΡΠ»ΠΎ ΠΏΡΠΎΠ²Π΅Π΄Π΅Π½ΠΎ Π±ΠΎΠ»Π΅Π΅ 4500 ΠΌΠ΅ΡΠΎΠΏΡΠΈΡΡΠΈΠΉ ΡΠ°Π·Π½ΡΡ ΡΠ΅ΠΌΠ°ΡΠΈΠΊ ΠΈΠ½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΠΉ. \nΠ₯ΠΎΡΠ΅ΡΡ ΡΠ·Π½Π°ΡΡ Π½Π΅ΠΌΠ½ΠΎΠ³ΠΎ ΠΏΠΎΠ΄ΡΠΎΠ±Π½Π΅Π΅ - ΡΠΌΠΎΡΡΠΈ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ)', reply_markup=markup)

            elif call.data == "Directions":
                addStatics('Directions')
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π°", callback_data='1')
                item2 = types.InlineKeyboardButton("Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ", callback_data='2')
                item3 = types.InlineKeyboardButton("ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π°", callback_data='3')
                item4 = types.InlineKeyboardButton("ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ", callback_data='4')
                item5 = types.InlineKeyboardButton("ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π°", callback_data='5')
                item6 = types.InlineKeyboardButton("ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ", callback_data='6')


                markup.add(item1, item2, item3, item4, item5, item6)

                directionMessages.append(bot.send_message(call.message.chat.id,
                                 'ΠΠ°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ ΠΠ²ΠΈΠΆΠ΅Π½ΠΈΡ: \n1) ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π° -  ΡΠΎΠΏΡΠΎΠ²ΠΎΠΆΠ΄Π΅Π½ΠΈΠ΅ ΠΠ°ΡΠ°Π΄ΠΎΠ² ΠΠΎΠ±Π΅Π΄Ρ ΠΈ ΠΠ΅ΡΡΠΌΠ΅ΡΡΠ½ΠΎΠ³ΠΎ ΠΠΎΠ»ΠΊΠ°, ΠΏΠΎΡΠΈΡΠ°Π½ΠΈΠ΅ ΠΏΠ°ΠΌΡΡΠΈ Π³Π΅ΡΠΎΠ΅Π² ΠΠΠ ΠΈ Π΄Ρ. \n2) Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ - ΠΏΠΎΠΌΠΎΡΡ Π²Π΅ΡΠ΅ΡΠ°Π½Π°ΠΌ ΠΠΠ, Π°ΠΊΡΠΈΡ "ΠΡΠ°ΡΠ½Π°Ρ ΠΠ²ΠΎΠ·Π΄ΠΈΠΊΠ°" ΠΈ Π΄Ρ. \n3) ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π° - ΠΎΠ±ΡΡΠ΅Π½ΠΈΠ΅ Π½ΠΎΠ²ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΠ΅ΡΠΎΠ² ΠΏΠΎ ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΠΎΠΉ ΠΏΡΠΎΠ³ΡΠ°ΠΌΠΌΠ΅, ΠΏΡΠΈΠ»ΠΎΠΆΠ΅Π½ΠΈΠ΅ Skill cup ΠΈ Π΄Ρ.  \n4) ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ - ΡΠ°ΡΡΠΊΠ°Π· ΠΎ Π²Π΅Π»ΠΈΠΊΠΈΡ ΠΏΠΎΠ΄Π²ΠΈΠ³Π°Ρ Π² ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΡΡ ΡΠΎΡΠΌΠ°ΡΠ°Ρ (ΠΠ²Π΅ΡΡΡ, ΠΈΠ³ΡΡ, ΠΊΠ²ΠΈΠ·Ρ) \n5) ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π° - ΠΠ΅Π΄ΠΈΠ° ΠΏΡΠΎΡΡΡΠ°Π½ΡΡΠ²ΠΎ, SMM -  ΡΠΏΠ΅ΡΠΈΠ°Π»ΠΈΡΡΡ ΠΈ ΡΠ΄. \n6) ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ - ΡΠΎΡΡΠ°Π²Π»Π΅Π½ΠΈΠ΅ ΡΠ΅ΠΌΠ΅ΠΉΠ½ΠΎΠ³ΠΎ Π΄ΡΠ΅Π²Π°, ΡΠ°Π±ΠΎΡΠ° Ρ Π°ΡΡΠΈΠ²ΠΎΠΌ.',
                                                          reply_markup=markup))
                directioning.append(call.message.chat.id)

                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back1')
                markup.add(item7)
                bot.send_message(call.message.chat.id, '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/drive/folders/18CoJji7LyoVTmVbrmFT7aTk7zSlJ1gjR?usp=share_link)', parse_mode='Markdown', reply_markup=markup)



            elif call.data == "Why":
                addStatics('Why')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄')
                markup.add(item1)

                bot.send_message(call.message.chat.id,
                     'Π‘ Π½Π°ΠΌΠΈ ΡΡ ΠΌΠΎΠΆΠ΅ΡΡ ΠΏΠΎΠ»ΡΡΠΈΡΡ:\n- ΠΠ°Π»Π»Ρ ΠΏΡΠΈ ΠΏΠΎΡΡΡΠΏΠ»Π΅Π½ΠΈΠ΅ Π² ΡΡΠ΅Π±Π½ΡΠΉ Π·Π°Π²Π΅Π΄Π΅Π½ΠΈΡ; \n- ΠΡΡΡ Π²ΠΎΠ·ΠΌΠΎΠΆΠ½ΠΎΡΡΡ Π΅Π·Π΄ΠΈΡΡ Π½Π° ΠΏΠΎΠ·Π½Π°Π²Π°ΡΠ΅Π»ΡΠ½ΡΠ΅ ΡΠΎΡΡΠΌΡ Π² ΡΠ°Π·Π½ΡΠ΅ Π³ΠΎΡΠΎΠ΄Π°; \n- Π£ΡΠ°ΡΡΠ²ΠΎΠ²Π°ΡΡ Π² ΠΊΠΎΠ½ΠΊΡΡΡΠ°Ρ; \n- Π‘ΠΎΠ·Π΄Π°Π²Π°ΡΡ ΡΠ²ΠΎΠΈ ΠΏΡΠΎΠ΅ΠΊΡΡ \n- ΠΠΎΠ»ΡΡΠΈΡΡ ΠΊΠ»Π°ΡΡΠ½ΡΡ Π°ΡΡΠΈΠ±ΡΡΠΈΠΊΡ \n- Π‘ΡΠ°ΡΡ ΡΠ°ΡΡΡΡ Π±ΠΎΠ»ΡΡΠΎΠΉ, Π΄ΡΡΠΆΠ½ΠΎΠΉ ΡΠ΅ΠΌΡΠΈ \n- Π ΠΌΠΎΡΠ΅ ΠΊΠ»Π°ΡΡΠ½ΡΡ Π²ΠΎΡΠΏΠΎΠΌΠΈΠ½Π°Π½ΠΈΠΉ, ΠΎΠΏΡΡΠ° ΠΈ ΠΏΠΎΠ·ΠΈΡΠΈΠ²Π½ΡΡ ΡΠΌΠΎΡΠΈΠΉ; \n- Π Π΄Π»Ρ ΡΡΠ°ΡΡΠ½ΠΈΠΊΠΎΠ²(!)Π½Π°ΡΠ΅Π³ΠΎ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΡ ΠΌΠ»Π°Π΄ΡΠ΅ 18 Π»Π΅Ρ Π΅ΡΡΡ ΡΠ½ΠΈΠΊΠ°Π»ΡΠ½Π°Ρ Π²ΠΎΠ·ΠΌΠΎΠΆΠ½ΠΎΡΡΡ ΠΏΠΎΠΏΠ°ΡΡΡ Π² ΡΠΎΠΏΠΎΠ²ΡΠ΅ Π»Π°Π³Π΅ΡΡ Π‘Π’Π ΠΠΠ«! π·πΊ)', reply_markup=markup)

            elif call.data == 'Back1':
                bot.delete_message(chat_id=call.message.chat.id, message_id=directionMessages[directioning.index(call.message.chat.id)].message_id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                # bot.edit_message_text(chat_id=call.message.chat.id, message_id=direcionMessages[direcioning.index(call.message.chat.id)].message_id,
                #     text="ΠΠ°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ ΠΠ²ΠΈΠΆΠ΅Π½ΠΈΡ: \n1) ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π° -  ΡΠΎΠΏΡΠΎΠ²ΠΎΠΆΠ΄Π΅Π½ΠΈΠ΅ ΠΠ°ΡΠ°Π΄ΠΎΠ² ΠΠΎΠ±Π΅Π΄Ρ ΠΈ ΠΠ΅ΡΡΠΌΠ΅ΡΡΠ½ΠΎΠ³ΠΎ ΠΠΎΠ»ΠΊΠ°, ΠΏΠΎΡΠΈΡΠ°Π½ΠΈΠ΅ ΠΏΠ°ΠΌΡΡΠΈ Π³Π΅ΡΠΎΠ΅Π² ΠΠΠ ΠΈ Π΄Ρ. \n2) Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ - ΠΏΠΎΠΌΠΎΡΡ Π²Π΅ΡΠ΅ΡΠ°Π½Π°ΠΌ ΠΠΠ, Π°ΠΊΡΠΈΡ ΠΡΠ°ΡΠ½Π°Ρ ΠΠ²ΠΎΠ·Π΄ΠΈΠΊΠ° ΠΈ Π΄Ρ. \n3) ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π° - ΠΎΠ±ΡΡΠ΅Π½ΠΈΠ΅ Π½ΠΎΠ²ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΠ΅ΡΠΎΠ² ΠΏΠΎ ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΠΎΠΉ ΠΏΡΠΎΠ³ΡΠ°ΠΌΠΌΠ΅, ΠΏΡΠΈΠ»ΠΎΠΆΠ΅Π½ΠΈΠ΅ Skill cup ΠΈ Π΄Ρ.  \n4) ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ - ΡΠ°ΡΡΠΊΠ°Π· ΠΎ Π²Π΅Π»ΠΈΠΊΠΈΡ ΠΏΠΎΠ΄Π²ΠΈΠ³Π°Ρ Π² ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΡΡ ΡΠΎΡΠΌΠ°ΡΠ°Ρ (ΠΠ²Π΅ΡΡΡ, ΠΈΠ³ΡΡ, ΠΊΠ²ΠΈΠ·Ρ) \n5) ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π° - ΠΠ΅Π΄ΠΈΠ° ΠΏΡΠΎΡΡΡΠ°Π½ΡΡΠ²ΠΎ, SMM -  ΡΠΏΠ΅ΡΠΈΠ°Π»ΠΈΡΡΡ ΠΈ ΡΠ΄. \n6) ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ - ΡΠΎΡΡΠ°Π²Π»Π΅Π½ΠΈΠ΅ ΡΠ΅ΠΌΠ΅ΠΉΠ½ΠΎΠ³ΠΎ Π΄ΡΠ΅Π²Π°, ΡΠ°Π±ΠΎΡΠ° Ρ Π°ΡΡΠΈΠ²ΠΎΠΌ.",reply_markup=types.ReplyKeyboardRemove())

                directionMessages.pop(directioning.index(call.message.chat.id))
                directioning.remove(call.message.chat.id)

                markup = types.InlineKeyboardMarkup(row_width=1)

                item1 = types.InlineKeyboardButton("ΠΠΎΠ»ΡΡΠΈΡΡ ΡΡΠΈΠΊΠ΅ΡΡ",
                                                   url='https://t.me/addstickers/vp_PresentStickers')
                item2 = types.InlineKeyboardButton("Π ΠΠΎΠ»ΠΎΠ½ΡΡΡΠ°Ρ ΠΠΎΠ±Π΅Π΄Ρ", callback_data='About')
                item3 = types.InlineKeyboardButton("ΠΠ°ΡΠΈ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ", callback_data='Directions')
                item4 = types.InlineKeyboardButton("ΠΠΎΡΠ΅ΠΌΡ ΠΌΡ?", callback_data='Why')
                item5 = types.InlineKeyboardButton("Π‘ΡΠ°ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΡΡΠΎΠΌ", callback_data='Reg')
                item6 = types.InlineKeyboardButton("ΠΡΡΠ°Π»ΠΈΡΡ Π²ΠΎΠΏΡΠΎΡΡ?", url='https://vk.com/im?sel=-71750281')
                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, 'Π§ΡΠΎ ΡΡ ΡΠΎΡΠ΅ΡΡ ΡΠ·Π½Π°ΡΡ ΠΎ Π½Π°ΡΠ΅ΠΌ Π΄Π²ΠΈΠΆΠ΅Π½ΠΈΠΈ?', reply_markup=markup)

            elif call.data == 'Back2':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π°", callback_data='1')
                item2 = types.InlineKeyboardButton("Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ", callback_data='2')
                item3 = types.InlineKeyboardButton("ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π°", callback_data='3')
                item4 = types.InlineKeyboardButton("ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ", callback_data='4')
                item5 = types.InlineKeyboardButton("ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π°", callback_data='5')
                item6 = types.InlineKeyboardButton("ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ", callback_data='6')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id,
                                 'ΠΠ°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ ΠΠ²ΠΈΠΆΠ΅Π½ΠΈΡ: \n1) ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π° -  ΡΠΎΠΏΡΠΎΠ²ΠΎΠΆΠ΄Π΅Π½ΠΈΠ΅ ΠΠ°ΡΠ°Π΄ΠΎΠ² ΠΠΎΠ±Π΅Π΄Ρ ΠΈ ΠΠ΅ΡΡΠΌΠ΅ΡΡΠ½ΠΎΠ³ΠΎ ΠΠΎΠ»ΠΊΠ°, ΠΏΠΎΡΠΈΡΠ°Π½ΠΈΠ΅ ΠΏΠ°ΠΌΡΡΠΈ Π³Π΅ΡΠΎΠ΅Π² ΠΠΠ ΠΈ Π΄Ρ. \n2) Π‘Π²ΡΠ·Ρ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉ - ΠΏΠΎΠΌΠΎΡΡ Π²Π΅ΡΠ΅ΡΠ°Π½Π°ΠΌ ΠΠΠ, Π°ΠΊΡΠΈΡ "ΠΡΠ°ΡΠ½Π°Ρ ΠΠ²ΠΎΠ·Π΄ΠΈΠΊΠ°" ΠΈ Π΄Ρ. \n3) ΠΠΎΡ ΠΠΎΠ±Π΅Π΄Π° - ΠΎΠ±ΡΡΠ΅Π½ΠΈΠ΅ Π½ΠΎΠ²ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΠ΅ΡΠΎΠ² ΠΏΠΎ ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΠΎΠΉ ΠΏΡΠΎΠ³ΡΠ°ΠΌΠΌΠ΅, ΠΏΡΠΈΠ»ΠΎΠΆΠ΅Π½ΠΈΠ΅ Skill cup ΠΈ Π΄Ρ.  \n4) ΠΠ°ΡΠΈ ΠΠΎΠ±Π΅Π΄Ρ - ΡΠ°ΡΡΠΊΠ°Π· ΠΎ Π²Π΅Π»ΠΈΠΊΠΈΡ ΠΏΠΎΠ΄Π²ΠΈΠ³Π°Ρ Π² ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΡΡ ΡΠΎΡΠΌΠ°ΡΠ°Ρ (ΠΠ²Π΅ΡΡΡ, ΠΈΠ³ΡΡ, ΠΊΠ²ΠΈΠ·Ρ) \n5) ΠΠ΅Π΄ΠΈΠ° ΠΠΎΠ±Π΅Π΄Π° - ΠΠ΅Π΄ΠΈΠ° ΠΏΡΠΎΡΡΡΠ°Π½ΡΡΠ²ΠΎ, SMM -  ΡΠΏΠ΅ΡΠΈΠ°Π»ΠΈΡΡΡ ΠΈ ΡΠ΄. \n6) ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡ - ΡΠΎΡΡΠ°Π²Π»Π΅Π½ΠΈΠ΅ ΡΠ΅ΠΌΠ΅ΠΉΠ½ΠΎΠ³ΠΎ Π΄ΡΠ΅Π²Π°, ΡΠ°Π±ΠΎΡΠ° Ρ Π°ΡΡΠΈΠ²ΠΎΠΌ.',
                                 reply_markup=markup)

                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back1')
                markup.add(item7)

                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/drive/folders/18CoJji7LyoVTmVbrmFT7aTk7zSlJ1gjR?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)
            elif call.data == "Reg":
                print('+1')
                addStatics('Become')
                if not config.reg.count(call.message.chat.id):
                    config.reg.append(call.message.chat.id)
                    print(len(config.reg))
                    bot.send_message(call.message.chat.id, '[Π‘ΡΠ°ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΡΡΠΎΠΌ](https://xn--90abhd2amfbbjkx2jf6f.xn--p1ai/)', parse_mode='Markdown')

            elif call.data == '1':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 'Β«ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π°Β» \nΠ ΡΠ°ΠΌΠΊΠ°Ρ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ Β«ΠΠ΅Π»ΠΈΠΊΠ°Ρ ΠΠΎΠ±Π΅Π΄Π°Β» Π΄ΠΎΠ±ΡΠΎΠ²ΠΎΠ»ΡΡΡ ΠΎΡΠ³Π°Π½ΠΈΠ·ΠΎΠ²ΡΠ²Π°ΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΡΡΡΠΊΠΎΠ΅ ΡΠΎΠΏΡΠΎΠ²ΠΎΠΆΠ΄Π΅Π½ΠΈΠ΅ ΠΠ°ΡΠ°Π΄ΠΎΠ² ΠΠΎΠ±Π΅Π΄Ρ ΠΈ ΠΠ΅ΡΡΠΌΠ΅ΡΡΠ½ΠΎΠ³ΠΎ ΠΠΎΠ»ΠΊΠ° Π² Π³ΠΎΡΠΎΠ΄Π°Ρ Π ΠΎΡΡΠΈΠΈ, Π±Π»Π°Π³ΠΎΡΡΡΡΠ°ΠΈΠ²Π°ΡΡ ΠΏΠ°ΠΌΡΡΠ½ΡΠ΅ ΠΌΠ΅ΡΡΠ° ΠΈ Π²ΠΎΠΈΠ½ΡΠΊΠΈΠ΅ Π·Π°ΡΠΎΡΠΎΠ½Π΅Π½ΠΈΡ, ΠΏΡΠΎΠ²ΠΎΠ΄ΡΡ ΡΠ°Π·Π»ΠΈΡΠ½ΡΠ΅ Π²ΡΠ΅ΡΠΎΡΡΠΈΠΉΡΠΊΠΈΠ΅ Π°ΠΊΡΠΈΠΈ ΠΈ ΠΏΡΠΎΠ΅ΠΊΡΡ, ΡΠ°ΠΊΠΈΠ΅ ΠΊΠ°ΠΊ Β«ΠΠ΅ΠΎΡΠ³ΠΈΠ΅Π²ΡΠΊΠ°Ρ Π»Π΅Π½ΡΠΎΡΠΊΠ°Β», Β«Π‘Π²Π΅ΡΠ° ΠΏΠ°ΠΌΡΡΠΈΒ», Β«ΠΠ½ΡΠΊΠΈ ΠΠΎΠ±Π΅Π΄ΡΒ» ΠΈ Π΄ΡΡΠ³ΠΈΠ΅.')
                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/file/d/17WzrzDzW9NuiRVvhZY0QoBPDBc4eBL3K/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)
                # bot.send_video(message.chat.id, video)

            elif call.data == '2':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 'Β«Π‘Π²ΡΠ·Ρ ΠΏΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉΒ» \nΠΠΎΠ±ΡΠΎΠ²ΠΎΠ»ΡΡΡ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ Β«Π‘Π²ΡΠ·Ρ ΠΏΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉΒ» ΠΏΡΠΎΠ²ΠΎΠ΄ΡΡ ΠΡΠ΅ΡΠΎΡΡΠΈΠΉΡΠΊΡΡ Π°ΠΊΡΠΈΡ Β«ΠΡΠ°ΡΠ½Π°Ρ Π³Π²ΠΎΠ·Π΄ΠΈΠΊΠ°Β» ΡΠΎΠ²ΠΌΠ΅ΡΡΠ½ΠΎ Ρ ΠΠ»Π°Π³ΠΎΡΠ²ΠΎΡΠΈΡΠ΅Π»ΡΠ½ΡΠΌ ΡΠΎΠ½Π΄ΠΎΠΌ Β«ΠΠ°ΠΌΡΡΡ ΠΠΎΠΊΠΎΠ»Π΅Π½ΠΈΠΉΒ», ΠΏΠΎΠΌΠΎΠ³Π°Ρ Π½Π΅ ΡΠΎΠ»ΡΠΊΠΎ ΡΠ»ΠΎΠ²ΠΎΠΌ, Π½ΠΎ ΠΈ ΡΠ΅Π°Π»ΡΠ½ΡΠΌ Π΄Π΅Π»ΠΎΠΌ. ΠΡΠ΅ Π²ΡΡΡΡΠ΅Π½Π½ΡΠ΅ Ρ Π°ΠΊΡΠΈΠΈ ΡΡΠ΅Π΄ΡΡΠ²Π° Π½Π°ΠΏΡΠ°Π²Π»ΡΡΡΡΡ Π½Π° Π²ΡΡΠΎΠΊΠΎΡΠ΅ΡΠ½ΠΎΠ»ΠΎΠ³ΠΈΡΠ½ΡΡ ΠΌΠ΅Π΄ΠΈΡΠΈΠ½ΡΠΊΡΡ ΠΏΠΎΠΌΠΎΡΡ Π²Π΅ΡΠ΅ΡΠ°Π½Π°ΠΌ.')
                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/file/d/1OQ-uvhJCsr3S3jZ0kcO5SMCdcpsm4TWc/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)

            elif call.data == '3':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 'Β«ΠΠΎΡ ΠΏΠΎΠ±Π΅Π΄Π°Β» \nΠ ΡΠ°ΠΌΠΊΠ°Ρ ΡΡΠΎΠ³ΠΎ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ Π΄ΠΎΠ±ΡΠΎΠ²ΠΎΠ»Π΅Ρ ΡΡΠΈΡΡΡ ΡΠΎΠ·Π΄Π°Π²Π°ΡΡ ΠΊΠΎΠΌΠ°Π½Π΄Ρ ΠΈ ΡΠΏΡΠ°Π²Π»ΡΡΡ Π΅Ρ, ΡΠ°Π·ΡΠ°Π±Π°ΡΡΠ²Π°ΡΡ ΠΈ ΡΠ΅Π°Π»ΠΈΠ·ΠΎΠ²ΡΠ²Π°ΡΡ ΠΊΡΡΠΏΠ½ΡΠ΅ ΠΏΡΠΎΠ΅ΠΊΡΡ, ΠΏΡΠ°Π²ΠΈΠ»ΡΠ½ΠΎ ΠΈΡΠΏΠΎΠ»ΡΠ·ΠΎΠ²Π°ΡΡ ΡΠ΅ΡΡΡΡΡ ΠΈ ΠΌΠ½ΠΎΠ³ΠΎΠΌΡ Π΄ΡΡΠ³ΠΎΠΌΡ.')
                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/file/d/1RnFGvUP2wgBQwTk_kuVfPCWtlUlgVaVX/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)


            elif call.data == '4':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 'Β«ΠΠ°ΡΠΈ ΠΏΠΎΠ±Π΅Π΄ΡΒ» \nΠΡ ΡΠ°ΡΡΠΊΠ°Π·ΡΠ²Π°Π΅ΠΌ ΠΎ ΠΠ΅ΡΠΎΡΡ ΠΈ Π΄ΠΎΡΡΠΈΠΆΠ΅Π½ΠΈΡΡ ΡΡΡΠ°Π½Ρ ΡΠ΅ΡΠ΅Π· ΠΈΠ½ΡΠ΅Π»Π»Π΅ΠΊΡΡΠ°Π»ΡΠ½ΡΠ΅ ΠΈΠ³ΡΡ, Π³ΠΎΡΠΎΠ΄ΡΠΊΠΈΠ΅ ΠΊΠ²Π΅ΡΡΡ, Π²ΡΠ΅ΡΠΎΡΡΠΈΠΉΡΠΊΠΈΠ΅ Π°ΠΊΡΠΈΠΈ.')
                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/file/d/18OBtt_Uki_Zv3pTGLO_b9zUsVAeFnpvW/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)

            elif call.data == '5':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 'Β«ΠΠ΅Π΄ΠΈΠ°ΠΏΠΎΠ±Π΅Π΄Π°Β» \nΠΠΎΠ»ΠΎΠ½ΡΡΡΡ Π½Π°ΠΏΡΠ°Π²Π»Π΅Π½ΠΈΡ Β«ΠΠ΅Π΄ΠΈΠ°ΠΏΠΎΠ±Π΅Π΄Π°Β» Π·Π°Π½ΠΈΠΌΠ°ΡΡΡΡ ΠΏΡΠΎΠΈΠ·Π²ΠΎΠ΄ΡΡΠ²ΠΎΠΌ ΠΏΠΎΠ·ΠΈΡΠΈΠ²Π½ΠΎΠ³ΠΎ ΠΊΠΎΠ½ΡΠ΅Π½ΡΠ°: ΠΏΠΈΡΡΡ ΡΡΠ°ΡΡΠΈ, ΡΠ½ΠΈΠΌΠ°ΡΡ ΡΠΎΡΠΎ ΠΈ Π²ΠΈΠ΄Π΅ΠΎ, Π²Π΅Π΄ΡΡ Π³ΡΡΠΏΠΏΡ ΠΈ Π°ΠΊΠΊΠ°ΡΠ½ΡΡ Π² ΡΠΎΡΠΈΠ°Π»ΡΠ½ΡΡ ΡΠ΅ΡΡΡ. ΠΠΊΡΠΈΠ²ΠΈΡΡΡ ΡΠΎΠ·Π΄Π°ΡΡ ΠΌΠ΅Π΄ΠΈΠ°ΠΏΠΎΡΠΎΠΊ, Π½Π΅ΡΡΡΠΈΠΉ Π² ΡΠ΅Π±Π΅ ΠΈΡΡΠΎΡΠΈΡΠ΅ΡΠΊΠΈΠ΅, ΠΈΠ½ΡΠ΅ΡΠ΅ΡΠ½ΡΠ΅ ΠΈ ΠΏΠΎΠ·Π½Π°Π²Π°ΡΠ΅Π»ΡΠ½ΡΠ΅ ΠΈΠ½ΡΠΎΠΏΠΎΠ²ΠΎΠ΄Ρ.')
                video = open('video5.mp4', 'rb')
                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/file/d/1gssQR1vCcktO44fmkEdrt-KsxZP2OPxG/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)


            elif call.data == '6':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('ΠΠ°Π·Π°Π΄', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 'Β«ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡΒ» \nΒ«ΠΠΎΡ ΠΈΡΡΠΎΡΠΈΡΒ» β ΡΡΠΎ ΠΏΠ΅ΡΠ²ΡΠΉ Π² Π ΠΎΡΡΠΈΠΈ ΠΏΡΠΎΠ΅ΠΊΡ, ΠΊΠΎΡΠΎΡΡΠΉ Π½Π΅ ΠΏΡΠΎΡΡΠΎ Π³ΠΎΠ²ΠΎΡΠΈΡ ΠΎ Π²Π°ΠΆΠ½ΠΎΡΡΠΈ ΠΈΠ·ΡΡΠ΅Π½ΠΈΡ ΠΈΡΡΠΎΡΠΈΠΈ ΡΠ΅ΠΌΡΠΈ, Π½ΠΎ ΠΈ Π΄Π°ΡΡ ΠΊΠΎΠ½ΠΊΡΠ΅ΡΠ½ΡΠΉ ΠΌΠ΅ΡΠ°Π½ΠΈΠ·ΠΌ, ΠΊΠ°ΠΊ ΡΡΠΎ ΡΠ΄Π΅Π»Π°ΡΡ Ρ ΠΏΠΎΠΌΠΎΡΡΡ Π²ΠΎΠ»ΠΎΠ½ΡΡΡΠΎΠ². Π£ΠΆΠ΅ Ρ Π²Π΅ΡΠ½Ρ 2019 Π³ΠΎΠ΄Π° Π»ΡΠ±ΠΎΠΉ ΠΆΠΈΡΠ΅Π»Ρ Π½Π°ΡΠ΅ΠΉ ΡΡΡΠ°Π½Ρ ΠΌΠΎΠΆΠ΅Ρ Π²ΠΎΡΠΏΠΎΠ»ΡΠ·ΠΎΠ²Π°ΡΡΡΡ ΠΏΠΎΠΌΠΎΡΡΡ Π΄ΠΎΠ±ΡΠΎΠ²ΠΎΠ»ΡΡΠ΅Π² Π² ΡΠΎΡΡΠ°Π²Π»Π΅Π½ΠΈΠΈ ΡΠ΅ΠΌΠ΅ΠΉΠ½ΠΎΠ³ΠΎ Π΄ΡΠ΅Π²Π°.')
                bot.send_message(call.message.chat.id,
                                 '[Π‘ΠΌΠΎΡΡΠ΅ΡΡ Π²ΠΈΠ΄Π΅ΠΎ](https://drive.google.com/file/d/17AhdJBdDknrkE27ZjCYl-fgCzkn0bBIq/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)



    except Exception as e:
        print(repr(e))

# RUN
bot.polling(none_stop=True)