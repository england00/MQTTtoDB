import abc


class IPickingSystemModel(abc.ABC):

    @abc.abstractmethod
    def get_pick_and_place_id(self):
        pass

    @abc.abstractmethod
    def get_endpoint(self):
        pass

    @abc.abstractmethod
    def get_resource_mapper(self):
        pass

    @abc.abstractmethod
    def get_resource_path_list(self):
        pass

    @abc.abstractmethod
    def set_pick_and_place_id(self, pick_and_place_id):
        pass

    @abc.abstractmethod
    def set_endpoint(self, endpoint):
        pass

    @abc.abstractmethod
    def set_resource_mapper(self, resource_mapper):
        pass

    @abc.abstractmethod
    def set_resource_path_list(self, resource_path_list):
        pass
