import os
import ast

from global_parameters import DESCRIPTOR_NAMES
from custom_exceptions import DescriptorError


class Module(object):

    def __init__(self, path):
        self.path = path
        self._descriptor = self.__get_descriptor()
        self.name, self.depends, self.info_dict = self.__parse_descriptor()
        self.tech_name = self.__get_tech_name()

    def __get_descriptor(self):
        with os.scandir(self.path) as ls:
            items = [x.name for x in ls if x.is_file()]
            for desc in DESCRIPTOR_NAMES:
                if desc in items:
                    return desc

    def __parse_descriptor(self):
        with open(os.path.join(self.path, self._descriptor), "r") as descriptor:
            node = ast.parse(descriptor.read()).body
            if len(node) != 1:
                raise DescriptorError(
                    f"Module with path {self.path} has incorrectly "
                    "filled {self._descriptor}"
                )
            node = node[0].value
            info_dict = ast.literal_eval(node)
        return (
            info_dict.get("name", ""),
            info_dict.get("depends", []),
            info_dict,
        )

    def __get_tech_name(self):
        return os.path.basename(self.path)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Odoo Module('{self.name}', '{self.tech_name}')"
