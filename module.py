import os

from global_parameters import DESCRIPTOR_NAMES


class Module(object):

    def __init__(self, path):
        self.path = path
        self._descriptor = self.__get_descriptor()
        self.name, self.depends = self.__parse_descriptor()
        self.tech_name = self.__get_tech_name()

    def __get_descriptor(self):
        with os.scandir(self.path) as ls:
            items = [x.name for x in ls if x.is_file()]
            for desc in DESCRIPTOR_NAMES:
                if desc in items:
                    return desc

    def __parse_descriptor(self):
        with open(os.path.join(self.path, self._descriptor), "r") as descriptor:
            pass
        return '', ''

    def __get_tech_name(self):
        return ''

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Module({self.name}, {self.tech_name})"
