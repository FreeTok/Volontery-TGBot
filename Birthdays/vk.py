#!/usr/bin/env python
# coding: utf-8

# In[1]:


import vk_sender_config as key_config
import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id

import pandas as pd


key = key_config.key
vk_session = vk_api.VkApi(token=key)
Lsvk = vk_session.get_api()

def SendMessageVk(vk_id, text):
    try:
        Lsvk.messages.send(
            user_id =  vk_id,
            message = text,
            random_id = get_random_id()
            )
        return 1
    except BaseException:
        return 0


# In[4]:


#input guryanoffilya (str)
#output 226735258 (int)

#input vk.com/guryanoffilya (str)
#output 0 (int)
# - Ошибка обработки короткого имени

#Функция преобразует короткое имя в vk_id по которому можно
#отправлять сообщения

def GetIdFromShortName(short_name):
    try:
        status = vk_session.method('utils.resolveScreenName', {
            'screen_name': short_name
        })
        return status['object_id']
    except BaseException:
        return 0



#input https://vk.com/id165157643 (str)
#output 165157643 (int)

#input id165157643 (str)
#output 0 (int)
# - Ошибка обработки

#Функция преобразует ссылку vk в vk_id по которому можно
#отправлять сообщения
def GetIdFromLink(link):
    link = 'link:' + str(link)
    sep = link.split('vk.com/')
    if len(sep) > 1:
        name = sep[1]
        return GetIdFromShortName(name)  
    return 0


