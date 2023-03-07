import abc


class IMqttPublisherClient(abc.ABC):

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def publish(self, target_topic, model, qos, retained):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
