import abc


class IDatabase(abc.ABC):

    @abc.abstractmethod
    def start_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass

    @abc.abstractmethod
    def create_database(self, database_name):
        pass

    @abc.abstractmethod
    def choose_database(self, database_name):
        pass

    @abc.abstractmethod
    def destroy_database(self, database_name):
        pass

    @abc.abstractmethod
    def read_query(self, query):
        pass

    @abc.abstractmethod
    def execute_query(self, query):
        pass
