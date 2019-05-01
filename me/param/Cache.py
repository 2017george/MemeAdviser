# |==========================================|
# | Copyright (c) 2019-present Reece Dunham  |
# | All rights reserved                      |
# | Used with explicit permission            |
# |==========================================|

# Taken from a project that may become open source soon, please keep the copyright header

class FileCache:
    def __init__(self) -> None:
        self.file_caches = []

    def refresh(self, file) -> object:
        with open(file, mode="r") as filehandler:
            if not type(filehandler) is TextIOWrapper:
                raise OSError("File handler not instance of TextIOWrapper! Quitting...")
            else:
                lines = filehandler.readlines()
                for i, x in enumerate(lines):
                    lines[i] = lines[i].replace("\n", "")
                return lines

    def get(self) -> object:
        return self.file_caches

    def add(self, i: object) -> bool:
        try:
            self.file_caches.append(i)
        except:
            return False
        finally:
            return True
