import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, Union

from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient


from src.Model.model import NameParamsModbus, ProtocolCom


@dataclass
class ModbusClientFactory:
    """
    Dataclass for creating and managing Modbus clients
    """
    config_dict: Dict[str, Dict[str, Any]]
    clients: Dict[str, Union[AsyncModbusSerialClient, AsyncModbusTcpClient]] = field(init=False, default_factory=dict)

    async def __start_connection(self) -> Dict[str, Union[AsyncModbusSerialClient, AsyncModbusTcpClient]]:
        """
        Establish Modbus client connections for all devices in `config_dict`.

        :return: Dictionary {device_name: modbus_client} with connected clients
        """
        self.clients = {}

        for device_name, device_config in self.config_dict.items():
            client = None

            try:
              
                protocol = device_config.get(NameParamsModbus.protocol)

                if protocol == ProtocolCom.RTU:
                    client = AsyncModbusSerialClient(
                        port=device_config.get(NameParamsModbus.serial_port),
                        baudrate=device_config.get(NameParamsModbus.baudrate),
                    )
                elif protocol == ProtocolCom.TCP:
                    client = AsyncModbusTcpClient(
                        host=device_config.get(NameParamsModbus.host),
                        port=device_config.get(NameParamsModbus.port),

                    )
                else:
                    print(f"[Modbus] --> No protocol mapped for {device_name}")
                    continue

                # Attempt connection
                await client.connect()

                if not client.connected:
                    print(f"[Modbus] --> Connection unsuccessful for {device_name}")
                    continue

                print(f"[Modbus] --> Connection successful for {device_name}")
                self.clients[device_name] = client  # Store successful connections

            except asyncio.TimeoutError:
                print(f"[Modbus] --> Connection timed out for {device_name}")
                await self.__end_connection(client)
            except AssertionError:
                print(f"[Modbus] --> Client connection assertion failed for {device_name}")
                await self.__end_connection(client)
            except Exception as e:
                print(f"[Modbus] --> Unexpected error for {device_name}: {e}")
                await self.__end_connection(client)

        return self.clients  # Return only successful clients

    async def __end_connection(self, client):
        """
        Close Modbus client connection
        
        :param client: Modbus client to close
        """
        try:
            if client:
                client.close()
                print("[Modbus] --> Closed connection successfully")
        except Exception as e:
            print(f"[Modbus] --> Cannot end connection with Modbus client: {e}")