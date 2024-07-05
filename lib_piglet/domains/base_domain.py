from typing import Generic, TypeVar

from lib_piglet.search.search_node import search_node


State = TypeVar("State")


class base_domain(Generic[State]):
    def serialise(self, state: search_node[State]):
        return dict()

    def views(self):
        return None

    def pivot(self):
        return None
