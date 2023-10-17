import os
import subprocess


class MinecraftServer:
    INSTANCES = {}
    FOLDER_PATH = './Minecraft'
    NOT_FOUND_MESSAGE = 'No server found with given name'

    name: str
    process: subprocess.Popen | None = None

    def __init__(self, name, store_instance=True):
        self.name = name

        if store_instance:
            MinecraftServer.INSTANCES[name] = self

    def __str__(self):
        return f'MinecraftServer(name={self.name}, process={self.process})'

    def __repr__(self):
        return str(self)

    @classmethod
    def of(cls, name):
        instance = cls.INSTANCES.get(name)
        return instance if instance is not None else cls(name)

    @classmethod
    def __start(cls, wait: bool):
        return cls.__subprocess_method(wait)(['java', '-jar', 'server.jar', 'nogui'])

    def __stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None

    @staticmethod
    def __subprocess_method(wait: bool):
        return subprocess.run if wait else subprocess.Popen

    @staticmethod
    def exit_directory():
        os.chdir('../..')

    def get_path(self):
        return f'{MinecraftServer.FOLDER_PATH}/{self.name}'

    def get_jar_path(self):
        return f'{self.get_path()}/server.jar'

    def get_properties_path(self):
        return f'{self.get_path()}/server.properties'

    def exists(self) -> bool:
        return os.path.exists(self.get_path())

    def enter_directory(self) -> bool:
        if not self.exists():
            return False

        os.chdir(self.get_path())
        return True

    def start(self) -> bool:
        if not self.enter_directory():
            return False

        if not os.path.exists('eula.txt'):
            self.__start(wait=True)

            with open('eula.txt', 'w') as file:
                file.write('eula=true')

        self.process = self.__start(wait=False)
        MinecraftServer.exit_directory()
        return True

    def stop(self) -> bool:
        if not self.exists():
            return False

        self.__stop()
        return True

    def restart(self) -> bool:
        if not self.enter_directory():
            return False

        self.__stop()
        self.__start(wait=False)
        MinecraftServer.exit_directory()
        return True

    def get_status(self) -> str:
        if not self.exists():
            return MinecraftServer.NOT_FOUND_MESSAGE

        return 'Running' if self.process is not None else 'Not running'
