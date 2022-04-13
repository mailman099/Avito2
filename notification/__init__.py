from abc import ABC, abstractmethod


class Notificator(ABC):
    @abstractmethod
    def notify(self, new_items):
        pass
