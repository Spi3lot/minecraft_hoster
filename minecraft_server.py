import os
import subprocess


class MinecraftServer:
    INSTANCES = {}
    FOLDER_PATH = './Minecraft'

    name: str
    process: subprocess.Popen = None

    def __init__(self, name, store_instance=True):
        self.name = name

        if store_instance:
            MinecraftServer.INSTANCES[name] = self

    def __str__(self):
        return f'MinecraftServer(name={self.name}, process={self.process})'

    def __repr__(self):
        return str(self)

    @staticmethod
    def of(name):
        instance = MinecraftServer.INSTANCES.get(name)
        return instance if instance is not None else MinecraftServer(name)

    @staticmethod
    def exit_directory():
        os.chdir('../..')

    @staticmethod
    def __subprocess_method(wait: bool):
        return subprocess.run if wait else subprocess.Popen

    @staticmethod
    def __start(wait: bool):
        return MinecraftServer.__subprocess_method(wait)(['java', '-jar', 'server.jar', 'nogui'])

    @staticmethod
    def __stop(wait: bool):
        return MinecraftServer.__subprocess_method(wait)(['java', '-jar', 'server.jar', 'stop'])

    def get_path(self):
        return f'{MinecraftServer.FOLDER_PATH}/{self.name}'

    def get_jar_path(self):
        return f'{self.get_path()}/server.jar'

    def get_properties_path(self):
        return f'{self.get_path()}/server.properties'

    def enter_directory(self):
        os.chdir(self.get_path())

    def start(self):
        self.enter_directory()

        if not os.path.exists('eula.txt'):
            self.__start(wait=True)

            with open('eula.txt', 'w') as file:
                file.write('eula=true')

        self.process = self.__start(wait=False)
        MinecraftServer.exit_directory()

    def stop(self):
        self.enter_directory()
        self.__stop(wait=False)
        MinecraftServer.exit_directory()

    def restart(self):
        self.enter_directory()
        self.__stop(wait=True)
        self.__start(wait=False)
        MinecraftServer.exit_directory()

    def get_status(self):
        self.enter_directory()
        status = subprocess.Popen(['java', '-jar', 'server.jar', 'status'],
                                  stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        MinecraftServer.exit_directory()
        return status
