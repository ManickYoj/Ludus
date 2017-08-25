"""
Model Loader

This gnarly script walks through the model directory and
loads each model into the model module namespace so that we
can eg. `from model import Player` rather than the more verbose
`from model.player import Player`.

"""
import pkgutil
import inspect


__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
  module = loader.find_module(name).load_module(name)

  for name, value in inspect.getmembers(module):
    if name.startswith(('__', '_')):
      continue

    globals()[name] = value
    __all__.append(name)
