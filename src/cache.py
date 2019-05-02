"""
|==========================================|
| Copyright (c) 2017-present Reece Dunham  |
| All rights reserved                      |
| Used with explicit permission            |
|==========================================|
"""

# Taken from a project that may become open source soon, please keep the copyright header

from io import TextIOWrapper


class AbstractFile:
    """Used for defining a file"""
    def __init__(self, name: str):
        """
        Create class instance

        :param name: the name of the file (and relative path if needed)
        """
        self.name = name

    def get_name(self) -> str:
        """
        Get the file's name

        :return: the file's name
        :rtype: str
        """
        return self.name


class FileCache:
    """Allows for caching of files easily!"""
    def __init__(self):
        """
        Creates the class

        :return: nothing
        """
        self.file_caches = []

    def refresh(self, file: AbstractFile) -> (object, list):
        """
        Refreshes the @TextIOWrapper for the file

        :param file: the @AbstractFile to refresh
        :return: some list thing
        """
        with open(file.get_name(), mode="r") as filehandler:
            if not type(filehandler) is TextIOWrapper:
                raise OSError("File handler not instance of TextIOWrapper! Quitting...")
            else:
                return list(filter(None, filehandler.read().split("\n")))

    def get(self) -> list:
        """
        Get the file caches stored in memory

        :return: file caches
        :rtype: list
        """
        return self.file_caches

    def get_by_int(self, num: int) -> object:
        """
        Get a file cache by its position in the caches array

        :param num: the number to search for
        :return: either the cache or an Exception, see next line
        :raises: Exception if anything went wrong
        :rtype: object
        """
        try:
            return self.file_caches[num]
        except Exception as e:
            return e

    def add(self, file: AbstractFile) -> bool:
        """
        Add a file to the list of caches

        :param file: the AbstractFile to append
        :return: boolean that is True if it worked, False if it didn't
        :rtype: bool
        :raises: Exception if it didn't work for some reason
        """
        try:
            self.file_caches.append(file)
        except Exception:
            return False
        finally:
            return True

    def clear_file(self, file: AbstractFile) -> object:
        """
        Clears a file of all contents, but does not delete the file
        :param file: the @AbstractFile to clear
        :return: either None or some Exception form
        :raises: Exception
        """
        try:
            open(file.get_name(), mode="w")
            return None
        except Exception as e:
            return e

    def write_to_file(self, file: AbstractFile, contents: list) -> None:
        """
        Writes to a file

        :param file: the @AbstractFile to write to
        :param contents: a list of items to write to the file
        :return: None
        """
        self.clear_file(file)
        with open(file.get_name(), mode="w") as filehandler:
            for item in contents:
                filehandler.write(str(contents[item]))
        return None
