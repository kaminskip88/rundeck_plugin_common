import os
import yaml
import sys
import logging


class RundeckPluginError(Exception):
    """Base exception class for plugin module"""
    pass


class RundeckPluginInputTypeError(RundeckPluginError):
    """Base exception class for plugin module"""
    pass


class RundeckPlugin(object):
    def __init__(self, *args, **kwargs):
        self.config = {k: self.__get_var(k, v) for (k, v) in kwargs.items()}
        self.__def_loglevel = 'WARN'

    def logger(self, name):
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(self.loglevel)
        logger.addHandler(handler)
        return logger

    @property
    def loglevel(self):
        try:
            logging._checkLevel(self.get_env('JOB_LOGLEVEL'))
            return self.get_env('JOB_LOGLEVEL')
        except (ValueError):
            return self.__def_loglevel

    def __get_var(self, var, type):
        value = self.get_env(var, prefix='RD_CONFIG_')
        if type == 'str':
            return str(value)
        elif type == 'int':
            return int(value) if value else None
        elif type == 'list':
            return list(value.splitlines())
        elif type == 'dict':
            return dict(s.split('=') for s in value.splitlines())
        elif type == 'bool':
            return value == 'true'
        elif type == 'yaml':
            return yaml.load(value, Loader=yaml.FullLoader)
        else:
            raise RundeckPluginInputTypeError('Wrong type: ' + type)

    def get_env(self, var, prefix='RD_'):
        return os.environ.get(prefix + var.upper(), '')

    def print(self, text):
        print(text)
