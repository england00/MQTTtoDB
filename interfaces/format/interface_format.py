import abc
from models.resource_model import ResourceModel


class IFormat(abc.ABC):

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def to_format(self, resource: ResourceModel):
        pass

    @abc.abstractmethod
    def from_format(self, senml_pack, resource: ResourceModel):
        pass
