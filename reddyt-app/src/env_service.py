from environs import Env

class EnvService:
    env: Env
    @staticmethod
    def init():
        EnvService.env = Env()
        EnvService.env.read_env('local.env', False)
