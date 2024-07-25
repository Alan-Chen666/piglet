from typing import TypedDict, Unpack
from lib_piglet.loggers.base_logger import base_logger
from lib_piglet.search.base_search import base_search
from lib_piglet.search.search_node import search_node
from lib_piglet.search.event_listener import event_listener
from lib_piglet.search_logger.serialisers import serialisers
from lib_piglet.utils.identifier import identifier


class search_logger_args(TypedDict):
    search: base_search | None
    logger: base_logger


class search_logger(event_listener):

    def __init__(self, **kwargs: Unpack[search_logger_args]):
        self.search_ = kwargs.get("search")
        self.logger_ = kwargs.get("logger") or base_logger

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.logger_.close()

    def get_serialiser(self):
        if self.search_:
            domain = self.search_.expander_.domain_.get_name()
            if domain in serialisers:
                return serialisers[domain]

    def head(self):
        serialiser = self.get_serialiser()
        if serialiser:
            self.logger_.head(
                views=serialiser.views(),
                pivot=serialiser.pivot(),
            )
        else:
            self.logger_.head()

    def log(self, event: str, current: search_node, **kwargs):
        serialiser = self.get_serialiser()
        self.logger_.event(
            type=event,
            id=identifier(current.state_),
            f=current.f_,
            g=current.g_,
            h=current.h_,
            depth=current.depth_,
            pId=identifier(current.parent_.state_) if current.parent_ else None,
            **(serialiser.serialise(current) if serialiser else None),
            **kwargs
        )
        return current


def bind(search: base_search, logger: search_logger):
    search.listener_ = logger
    logger.search_ = search
    return logger
