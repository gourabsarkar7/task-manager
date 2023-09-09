import os
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv(dotenv_path='/Users/anirudh.chawla/python_django/task-management-django/taskmanagement/.env.dev')

class Config: 
    DEFAULT_PORT = os.getenv('DEFAULT_PORT')
    DEBUG = os.getenv('DEBUG')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
