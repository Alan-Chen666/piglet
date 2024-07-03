from lib_piglet.loggers.base_logger import base_logger


class print_logger(base_logger):

    def verbatim(self, s: str):
        print(s)

    def event(self, **kwargs):
        self.verbatim(", ".join(f"{k}: {v}" for k, v in kwargs.items()) + "\n")
