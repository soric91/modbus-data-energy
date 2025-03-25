from src.Config.config import ConfigManager
from src.Comunication.conect import ModbusClientFactory
def main():
    config_manager = ConfigManager("config.ini") 
    
    device_config = config_manager.get_device_config()
    
    modbus_client_factory = ModbusClientFactory(device_config).clients
    print(modbus_client_factory)
if __name__ == "__main__":
    main()
