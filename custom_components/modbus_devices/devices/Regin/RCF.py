"""Support for Regin RCF fan coil controllers via Modbus."""
import logging

from ..modbusdevice import ModbusDevice
from ..const import ModbusMode, ModbusPollMode
from ..datatypes import (
    ModbusDatapoint,
    ModbusGroup,
    ModbusDefaultGroups,
    EntityDataSensor,
    EntityDataSelect,
    EntityDataNumber,
    EntityDataBinarySensor,
    EntityDataSwitch,
    EntityDataButton,
)

from homeassistant.const import (
    UnitOfTemperature,
    UnitOfTime,
    PERCENTAGE,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.number import NumberDeviceClass

_LOGGER = logging.getLogger(__name__)

# Define groups
GROUP_DEVICE_INFO = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ONCE)
GROUP_SENSORS = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ON)
GROUP_CONTROL = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)

class Device(ModbusDevice):
    """Representation of a Regin RCF Modbus device."""

    # Override static device information
    manufacturer = "Regin"
    model = "RCF"

    def loadDatapoints(self):
        # DEVICE_INFO - Read-only
        self.Datapoints[GROUP_DEVICE_INFO] = {
            "Software Type": ModbusDatapoint(
                address=1,
                entity_data=EntityDataSensor(
                    enum={0: "RCP", 1: "RC"},
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Major version": ModbusDatapoint(
                address=2,
                entity_data=EntityDataSensor(
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Minor version": ModbusDatapoint(
                address=3,
                entity_data=EntityDataSensor(
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Branch version": ModbusDatapoint(
                address=4,
                entity_data=EntityDataSensor(
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Revision": ModbusDatapoint(
                address=5,
                entity_data=EntityDataSensor(
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
        }

        # SENSORS - Read (Input Registers Function 04)
        self.Datapoints[GROUP_SENSORS] = {
            "Current running mode": ModbusDatapoint(
                address=7,
                entity_data=EntityDataSensor(
                    enum={
                        0: "Off",
                        1: "Economy/Standby",
                        2: "Not Used",
                        3: "Not Used",
                        4: "Comfort",
                    },
                ),
            ),
            "Current control": ModbusDatapoint(
                address=8,
                entity_data=EntityDataSensor(
                    enum={
                        0: "Off",
                        1: "Heating",
                        2: "Cooling",
                    },
                ),
            ),
            "Current fan speed": ModbusDatapoint(
                address=9,
                entity_data=EntityDataSensor(
                    enum={
                        0: "Off",
                        1: "Speed 1",
                        2: "Speed 2",
                        3: "Speed 3",
                    },
                ),
            ),
            "Room temperature": ModbusDatapoint(
                address=11,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Room temperature external": ModbusDatapoint(
                address=12,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Room temperature internal": ModbusDatapoint(
                address=13,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Change over temperature": ModbusDatapoint(
                address=14,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Controller setpoint": ModbusDatapoint(
                address=20,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Controller output signal": ModbusDatapoint(
                address=21,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=PERCENTAGE
                )
            ),
            "Heating output signal": ModbusDatapoint(
                address=22,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=PERCENTAGE
                )
            ),
            "Cooling output signal": ModbusDatapoint(
                address=23,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=PERCENTAGE
                )
            ),
            "Supply air temperature": ModbusDatapoint(
                address=47,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS,
                ),
            ),
            "Supply air PID output": ModbusDatapoint(
                address=48,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=PERCENTAGE
                )
            ),
            "Supply air setpoint": ModbusDatapoint(
                address=49,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS,
                ),
            ),
        }

        # CONTROL - Read/Write (Holding Registers Function 03)
        self.Datapoints[GROUP_CONTROL] = {
            "Fan Mode": ModbusDatapoint(
                address=5,
                entity_data=EntityDataSelect(
                    options={
                        0: "Off",
                        1: "Manual 1",
                        2: "Manual 2",
                        3: "Manual 3",
                        4: "Auto",
                    },
                ),
            ),
            "Remote State": ModbusDatapoint(
                address=14,
                entity_data=EntityDataSelect(
                    options={
                        0: "Off",
                        1: "Economy/Standby",
                        4: "Comfort",
                        5: "No Remote",
                    },
                ),
            ),
            "Setpoint Offset": ModbusDatapoint(
                address=76,
                scaling=0.1,
                entity_data=EntityDataNumber(
                    min_value=-10,
                    max_value=10,
                    step=0.1,
                    units=UnitOfTemperature.CELSIUS,
                    deviceClass=NumberDeviceClass.TEMPERATURE
                )
            ),
        }

        # CONFIGURATION - Read/Write (Holding Registers Function 03)
        self.Datapoints[ModbusDefaultGroups.CONFIG] = {
            "Basic Setpoint": ModbusDatapoint(
                address=284,
                scaling=0.1,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=10,
                    max_value=35,
                    step=0.1
                )
            ),
            "Change-over Select": ModbusDatapoint(
                address=13,
                entity_data=EntityDataSelect(
                    options={
                        0: "Heating",
                        1: "Cooling",
                        2: "Auto",
                    },
                ),
            ),
            "Fan speed 1 output": ModbusDatapoint(
                address=7,
                entity_data=EntityDataNumber(
                    units=PERCENTAGE,
                    icon="mdi:fan",
                    min_value=0,
                    max_value=100,
                    step=1
                )
            ),
            "Fan speed 2 output": ModbusDatapoint(
                address=8,
                entity_data=EntityDataNumber(
                    units=PERCENTAGE,
                    icon="mdi:fan",
                    min_value=0,
                    max_value=100,
                    step=1
                )
            ),
            "Fan speed 3 output": ModbusDatapoint(
                address=9,
                entity_data=EntityDataNumber(
                    units=PERCENTAGE,
                    icon="mdi:fan",
                    min_value=0,
                    max_value=100,
                    step=1
                )
            ),
            "Modbus Slave Address": ModbusDatapoint(
                address=44,
                entity_data=EntityDataNumber(
                    min_value=1,
                    max_value=247,
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Modbus Parity": ModbusDatapoint(
                address=45,
                entity_data=EntityDataSelect(
                    options={
                        0: "8N2",
                        1: "8O1",
                        2: "8E1",
                        3: "8N1",
                    },
                    category=EntityCategory.DIAGNOSTIC,
                ),
            ),
            "Modbus Char Timeout": ModbusDatapoint(
                address=46,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MILLISECONDS,
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Modbus Answer Delay": ModbusDatapoint(
                address=47,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MILLISECONDS,
                    category=EntityCategory.DIAGNOSTIC
                )
            ),
            "Display Backlight Low": ModbusDatapoint(
                address=48,
                entity_data=EntityDataNumber(
                    min_value=0,
                    max_value=100,
                    units=PERCENTAGE,
                    category=EntityCategory.CONFIG
                )
            ),
            "Display Backlight High": ModbusDatapoint(
                address=49,
                entity_data=EntityDataNumber(
                    min_value=0,
                    max_value=100,
                    units=PERCENTAGE,
                    category=EntityCategory.CONFIG
                )
            ),
            "Display Contrast": ModbusDatapoint(
                address=50,
                entity_data=EntityDataNumber(
                    min_value=0,
                    max_value=15,
                    category=EntityCategory.CONFIG
                )
            ),
            "Display View Mode": ModbusDatapoint(
                address=51,
                entity_data=EntityDataSelect(
                    options={
                        0: "Temp/Setp",
                        1: "Temp/Setp",
                        2: "Setpoint",
                        3: "Offset",
                    },
                    category=EntityCategory.CONFIG,
                ),
            ),
        }

    def onAfterFirstRead(self):
        # Update device info

        a = self.Datapoints[GROUP_DEVICE_INFO]["Software Type"].value
        b = self.Datapoints[GROUP_DEVICE_INFO]["Major version"].value
        c = self.Datapoints[GROUP_DEVICE_INFO]["Minor version"].value
        d = self.Datapoints[GROUP_DEVICE_INFO]["Branch version"].value
        e = self.Datapoints[GROUP_DEVICE_INFO]["Revision"].value
        self.sw_version = '{}{}.{}.{}-{}'.format(a,b,c,d,e)
