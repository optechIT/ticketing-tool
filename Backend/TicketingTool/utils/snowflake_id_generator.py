from snowflake import SnowflakeGenerator

from django.conf import settings



class SnowflakeIDGenerator:
    def __init__(self):
        self.instance  = settings.SNOWFLAKE_INSTANCE
        self.epoch  = settings.SNOWFLAKE_EPOCH

        self.generator = SnowflakeGenerator(instance = self.instance, epoch = self.epoch, )


    def generate_id(self):
        return next(self.generator)