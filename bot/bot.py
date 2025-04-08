import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота
vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN'))
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def send_message(user_id, message):
    """Отправка сообщения пользователю"""
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0
    )

def main():
    """Основной цикл бота"""
    print("Бот запущен")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            # Получаем текст сообщения
            text = event.text.lower()
            user_id = event.user_id

            # Обработка команд
            if text == "начать":
                send_message(user_id, "Привет! Я бот ВКонтакте!")
            else:
                send_message(user_id, text)

if __name__ == "__main__":
    main()
