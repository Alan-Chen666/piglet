from lib_piglet.loggers.base_logger import base_logger


class file_logger(base_logger):
    def __init__(self, **kwargs):
        self.args = kwargs
        if "file" in self.args:
            self.file = open(self.args["file"], "w")
        else:
            raise IOError("Output file not specified.")

    def verbatim(self, s: str):
        self.file.write(s)

    def event(self, **kwargs):
        self.verbatim(", ".join(f"{k}: {v}" for k, v in kwargs.items()) + "\n")

    def close(self):
        self.file.close()
