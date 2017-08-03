"""
Factory Loader

This gnarly script walks through the factory directory and
loads each factory into the factory module namespace so that we
can eg. `from factory import PlayerFactory` rather than the more
verbose `from factory.player import PlayerFactory`.

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
