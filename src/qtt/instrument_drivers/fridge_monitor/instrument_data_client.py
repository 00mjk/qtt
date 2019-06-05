from functools import partial
from typing import Any

from qcodes.instrument.base import InstrumentBase
from qcodes.instrument.parameter import Parameter
from zmqrpc.ZmqRpcClient import ZmqRpcClient

from qtt.instrument_drivers.fridge_monitor import ConnectionSettings


class InstrumentDataClient(InstrumentBase):

    def __init__(self, name: str, **kwargs) -> None:
        """ Represents a proxy client for collecting instrument measurable quantities from a InstrumentDataServer.

        The InstrumentDataClient contains the following instance attributes:
            settings: The connection settings of the server.
            timeout: The timeout waiting time in seconds for responce of a remote procedure call.

        Args:
            name (str): the name of the qcodes instrument.
        """
        super().__init__(name, **kwargs)
        self.settings = ConnectionSettings(address='localhost')
        self.__client = None
        self.timeout = 5

    def __create_rpc_server_client(self) -> None:
        username = self.settings.username
        password = self.settings.password
        bind_addres = [self.settings.tcp_bind_address()]
        self.__client = ZmqRpcClient(bind_addres, username=username, password=password)

    def connect(self) -> None:
        """Connects the client to the server using the settings."""
        self.__create_rpc_server_client()

    def __invoke_getter(self, function_name, default_return_value):
        if self.__client is None:
            raise AttributeError('Client not connected! Run connect first.')
        try:
            return self.__client.invoke(function_name, None, self.timeout)
        except Exception:
            return default_return_value

    def __invoke_setter(self, function_name, value, parameter_name='argument'):
        function_parameters = {parameter_name: value}
        if self.__client is None:
            raise AttributeError('Client not connected! Run connect first.')
        return self.__client.invoke(function_name, function_parameters, self.timeout)

    def add_get_set_parameter(self, name: str, parameter_class: type = Parameter, **kwargs) -> None:
        get_command = partial(self.__invoke_getter, name, default_return_value=None)  # default_value???
        set_command = partial(self.__invoke_setter, name)
        self.add_parameter(name, parameter_class, get_cmd=get_command, set_cmd=set_command, **kwargs)

    def add_get_parameter(self, function_name: str, unit: str = '',
                          default_value: Any = None, doc_string: str = '') -> None:
        """ Creates a new get parameter for the instrument client.

        Args:
            function_name: The name of the instrument get parameter.
            unit: The unit of the instrument get parameter.
            default_value: The initial value and on error return value for the get parameter.
            doc_string: The get parameter documentation.
        """
        get_command = partial(self.__invoke_getter, function_name, default_value)
        self.add_parameter(function_name, get_cmd=get_command,
                           unit=unit, default_value=default_value, doc_string=doc_string)
