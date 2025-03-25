from pydantic import BaseModel, Field
from typing import Optional, Union, List
from enum import Enum


class DeviceConfig(BaseModel):
    protocol: str
    host: Optional[str] = None
    port: Optional[str] = None
    serial_port: Optional[str] = None
    baudrate: Optional[int] = None
    modbus_function: Optional[int] = None
    slave_id: Union[int, List[int]] = Field(default=1)
    modbus_map_path: Optional[str] = None
    
    
    
    
class NameParamsModbus(str,Enum):
    protocol = "protocol"
    host = "host"
    port = "port"
    serial_port = "serial_port"
    baudrate = "baudrate"
    modbus_function = "modbus_function"
    slave_id = "slave_id"   
    modbus_map_path = "modbus_map_path"
    
    def __str__(self) -> str:
        return self.value
    
    
    
class ProtocolCom(str,Enum):
    RTU = "RTU"
    TCP = "TCP"
    
    def __str__(self) -> str:
        return self.value