from module import Module
from global_parameters import DESCRIPTOR_NAMES
import os


class DirectoryParser(object):

    def __init__(self, paths):
        self.paths = self._check_paths(paths)
        self.modules = self._get_modules()

    @staticmethod
    def _check_paths(paths):
        res_paths = []
        for path in paths:
            path = os.path.abspath(path)
            path = os.path.normpath(os.path.normcase(path))
            assert os.path.exists(path) is True, \
                f"Selected path {path} doesn't exist!"
            res_paths.append(path)
        return res_paths

    def _get_modules_paths(self):
        for path in self.paths:
            for directory in os.walk(path):
                if any([desc in directory[2] for desc in DESCRIPTOR_NAMES]):
                    # do not walk further
                    directory[1].clear()
                    yield directory[0]

    @property
    def modules_paths(self):
        paths_gen = self._get_modules_paths()
        return [x for x in paths_gen]

    def _get_modules(self):
        modules = []
        for module_path in self._get_modules_paths():
            modules.append(Module(module_path))
        return modules
