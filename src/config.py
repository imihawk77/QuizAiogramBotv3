import os

from dotenv import load_dotenv, find_dotenv
if not find_dotenv():
    exit('Переменные окружения не загружены т.к. отсутствует файл .env')
else:
    load_dotenv()
    
class Settings:
    API_TOKEN = os.getenv('API_TOKEN')

settings = Settings()