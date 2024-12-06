from peewee import *

from .env_service import EnvService


class DBService:
    connection: PostgresqlDatabase

    @staticmethod
    def init():
        config = DBService.get_db_config()
        DBService.connection = PostgresqlDatabase(config["db_connect_string"])
        DBService.connection.connect()
        from .model.comment import Comment
        from .model.post import Post
        DBService.connection.create_tables([Post, Comment])
        print("Successfully connected to PostgreSQL database.")

    @staticmethod
    def get_db_config():
        return {
            "db_connect_string": "postgresql://{user}:{password}@{hostname}:{port}/{db}"
            .format(user=EnvService.env("DB_USER"),
                    password=EnvService.env("DB_PASSWORD"),
                    hostname=EnvService.env("DB_HOSTNAME"),
                    port=EnvService.env("DB_PORT"),
                    db=EnvService.env("DB_NAME")
                    )
        }