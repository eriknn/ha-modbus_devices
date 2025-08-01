import logging

from ..modbusdevice import ModbusDevice
from ..datatypes import ModbusDatapoint, ModbusGroup, ModbusDefaultGroups, ModbusMode, ModbusPollMode
from ..datatypes import ModbusSensorData, ModbusNumberData, ModbusSelectData, ModbusBinarySensorData, ModbusSwitchData, ModbusButtonData

from copy import deepcopy

from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.const import PERCENTAGE
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.number import NumberDeviceClass

_LOGGER = logging.getLogger(__name__)

class Device(ModbusDevice):
    Datapoints = deepcopy(ModbusDevice.Datapoints)

    # Override static device information
    manufacturer="LKSystems"
    model="ARCHUB"

    # Define groups
    GROUP_DEVICE_INFO = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ONCE)
    GROUP_UNIT_STATUSES = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ON)  
    GROUP_ALARMS = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ON)
    GROUP_SENSORS = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ON)
    GROUP_COMMANDS = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)
    GROUP_SETPOINTS = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)
#    GROUP_UI = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_OFF) 

    # DEVICE_INFO - Read-only
    Datapoints[GROUP_DEVICE_INFO] = {
        "Serial Number": ModbusDatapoint(Address=1, Length=3),     # 4 registers
        "Software Version Major": ModbusDatapoint(Address=4),
        "Software Version Minor": ModbusDatapoint(Address=5),
        "Software Version Micro": ModbusDatapoint(Address=6),
        "Number Of Zones": ModbusDatapoint(Address=51),
    }

    # UNIT_STATUSES - Read
    Datapoints[GROUP_UNIT_STATUSES] = {
        "Actuator 1": ModbusDatapoint(Address=60),
        "Actuator 2": ModbusDatapoint(Address=61),
        "Actuator 3": ModbusDatapoint(Address=62),
        "Actuator 4": ModbusDatapoint(Address=63),
        "Actuator 5": ModbusDatapoint(Address=64),
        "Actuator 6": ModbusDatapoint(Address=65),
        "Actuator 7": ModbusDatapoint(Address=66),
        "Actuator 8": ModbusDatapoint(Address=67),
        "Actuator 9": ModbusDatapoint(Address=68),
        "Actuator 10": ModbusDatapoint(Address=69),
        "Actuator 11": ModbusDatapoint(Address=70),
        "Actuator 12": ModbusDatapoint(Address=71),
    }


    # ALARMS - Read-only
    Datapoints[GROUP_ALARMS] = {
        "Cooling Emergency Mode": ModbusDatapoint(Address=80),
    }

    # SENSORS - Read
    #
    # Zones below (MAX 12)
    # Should theses be addded dynamically based on "number of zones"??? 
    Datapoints[GROUP_SENSORS] = {
        "Zone1 Actual Temperature": ModbusDatapoint(Address=100, Scaling=0.1, DataType=ModbusSensorData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS)),
        "Zone1 Actual Humidity": ModbusDatapoint(Address=101, Scaling=0.1, DataType=ModbusSensorData(deviceClass=SensorDeviceClass.HUMIDITY, units=PERCENTAGE)),
        "Zone1 Actual Battery": ModbusDatapoint(Address=102, DataType=ModbusSensorData(deviceClass=SensorDeviceClass.BATTERY, units=PERCENTAGE)),
        "Zone1 Actual Signal Strength": ModbusDatapoint(Address=103),
        "Zone1 Thermostat Address": ModbusDatapoint(Address=104, Length=3),
        "Zone1 Connected Actuators": ModbusDatapoint(Address=106),
    }



    # COMMANDS - Read/Write
    Datapoints[GROUP_COMMANDS] = {
        "Operating Mode": ModbusDatapoint(Address=0, DataType=ModbusSelectData(options={0: "Undefined", 1: "Heating", 2: "Cooling"})),
        "LED Enable": ModbusDatapoint(Address=58, DataType=ModbusSelectData(options={0: "Disable", 1: "Enable"})),
    }

    # SETPOINTS - Read/Write
    Datapoints[GROUP_SETPOINTS] = {
        "Temperature Alarm High Level": ModbusDatapoint(Address=50, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=-100, max_value=100, step=0.1)),
        "Temperature Alarm Low Level": ModbusDatapoint(Address=51, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=-100, max_value=100, step=0.1)),
        "Humidity Alarm High Level": ModbusDatapoint(Address=52, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.HUMIDITY, units=PERCENTAGE, min_value=0, max_value=100, step=0.1)),
        "Humidity Alarm Low Level": ModbusDatapoint(Address=53, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.HUMIDITY, units=PERCENTAGE, min_value=0, max_value=100, step=0.1)),
        "Battery Alarm Low Level": ModbusDatapoint(Address=54, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.BATTERY, units=PERCENTAGE, min_value=0, max_value=100, step=0.1)),
        "Battery Alarm Critical Level": ModbusDatapoint(Address=55, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.BATTERY, units=PERCENTAGE, min_value=0, max_value=100, step=0.1)),
        "Cooling Emergency Number of Zones": ModbusDatapoint(Address=56, DataType=ModbusNumberData(min_value=0, max_value=12)),
        "Coling Mode Humidity Limit": ModbusDatapoint(Address=57, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.HUMIDITY, units=PERCENTAGE, min_value=0, max_value=100, step=0.1)),
#
# Zones below (MAX 12), should be in separate sections? Should be addded dynamically based on "number of zones"??
#
##            "Zone 1 Target Temperature": ModbusDatapoint(Address=100, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=-100, max_value=100, step=0.1)),
        "Zone 1 Target Temperature": ModbusDatapoint(Address=100, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=-100, max_value=100)),
        "Zone 1 Override ": ModbusDatapoint(Address=101, DataType=ModbusSelectData(options={0: "Inactive", 1: "Active"})),
        "Zone 1 Override Level": ModbusDatapoint(Address=102, DataType=ModbusNumberData(min_value=0, max_value=255)),
    }
##
##
## Below is leftover code from casa, remove later... 
##
    # CONFIGURATION - Read/Write
    Datapoints[ModbusDefaultGroups.CONFIG] = {
##            "Travelling Mode Speed Drop": ModbusDatapoint(Address=5105, DataType=ModbusNumberData(units=PERCENTAGE, min_value=0, max_value=20, step=1)),
##            "Fireplace Run Time": ModbusDatapoint(Address=5103, DataType=ModbusNumberData(units=UnitOfTime.MINUTES, min_value=0, max_value=60, step=1)),
##            "Fireplace Max Speed Difference": ModbusDatapoint(Address=5104, DataType=ModbusNumberData(units=PERCENTAGE, min_value=0, max_value=25, step=1)),
##            "Night Cooling": ModbusDatapoint(Address=5163, DataType=ModbusNumberData(units=None)),
##            "Night Cooling FreshAir Max": ModbusDatapoint(Address=5164, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=0, max_value=25, step=0.1)),
##            "Night Cooling FreshAir Start": ModbusDatapoint(Address=5165, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=0, max_value=25, step=0.1)),
##            "Night Cooling RoomTemp Start": ModbusDatapoint(Address=5166, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=0, max_value=35, step=0.1)),
##            "Night Cooling SupplyTemp Min": ModbusDatapoint(Address=5167, Scaling=0.1, DataType=ModbusNumberData(deviceClass=NumberDeviceClass.TEMPERATURE, units=UnitOfTemperature.CELSIUS, min_value=10, max_value=25, step=0.1)),
##            "Away Supply Speed": ModbusDatapoint(Address=5301, DataType=ModbusNumberData(units=PERCENTAGE, min_value=20, max_value=100, step=1)),
##            "Away Exhaust Speed": ModbusDatapoint(Address=5302, DataType=ModbusNumberData(units=PERCENTAGE, min_value=20, max_value=100, step=1)),
##            "Home Supply Speed": ModbusDatapoint(Address=5303, DataType=ModbusNumberData(units=PERCENTAGE, min_value=20, max_value=100, step=1)),
##            "Home Exhaust Speed": ModbusDatapoint(Address=5304, DataType=ModbusNumberData(units=PERCENTAGE, min_value=20, max_value=100, step=1)),
##            "Boost Supply Speed": ModbusDatapoint(Address=5305, DataType=ModbusNumberData(units=PERCENTAGE, min_value=20, max_value=100, step=1)),
##            "Boost Exhaust Speed": ModbusDatapoint(Address=5306, DataType=ModbusNumberData(units=PERCENTAGE, min_value=20, max_value=100, step=1)),
    }

    _LOGGER.debug("Loaded datapoints for %s %s", manufacturer, model)

    def onAfterFirstRead(self):
        # Update device info
        self.serial_number = self.Datapoints[self.GROUP_DEVICE_INFO]["Serial Number"].Value

        a = self.Datapoints[self.GROUP_DEVICE_INFO]["Software Version Major"].Value
        b = self.Datapoints[self.GROUP_DEVICE_INFO]["Software Version Minor"].Value
        c = self.Datapoints[self.GROUP_DEVICE_INFO]["Software Version Micro"].Value
        self.sw_version = '{}.{}.{}'.format(a,b,c)

    ##    def onAfterRead(self):
    ##
    ##        # Set alarms as attributes on Alarm-datapoint. This is done so that we don't
    ##        # need to present all values in the UI
    ##        alarms = self.Datapoints[self.GROUP_ALARMS]
    ##        attrs = {}
    ##        for (dataPointName, data) in alarms.items():
    ##            if data.Value:
    ##                attrs.update({dataPointName:"ALARM"})
    ##        alarms["Active Alarms"].Attrs = attrs
