import telebot
import config
import json

from telebot import types

bot = telebot.TeleBot(config.token)

creating = []
polling = []

newevents = []
neweventsIDs = []

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, введите своё имя, фамилию, возвраст и номер телефона через пробелы".format(
                                 message.from_user, bot.get_me()),
                     parse_mode='html')
    polling.append(message.chat.id)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        # Организторам
        if len(creating) > 0:
            for id in creating:
                if id == message.chat.id:
                    newevents.append(message.text)
                    neweventsIDs.append(message.chat.id)

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton("Создать", callback_data='Create')
                    item2 = types.InlineKeyboardButton("Не создавать", callback_data='Dont create')

                    markup.add(item1, item2)

                    bot.send_message(message.chat.id, f'Создать это мероприятие?\n{message.text}', reply_markup=markup)
                    # bot.send_message(message.chat.id, f'Создать это мероприятие?\n{message}', reply_markup=markup)

                    break

        if len(polling) > 0 and len(message.text.split()) == 4:
            for id in polling:
                if id == message.chat.id:
                    info = message.text.split()
                    config.usersInfo.update({message.chat.id: {'name' : info[0], 'surname' : info[1], 'age' : info[2], 'tel' : info[3]}})

                    print(config.usersInfo)

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Я - огранизатор")
                    item2 = types.KeyboardButton("Я - волонтёр")

                    markup.add(item1, item2)

                    bot.send_message(message.chat.id, 'Отлично', reply_markup=markup)
                    # bot.send_message(message.chat.id, f'Создать это мероприятие?\n{message}', reply_markup=markup)

                    break

        elif message.text == 'Я - огранизатор':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Создать мероприятие")
            item2 = types.KeyboardButton("Мероприятия")
            item3 = types.KeyboardButton("Назад")

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Вы - организатор', reply_markup=markup)

        elif message.text == 'Создать мероприятие':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Создать мероприятие")
            item2 = types.KeyboardButton("Мероприятия")
            item3 = types.KeyboardButton("Назад")

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Напишите текст мероприятия')
            creating.append(message.chat.id)

        elif message.text == 'Мероприятия':
            if len(config.events) == 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Создать мероприятие")
                item2 = types.KeyboardButton("Мероприятия")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(message.chat.id, 'Похоже, мероприятий нет', reply_markup=markup)
                return

            for i in range(len(config.events)):
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Информация", callback_data=f'Info {i}')
                item2 = types.InlineKeyboardButton("Удалить", callback_data=f'Delete {i}')

                markup.add(item1, item2)
                bot.send_message(message.chat.id, config.events[i], reply_markup=markup)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Создать мероприятие")
            item2 = types.KeyboardButton("Мероприятия")
            item3 = types.KeyboardButton("Назад")

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Вот вся информация', reply_markup=markup)

        ##################################################################################

        elif message.text == 'Я - волонтёр':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton("Посмотреть все события")
            item2 = types.KeyboardButton("Посмотреть свои события")
            item3 = types.KeyboardButton("Назад")

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id,
                             'Поздравляю',
                             parse_mode='html', reply_markup=markup)


        elif message.text == 'Посмотреть свои события':
            if config.usersEvents.get(message.chat.id):
                for i in range(len(config.usersEvents.get(message.chat.id))):
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Отписаться", callback_data=f'Unsubscribe {i} {0}')

                    markup.add(item1)

                    bot.send_message(message.chat.id, config.usersEvents.get(message.chat.id)[i], reply_markup=markup)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                item1 = types.KeyboardButton("Посмотреть все события")
                item2 = types.KeyboardButton("Посмотреть свои события")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(message.chat.id, 'Перейти ко всем событиям?', reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                item1 = types.KeyboardButton("Посмотреть все события")
                item2 = types.KeyboardButton("Посмотреть свои события")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(message.chat.id, 'У вас ещё нет событий', reply_markup=markup)

        elif message.text == 'Посмотреть все события':
            if len(config.events) == 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                item1 = types.KeyboardButton("Посмотреть все события")
                item2 = types.KeyboardButton("Посмотреть свои события")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(message.chat.id, 'Похоже, событий нет', reply_markup=markup)
                return

            for i in range(len(config.events)):
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Подписаться", callback_data=f'Subscribe {i}')

                if (config.usersEvents.get(message.chat.id)) and (config.usersEvents.get(message.chat.id).count(config.events[i]) != 0):
                    item1 = types.InlineKeyboardButton("Отписаться", callback_data=f'Unsubscribe {i} {1}')

                markup.add(item1)
                bot.send_message(message.chat.id, config.events[i], reply_markup=markup)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton("Посмотреть все события")
            item2 = types.KeyboardButton("Посмотреть свои события")
            item3 = types.KeyboardButton("Назад")

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Перейти к вашим событиям?', reply_markup=markup)

        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Я - огранизатор")
            item2 = types.KeyboardButton("Я - волонтёр")

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Назад', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "Create" or call.data == 'Dont create':
                index = neweventsIDs.index(call.message.chat.id)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Создать мероприятие")
                item2 = types.KeyboardButton("Мероприятия")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                if call.data == "Create":
                    config.events.append(newevents[index])
                    config.adminsEvents.update({newevents[index] : []})

                    bot.send_message(call.message.chat.id, 'Новое событие создано', reply_markup=markup)

                elif call.data == "Dont create":
                    bot.send_message(call.message.chat.id, 'Бывает 😢', reply_markup=markup)

                creating.pop(index)
                newevents.pop(index)
                neweventsIDs.pop(index)

            elif str(call.data).split()[0] == 'Subscribe':
                newSubscribers = []

                if config.usersEvents.get(call.message.chat.id):
                    lastEvents = config.usersEvents.get(call.message.chat.id)

                    if lastEvents.count(config.events[int(str(call.data).split()[1])]) == 0:
                        lastEvents.append(config.events[int(str(call.data).split()[1])])
                        config.usersEvents.update({call.message.chat.id : lastEvents})

                        if config.adminsEvents.get(config.events[int(str(call.data).split()[1])]):
                            newSubscribers = config.adminsEvents.get(config.events[int(str(call.data).split()[1])])

                        newSubscribers.append(config.usersInfo.get(call.message.chat.id))
                        config.adminsEvents.update({config.events[int(str(call.data).split()[1])]: newSubscribers})

                        config.usersEvents.update(
                            {call.message.chat.id: [config.events[int(str(call.data).split()[1])]]})

                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("Посмотреть все события")
                        item2 = types.KeyboardButton("Посмотреть свои события")
                        markup.add(item1, item2)

                        bot.send_message(call.message.chat.id, f'Вы уже подписаны на это событие', reply_markup=markup)
                        return

                else:
                    if config.adminsEvents.get(config.events[int(str(call.data).split()[1])]):
                        newSubscribers = config.adminsEvents.get(config.events[int(str(call.data).split()[1])])

                    newSubscribers.append(config.usersInfo.get(call.message.chat.id))
                    config.adminsEvents.update({config.events[int(str(call.data).split()[1])]: newSubscribers})

                    config.usersEvents.update({call.message.chat.id : [config.events[int(str(call.data).split()[1])]]})

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                item1 = types.KeyboardButton("Посмотреть все события")
                item2 = types.KeyboardButton("Посмотреть свои события")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(call.message.chat.id, 'Вы подписались на новое событие', reply_markup=markup)
                print(config.adminsEvents)
                print(config.usersEvents)


            elif str(call.data).split()[0] == 'Unsubscribe':
                if config.usersEvents.get(call.message.chat.id):
                    eventToRemove = ''
                    if int(str(call.data).split()[2]) == 0:
                        eventToRemove = config.usersEvents.get(call.message.chat.id)[int(str(call.data).split()[1])]

                    elif int(str(call.data).split()[2]) == 1:
                        eventToRemove = config.events[int(str(call.data).split()[1])]

                    lastEvents = config.usersEvents.get(call.message.chat.id)

                    config.adminsEvents.get(eventToRemove).pop(config.adminsEvents.get(eventToRemove).index(config.usersInfo.get(call.message.chat.id)))
                    print(config.adminsEvents)

                    lastEvents.pop(lastEvents.index(eventToRemove))
                    config.usersEvents.update({call.message.chat.id : lastEvents})

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                item1 = types.KeyboardButton("Посмотреть все события")
                item2 = types.KeyboardButton("Посмотреть свои события")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(call.message.chat.id, f'Вы отписались от события', reply_markup=markup)

            elif str(call.data).split()[0] == 'Info':
                print(len(config.adminsEvents.get(config.events[int((str(call.data)).split()[1])])))
                if len(config.adminsEvents.get(config.events[int((str(call.data)).split()[1])])) == 0:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                    item1 = types.KeyboardButton("Создать мероприятие")
                    item2 = types.KeyboardButton("Мероприятия")
                    item3 = types.KeyboardButton("Назад")

                    markup.add(item1, item2, item3)

                    bot.send_message(call.message.chat.id, f'Похоже ещё никто не подписался на данное мероприятие', reply_markup=markup)

                people = config.adminsEvents.get(config.events[int((str(call.data)).split()[1])])

                for i in range(len(people)):
                    print(people[i])

                    name = people[i].get('name')
                    surname = people[i].get('surname')
                    age = people[i].get('age')
                    tel = people[i].get('tel')

                    bot.send_message(call.message.chat.id, f'{i+1} - {name} {surname}, {age}, {tel}')

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Создать мероприятие")
                item2 = types.KeyboardButton("Мероприятия")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(call.message.chat.id, f'Назад?', reply_markup=markup)

            elif str(call.data).split()[0] == 'Delete':
                markup = types.InlineKeyboardMarkup(row_width=1)

                item1 = types.InlineKeyboardButton("Да", callback_data=f'SuperDelete {str(call.data).split()[1]}')
                item2 = types.InlineKeyboardButton("Нет", callback_data=f'DontDelete')

                markup.add(item1, item2)

                bot.send_message(call.message.chat.id, f'Вы действительно хотите удалить {str(call.data).split()[1]}?', reply_markup=markup)

            elif str(call.data).split()[0] == 'SuperDelete':
                eventName = config.events[int(str(call.data).split()[1])]
                config.adminsEvents.pop(eventName)
                for user in config.usersEvents:
                    if config.usersEvents.get(user).count(eventName):
                        config.usersEvents.get(user).pop(config.usersEvents.get(user).index(eventName))

                config.events.remove(eventName)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Создать мероприятие")
                item2 = types.KeyboardButton("Мероприятия")
                item3 = types.KeyboardButton("Назад")

                markup.add(item1, item2, item3)

                bot.send_message(call.message.chat.id, f'Мероприятие удалено', reply_markup=markup)

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)