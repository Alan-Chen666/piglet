from lib_piglet.loggers.base_logger import base_logger
from lib_piglet.loggers.print_logger import print_logger
from lib_piglet.loggers.search_trace_logger import search_trace_logger


loggers: dict[str, type[base_logger]] = {
    "trace": search_trace_logger,
    "print": print_logger,
}
