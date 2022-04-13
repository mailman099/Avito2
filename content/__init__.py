from abc import ABC, abstractmethod


class ContentGetter(ABC):
    @abstractmethod
    def get_resource(self, url):  # type: (str) -> str
        pass
