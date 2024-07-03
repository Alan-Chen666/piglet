from lib_piglet.loggers.file_logger import file_logger
from yaml import dump


class search_trace_logger(file_logger):
    out = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def head(self, **kwargs):
        self.verbatim(dump({"version": "1.4.0"}))
        if "views" in kwargs:
            self.verbatim(dump({"views": kwargs["views"]}))
        self.verbatim("events:\n")

    def event(self, **kwargs):
        self.verbatim(f"- {dump(kwargs, default_flow_style=True,width=99999)}")
