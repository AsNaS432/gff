from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные окружения

from flask_cors import CORS
from gigachat import GigaChat
import time

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от фронтенда

API_KEY = os.getenv("API_KEY")  # Получаем API_KEY из переменной окружения

def find_answer(user_message):
    # Обновленная логика поиска с более лояльными ответами
    knowledge_base = {
        "гарантия": "Конечно! Мы предоставляем гарантию от 3 до 6 месяцев в зависимости от компонента.",
        "заказ сегодня": "Да, вы можете получить заказ сегодня при самовывозе и наличии на складе.",
        "оригинал": "Все оригинальные запчасти имеют серийный номер Apple, чтобы вы могли быть уверены в их качестве.",
        "возврат": "Да, у нас есть возможность возврата в течение 14 дней при сохранении упаковки и чека.",
        "предоплата": "Нет, вам не нужно делать предоплату. Оплата производится только при получении заказа.",
        "доставка": "Мы предлагаем несколько способов доставки: самовывоз, курьерская доставка (1-2 дня) и СДЭК (2-3 дня)."
    }
    
    # Приведение сообщения к нижнему регистру для поиска
    user_message = user_message.lower()
    
    # Поиск ответа по ключевым словам
    for keyword, answer in knowledge_base.items():
        if keyword in user_message:
            return answer
    
    return "Если у вас есть дополнительные вопросы, не стесняйтесь связаться с нашим менеджером!"

GREETING = """Добрый день! Вас приветствует MYTOOLSSHOP. 
Мы специализируемся на оригинальных и совместимых запчастях для техники Apple.
🕒 Режим работы: ежедневно 9:00-21:00
📞 Контактный телефон: +7 (495) XXX-XX-XX
📍 Адрес самовывоза: Москва, ул. Запчастная, 15 (метро "Детализация")

Чем могу помочь?"""

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Если это первое сообщение, отправляем приветствие
    if user_message.lower() == "привет" or user_message.lower() == "здравствуйте":
        reply = GREETING
    else:
        # Поиск ответа в базе знаний
        reply = find_answer(user_message)
    
    return jsonify({
        'success': True,
        'reply': reply
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
