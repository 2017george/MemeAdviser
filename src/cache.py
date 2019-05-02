# |==========================================|
# | Copyright (c) 2017-present Reece Dunham  |
# | All rights reserved                      |
# | Used with explicit permission            |
# |==========================================|

# Taken from a project that may become open source soon, please keep the copyright header

from io import TextIOWrapper

class FileCache:
    def __init__(self):
        self.file_caches = []

    def refresh(self, file: AbstractFile) -> object:
        with open(file.get_name, mode="r") as filehandler:
            if not type(filehandler) is TextIOWrapper:
                raise OSError("File handler not instance of TextIOWrapper! Quitting...")
            else:
                return list(filter(None, filehandler.read().split("\n")))

    def get(self) -> object:
        return self.file_caches

    def get_by_int(self, num: int) -> object:
        try:
            return self.file_caches[num]
        except Exception as e:
            return e

    def add(self, i: object) -> bool:
        try:
            self.file_caches.append(i)
        except:
            return False
        finally:
            return True

    def clear_file(self, file: AbstractFile) -> object:
        try:
            open(file.get_name(), mode="w")
            return None
        except Exception as e:
            return e

    def write_to_file(self, file: AbstractFile, content: object) -> None:
        self.clear_file(file)
        with open(file.get_name(), mode="w") as filehandler:
            filehandler.write(content)
        return None

class AbstractFile:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name
