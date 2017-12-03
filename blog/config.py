import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://zak:thinkful@localhost:5432/blogful"
    DEBUG = True