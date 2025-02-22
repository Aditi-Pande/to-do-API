import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:Mysql%40123@db:3306/task1")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
