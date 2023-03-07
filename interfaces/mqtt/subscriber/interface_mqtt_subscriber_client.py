import abc


class IMqttSubscriberClient(abc.ABC):

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def on_connect(self, client, userdata, flags, rc):
        pass

    @abc.abstractmethod
    def on_message(self, client, userdata, message):
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def start_forever(self):
        pass
