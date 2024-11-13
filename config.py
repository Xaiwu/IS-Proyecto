import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_secreto')