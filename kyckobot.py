# Кыцкобот v1
# Компрометирует всё, что видит
# Предназначен для троллинга
# (c) aGrIk Software, 2020. Licensed by GPL v3

##########CONFIG##########
token = "Ваш токен ВКонтакте. Сгенерируйте на https://vkhost.github.io от приложения Kate Mobile (это важно!)"
##########CONFIG##########

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import sys
import traceback

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
impostors = []
why = "Ай, упал: *Споткнулся: ".split("*")

def getname(uid):
    unamee = vk.users.get(user_id=uid)[0]
    return unamee["first_name"] + " " + unamee["last_name"]
    
print("Модули подгружены, авторизация завершена успешно. Кыцкобот v1 начинает свою работу.")

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_group:
            obj = vk.messages.getById(message_ids=[event.message_id])['items'][0]
            user_id = obj["from_id"]
            peer_id = obj["peer_id"]
            text = str(obj['text'])
            if event.from_me:
                if text == "/" and 'reply_message' in obj.keys():
                    if obj['reply_message']['from_id'] not in impostors: 
                        impostors.append(obj['reply_message']['from_id'])
                        print(getname(obj['reply_message']['from_id']) + " (" + str(obj['reply_message']['from_id']) + ") теперь под пристальной слежкой ФСБ!")
                    else: 
                        impostors.remove(obj['reply_message']['from_id'])
                        print(getname(obj['reply_message']['from_id']) + " (" + str(obj['reply_message']['from_id']) + ") снят из под слежки! Но однажды придёт день...")
                    vk.messages.delete(message_ids=event.message_id, delete_for_all=1)
                    
            else:
                if user_id in impostors:
                    if user_id != peer_id: print(getname(user_id) + " (" + str(user_id) + ") посмел высказаться в чате " + str(peer_id) + ". ФСБ такого не прощает!")
                    else: print(getname(user_id) + " (" + str(user_id) + ") посмел высказаться в личных сообщениях. ФСБ такого не прощает!")
                    vk.messages.send(peer_id=peer_id,
                    message=".",
                    reply_to=event.message_id,
                    random_id=random.randint(-2147483647, 2147483647))
                  
except Exception as e:
    print(random.choice(why) + str(e))
