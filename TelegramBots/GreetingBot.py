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
        bot.send_message(message.chat.id, '😎🕊Привет! На связи Голубь Гриша. Именно меня ты видел на логотипе огромного Всероссийского движения "Волонтёры Победы".', reply_markup=None)
        photo = open('GolubGrisha.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, 'Чтобы отписаться, напишите в этот чат «/stop».')

        markup = types.InlineKeyboardMarkup(row_width=1)

        item1 = types.InlineKeyboardButton("Получить стикеры", url='https://t.me/addstickers/vp_PresentStickers')
        item2 = types.InlineKeyboardButton("О Волонтёрах Победы", callback_data='About')
        item3 = types.InlineKeyboardButton("Наши направления", callback_data='Directions')
        item4 = types.InlineKeyboardButton("Почему мы?", callback_data='Why')
        item5 = types.InlineKeyboardButton("Стать волонтёром", callback_data='Reg')
        item6 = types.InlineKeyboardButton("Остались вопросы?", url='https://vk.com/im?sel=-71750281')

        markup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(message.chat.id, 'Что ты хочешь узнать о нашем движении?', reply_markup=markup)

    elif message.text == '/sendall':
        bot.send_message(message.chat.id, 'Отправьте сообщение, которое будет отправленно всем')
        sendingAll.append(message.chat.id)

    elif message.text == '/stop':
        config.greetingUsers.remove(message.chat.id)
        removeUser(message.chat.id)



@bot.message_handler(content_types=['text', 'photo'])
def lalala(message):
    if message.chat.id in sendingAll:
        for chatID in config.greetingUsers:
            bot.forward_message(chatID, message.chat.id, message.message_id)

        bot.send_message(message.chat.id, 'Сообщение отправленно')

    elif message.chat.type == 'private':
        if message.text == 'О Волонтёрах Победы':
            bot.send_message(message.chat.id, f'👨‍👩‍👧Волонтеры Победы - это не просто общественное движение, а целая жизнь и семья. По всей стране и даже за рубежом налаживается связь поколений между молодежью и пожилыми людьми, большое количество молодых людей вовлекается в волонтерскую деятельность. За 7 лет в Нижегородской области было проведено более 4500 мероприятий разных тематик инаправлений. \nХочешь узнать немного подробнее?)')

        elif message.text == 'Наши направления':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Великая Победа", callback_data='1')
            item2 = types.InlineKeyboardButton("Связь Поколений", callback_data='2')
            item3 = types.InlineKeyboardButton("Моя Победа", callback_data='3')
            item4 = types.InlineKeyboardButton("Наши Победы", callback_data='4')
            item5 = types.InlineKeyboardButton("Медиа Победа", callback_data='5')
            item6 = types.InlineKeyboardButton("Моя история", callback_data='6')

            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, 'Направления Движения: \n'
                                              '\1) Великая Победа -  сопровождение Парадов Победы и Бессмертного Полка, почитание памяти героев ВОВ и др. '
                                              '\n2) Связь Поколений - помощь ветеранам ВОВ, акция "Красная Гвоздика" и др. '
                                              '\n3) Моя Победа - обучение новых волонтеров по интересной программе, приложение Skill cup и др.  '
                                              '\n4) Наши Победы - рассказ о великих подвигах в интересных форматах (Квесты, игры, квизы) '
                                              '\n5) Медиа Победа - Медиа пространство, SMM -  специалисты и тд. '
                                              '\n6) Моя история - составление семейного древа, работа с архивом.', reply_markup=markup)


        elif message.text == 'Почему мы?':
            bot.send_message(message.chat.id, 'С нами ты можешь получить:\n- Баллы при поступление в учебный заведения; \n- Есть возможность ездить на познавательные форумы в разные города; \n- Участвовать в конкурсах; \n- Создавать свои проекты \n- Получить классную атрибутику \n- Стать частью большой, дружной семьи \n- И море классных воспоминаний, опыта и позитивных эмоций; \n- А для участников(!)нашего движения младше 18 лет есть уникальная возможность попасть в топовые лагеря СТРАНЫ! 🇷🇺)')


        elif message.text == 'Назад':

            markup = types.InlineKeyboardMarkup(row_width=1)

            item1 = types.InlineKeyboardButton("Получить стикеры", url='https://t.me/addstickers/vp_PresentStickers')
            item2 = types.InlineKeyboardButton("О Волонтёрах Победы", callback_data='About')
            item3 = types.InlineKeyboardButton("Наши направления", callback_data='Directions')
            item4 = types.InlineKeyboardButton("Почему мы?", callback_data='Why')
            item5 = types.InlineKeyboardButton("Стать волонтёром", callback_data='Reg')
            item6 = types.InlineKeyboardButton("Остались вопросы?", url='https://vk.com/im?sel=-71750281')
            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, 'Что ты хочешь узнать о нашем движении?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "About":
                addStatics('About')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.InlineKeyboardButton('Назад')
                markup.add(item1)

                bot.send_message(call.message.chat.id,
                                 f'👨‍👩‍👧Волонтеры Победы - это не просто общественное движение, а целая жизнь и семья. По всей стране и даже за рубежом налаживается связь поколений между молодежью и пожилыми людьми, большое количество молодых людей вовлекается в волонтерскую деятельность. За 7 лет в Нижегородской области было проведено более 4500 мероприятий разных тематик инаправлений. \nХочешь узнать немного подробнее - смотри направления)', reply_markup=markup)

            elif call.data == "Directions":
                addStatics('Directions')
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Великая Победа", callback_data='1')
                item2 = types.InlineKeyboardButton("Связь Поколений", callback_data='2')
                item3 = types.InlineKeyboardButton("Моя Победа", callback_data='3')
                item4 = types.InlineKeyboardButton("Наши Победы", callback_data='4')
                item5 = types.InlineKeyboardButton("Медиа Победа", callback_data='5')
                item6 = types.InlineKeyboardButton("Моя история", callback_data='6')


                markup.add(item1, item2, item3, item4, item5, item6)

                directionMessages.append(bot.send_message(call.message.chat.id,
                                 'Направления Движения: \n1) Великая Победа -  сопровождение Парадов Победы и Бессмертного Полка, почитание памяти героев ВОВ и др. \n2) Связь Поколений - помощь ветеранам ВОВ, акция "Красная Гвоздика" и др. \n3) Моя Победа - обучение новых волонтеров по интересной программе, приложение Skill cup и др.  \n4) Наши Победы - рассказ о великих подвигах в интересных форматах (Квесты, игры, квизы) \n5) Медиа Победа - Медиа пространство, SMM -  специалисты и тд. \n6) Моя история - составление семейного древа, работа с архивом.',
                                                          reply_markup=markup))
                directioning.append(call.message.chat.id)

                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back1')
                markup.add(item7)
                bot.send_message(call.message.chat.id, '[Смотреть видео](https://drive.google.com/drive/folders/18CoJji7LyoVTmVbrmFT7aTk7zSlJ1gjR?usp=share_link)', parse_mode='Markdown', reply_markup=markup)



            elif call.data == "Why":
                addStatics('Why')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.InlineKeyboardButton('Назад')
                markup.add(item1)

                bot.send_message(call.message.chat.id,
                     'С нами ты можешь получить:\n- Баллы при поступление в учебный заведения; \n- Есть возможность ездить на познавательные форумы в разные города; \n- Участвовать в конкурсах; \n- Создавать свои проекты \n- Получить классную атрибутику \n- Стать частью большой, дружной семьи \n- И море классных воспоминаний, опыта и позитивных эмоций; \n- А для участников(!)нашего движения младше 18 лет есть уникальная возможность попасть в топовые лагеря СТРАНЫ! 🇷🇺)', reply_markup=markup)

            elif call.data == 'Back1':
                bot.delete_message(chat_id=call.message.chat.id, message_id=directionMessages[directioning.index(call.message.chat.id)].message_id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                # bot.edit_message_text(chat_id=call.message.chat.id, message_id=direcionMessages[direcioning.index(call.message.chat.id)].message_id,
                #     text="Направления Движения: \n1) Великая Победа -  сопровождение Парадов Победы и Бессмертного Полка, почитание памяти героев ВОВ и др. \n2) Связь Поколений - помощь ветеранам ВОВ, акция Красная Гвоздика и др. \n3) Моя Победа - обучение новых волонтеров по интересной программе, приложение Skill cup и др.  \n4) Наши Победы - рассказ о великих подвигах в интересных форматах (Квесты, игры, квизы) \n5) Медиа Победа - Медиа пространство, SMM -  специалисты и тд. \n6) Моя история - составление семейного древа, работа с архивом.",reply_markup=types.ReplyKeyboardRemove())

                directionMessages.pop(directioning.index(call.message.chat.id))
                directioning.remove(call.message.chat.id)

                markup = types.InlineKeyboardMarkup(row_width=1)

                item1 = types.InlineKeyboardButton("Получить стикеры",
                                                   url='https://t.me/addstickers/vp_PresentStickers')
                item2 = types.InlineKeyboardButton("О Волонтёрах Победы", callback_data='About')
                item3 = types.InlineKeyboardButton("Наши направления", callback_data='Directions')
                item4 = types.InlineKeyboardButton("Почему мы?", callback_data='Why')
                item5 = types.InlineKeyboardButton("Стать волонтёром", callback_data='Reg')
                item6 = types.InlineKeyboardButton("Остались вопросы?", url='https://vk.com/im?sel=-71750281')
                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id, 'Что ты хочешь узнать о нашем движении?', reply_markup=markup)

            elif call.data == 'Back2':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Великая Победа", callback_data='1')
                item2 = types.InlineKeyboardButton("Связь Поколений", callback_data='2')
                item3 = types.InlineKeyboardButton("Моя Победа", callback_data='3')
                item4 = types.InlineKeyboardButton("Наши Победы", callback_data='4')
                item5 = types.InlineKeyboardButton("Медиа Победа", callback_data='5')
                item6 = types.InlineKeyboardButton("Моя история", callback_data='6')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(call.message.chat.id,
                                 'Направления Движения: \n1) Великая Победа -  сопровождение Парадов Победы и Бессмертного Полка, почитание памяти героев ВОВ и др. \n2) Связь Поколений - помощь ветеранам ВОВ, акция "Красная Гвоздика" и др. \n3) Моя Победа - обучение новых волонтеров по интересной программе, приложение Skill cup и др.  \n4) Наши Победы - рассказ о великих подвигах в интересных форматах (Квесты, игры, квизы) \n5) Медиа Победа - Медиа пространство, SMM -  специалисты и тд. \n6) Моя история - составление семейного древа, работа с архивом.',
                                 reply_markup=markup)

                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back1')
                markup.add(item7)

                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/drive/folders/18CoJji7LyoVTmVbrmFT7aTk7zSlJ1gjR?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)
            elif call.data == "Reg":
                print('+1')
                addStatics('Become')
                if not config.reg.count(call.message.chat.id):
                    config.reg.append(call.message.chat.id)
                    print(len(config.reg))
                    bot.send_message(call.message.chat.id, '[Стать волонтёром](https://xn--90abhd2amfbbjkx2jf6f.xn--p1ai/)', parse_mode='Markdown')

            elif call.data == '1':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 '«Великая Победа» \nВ рамках направления «Великая Победа» добровольцы организовывают волонтёрское сопровождение Парадов Победы и Бессмертного Полка в городах России, благоустраивают памятные места и воинские захоронения, проводят различные всероссийские акции и проекты, такие как «Георгиевская ленточка», «Свеча памяти», «Внуки Победы» и другие.')
                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/file/d/17WzrzDzW9NuiRVvhZY0QoBPDBc4eBL3K/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)
                # bot.send_video(message.chat.id, video)

            elif call.data == '2':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 '«Связь поколений» \nДобровольцы направления «Связь поколений» проводят Всероссийскую акцию «Красная гвоздика» совместно с Благотворительным фондом «Память Поколений», помогая не только словом, но и реальным делом. Все вырученные с акции средства направляются на высокотехнологичную медицинскую помощь ветеранам.')
                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/file/d/1OQ-uvhJCsr3S3jZ0kcO5SMCdcpsm4TWc/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)

            elif call.data == '3':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 '«Моя победа» \nВ рамках этого направления доброволец учится создавать команду и управлять ею, разрабатывать и реализовывать крупные проекты, правильно использовать ресурсы и многому другому.')
                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/file/d/1RnFGvUP2wgBQwTk_kuVfPCWtlUlgVaVX/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)


            elif call.data == '4':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 '«Наши победы» \nМы рассказываем о Героях и достижениях страны через интеллектуальные игры, городские квесты, всероссийские акции.')
                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/file/d/18OBtt_Uki_Zv3pTGLO_b9zUsVAeFnpvW/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)

            elif call.data == '5':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 '«Медиапобеда» \nВолонтёры направления «Медиапобеда» занимаются производством позитивного контента: пишут статьи, снимают фото и видео, ведут группы и аккаунты в социальных сетях. Активисты создают медиапоток, несущий в себе исторические, интересные и познавательные инфоповоды.')
                video = open('video5.mp4', 'rb')
                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/file/d/1gssQR1vCcktO44fmkEdrt-KsxZP2OPxG/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)


            elif call.data == '6':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item7 = types.InlineKeyboardButton('Назад', callback_data='Back2')
                markup.add(item7)
                bot.send_message(call.message.chat.id,
                                 '«Моя история» \n«Моя история» — это первый в России проект, который не просто говорит о важности изучения истории семьи, но и даёт конкретный механизм, как это сделать с помощью волонтёров. Уже с весны 2019 года любой житель нашей страны может воспользоваться помощью добровольцев в составлении семейного древа.')
                bot.send_message(call.message.chat.id,
                                 '[Смотреть видео](https://drive.google.com/file/d/17AhdJBdDknrkE27ZjCYl-fgCzkn0bBIq/view?usp=share_link)',
                                 parse_mode='Markdown', reply_markup=markup)



    except Exception as e:
        print(repr(e))

# RUN
bot.polling(none_stop=True)