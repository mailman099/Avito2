from abc import abstractmethod, ABC


class ContentParser(ABC):
    @abstractmethod
    def parse(self, content):  # type: (str) -> list[dict]
        pass
