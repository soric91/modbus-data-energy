import configparser
from dataclasses import dataclass
from src.Model.model import DeviceConfig, NameParamsModbus
from typing import Dict, List, Union


class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass


@dataclass
class ConfigManager:
    path_config: str

    def __post_init__(self):
        self.__config = configparser.ConfigParser()
        try:
            with open(self.path_config, 'r') as config_file:
                self.__config.read_file(config_file)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {self.path_config}")
        except configparser.Error as e:
            raise ConfigurationError(f"Error parsing configuration file: {e}")

    def __parse_slave_id(self, slave_id_raw: str) -> Union[int, List[int]]:
        return [int(id.strip()) for id in slave_id_raw.split(',') if id.strip()] if ',' in slave_id_raw else int(slave_id_raw)

    def __save_deviceconfig(self, device_name: str) -> DeviceConfig:
        return DeviceConfig(
            protocol=self.__config[device_name].get(NameParamsModbus.protocol, None),
            host=self.__config[device_name].get(NameParamsModbus.host, None),
            port=self.__config[device_name].get(NameParamsModbus.port, None),
            serial_port=self.__config[device_name].get(NameParamsModbus.serial_port, None),
            baudrate=self.__config[device_name].getint(NameParamsModbus.baudrate, None),
            modbus_function=self.__config[device_name].getint(NameParamsModbus.modbus_function, None),
            slave_id=self.__parse_slave_id(self.__config[device_name].get(NameParamsModbus.slave_id, fallback="1")),
            modbus_map_path=self.__config[device_name].get(NameParamsModbus.modbus_map_path, None)
        )

    def get_device_config(self) -> Dict[str, dict]:
        try:
            device_names = self.__config.sections()
            if not device_names:
                return {}

            return {
                name: self.__save_deviceconfig(name).model_dump(exclude_none=True)
                for name in device_names if self.__config.has_section(name)
            }
        except Exception as e:
            raise ConfigurationError(f"Error parsing configuration file: {e}")