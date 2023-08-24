import abc


class JSONSerializable(abc.ABC):
    @abc.abstractmethod
    def tojson(self) -> dict: ...
