# demo_reader/multireader.py

import os
import pkgutil
import importlib
import demo_reader.compressed


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(
        ns_pkg.__path__,
        ns_pkg.__name__ + "."
    )

compression_plugins = {
    importlib.import_module(module_name)
    for _, module_name, _ in iter_namespace(demo_reader.compressed)
}

extension_map = {
    module.extension: module.opener 
    for module in compression_plugins
}

class MultiReader:
    def __init__(self, filename) -> None:
        extension = os.path.splitext(filename)[1]
        opener = extension_map.get(extension, open)
        self.f = opener(filename, 'rt')
        
    def close(self):
        self.f.close()

    def read(self):
        return self.f.read()