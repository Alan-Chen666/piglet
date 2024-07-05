from typing import TypeVar
from lib_piglet.domains.base_domain import base_domain
from lib_piglet.search.search_node import search_node

State = TypeVar("State")


def serialise(domain: base_domain[State], obj: search_node[State]):
    return domain.serialise(obj)
