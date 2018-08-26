import os
import ast

from global_parameters import DESCRIPTOR_NAMES
from custom_exceptions import DescriptorError


class Module(object):

    def __init__(self, path):
        self.path = path
        self._descriptor = self.__get_descriptor()
        self.name, self.info_dict = self.__parse_descriptor()
        self.tech_name = self.__get_tech_name()
        self.parents = set()
        self.children = set()

    def __get_descriptor(self):
        with os.scandir(self.path) as ls:
            items = [x.name for x in ls if x.is_file()]
            for desc in DESCRIPTOR_NAMES:
                if desc in items:
                    return desc

    def __parse_descriptor(self):
        with open(os.path.join(self.path, self._descriptor),
                  "rb") as descriptor:
            node = ast.parse(descriptor.read()).body
            if len(node) != 1:
                raise DescriptorError(
                    f"Module with path {self.path} has incorrectly "
                    "filled {self._descriptor}"
                )
            node = node[0].value
            info_dict = ast.literal_eval(node)
        return info_dict.get("name", ""), info_dict

    def __get_tech_name(self):
        return os.path.basename(self.path)

    def __str__(self):
        return self.tech_name

    def __repr__(self):
        return f"Odoo Module('{self.name}', '{self.tech_name}')"

    @property
    def expanded_children(self):
        exp_children = set()
        covered_modules = []

        def expand(module):
            nonlocal exp_children
            exp_children = exp_children.union(module.children)
            if module.name not in covered_modules:
                covered_modules.append(module.name)
                for child in module.children:
                    expand(child)

        expand(self)
        return exp_children

    def get_cyclic_dependencies(self):
        if self not in self.expanded_children:
            return False
        result = [[self.tech_name] + path
                  for path in self.__get_cyclic_dependencies()]
        return result


    def __get_graph_of_children(self):
        modules = self.expanded_children
        graph = {
            x.tech_name: [y.tech_name for y in x.children]
            for x in modules
        }
        return graph

    def __get_cyclic_dependencies(self):
        graph = self.__get_graph_of_children()
        fringe = [(self.tech_name, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == self.tech_name:
                yield path
                continue
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path + [next_state]))

    def has_child(self, name, key="tech_name"):
        return bool(name in map(lambda x: getattr(self, key), self.children))

    def has_parent(self, name, key="tech_name"):
        return bool(name in map(lambda x: getattr(self, key), self.parents))


class UnknownModule(Module):

    def __init__(self, tech_name):
        self.path = None
        self._descriptor = None
        self.name = tech_name
        self.info_dict = {}
        self.tech_name = tech_name
        self.parents = set()
        self.children = set()

    def __repr__(self):
        return f"Uknown Odoo Module('{self.tech_name}')"
