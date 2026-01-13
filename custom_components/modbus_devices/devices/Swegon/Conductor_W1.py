####################################################
##### Swegon Conductor Apartment W1 Modbus     #####
##### Based on "conductor apartment re modbus.pdf" #
##### Register set W1 (basic, no airflow ctrl) #####
####################################################

import logging

from ..modbusdevice import ModbusDevice
from ..const import ModbusMode, ModbusPollMode, ModbusDataType
from ..datatypes import ModbusDatapoint, ModbusGroup, ModbusDefaultGroups
from ..datatypes import EntityDataSensor, EntityDataSelect, EntityDataNumber, EntityDataBinarySensor

from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.const import PERCENTAGE, UnitOfElectricPotential
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.number import NumberDeviceClass

_LOGGER = logging.getLogger(__name__)

# Define groups - Register types from PDF:
# 1x = Discrete Inputs (read-only, 1-bit) - Alarms and status
# 3x = Input Registers (read-only, 16-bit) - Sensor data
# 4x = Holding Registers (read/write, 16-bit) - Commands and configuration

# Discrete Inputs (1x) - Status and Alarms
GROUP_STATUS = ModbusGroup(ModbusMode.DISCRETE_INPUTS, ModbusPollMode.POLL_ON)
GROUP_ALARMS = ModbusGroup(ModbusMode.DISCRETE_INPUTS, ModbusPollMode.POLL_ON)

# Input Registers (3x) - Device info and sensors
GROUP_DEVICE_INFO = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ONCE)
GROUP_SENSORS = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ON)
GROUP_OUTPUTS = ModbusGroup(ModbusMode.INPUT, ModbusPollMode.POLL_ON)

# Holding Registers (4x) - Commands
GROUP_COMMANDS = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)
GROUP_SETPOINTS = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)

# UI virtual group for calculated values
GROUP_UI = ModbusGroup(ModbusMode.NONE, ModbusPollMode.POLL_OFF)


class Device(ModbusDevice):
    manufacturer = "Swegon"
    model = "Conductor W1"

    def loadDatapoints(self):
        # ============================================
        # DISCRETE INPUTS (1x) - Status bits
        # Addresses are 0-indexed (1x0001 = address 0)
        # ============================================
        self.Datapoints[GROUP_STATUS] = {
            "Condensation": ModbusDatapoint(address=0, entity_data=EntityDataBinarySensor(deviceClass=BinarySensorDeviceClass.MOISTURE)),
            "Relay State": ModbusDatapoint(address=1, entity_data=EntityDataBinarySensor()),
            "Occupancy Switch": ModbusDatapoint(address=2, entity_data=EntityDataBinarySensor(deviceClass=BinarySensorDeviceClass.OCCUPANCY)),
            "Window Switch": ModbusDatapoint(address=3, entity_data=EntityDataBinarySensor(deviceClass=BinarySensorDeviceClass.WINDOW)),
            "Motion": ModbusDatapoint(address=4, entity_data=EntityDataBinarySensor(deviceClass=BinarySensorDeviceClass.MOTION)),
        }

        # Alarms (1x0006-1x0054)
        self.Datapoints[GROUP_ALARMS] = {
            "No Active Alarms": ModbusDatapoint(address=5),  # Inverted logic - 1 = no alarms
            "No Room Unit 1": ModbusDatapoint(address=6),
            "No Room Unit 2": ModbusDatapoint(address=7),
            "No Pressure Sensor": ModbusDatapoint(address=8),
            "No Supply Flow Sensor": ModbusDatapoint(address=9),
            "No Exhaust Flow Sensor": ModbusDatapoint(address=10),
            "Room Unit 1 Temperature": ModbusDatapoint(address=11),
            "Room Unit 2 Temperature": ModbusDatapoint(address=12),
            "Regulator KTY Short Circuit": ModbusDatapoint(address=13),
            "Regulator KTY Open Circuit": ModbusDatapoint(address=14),
            "Room Unit Low Battery": ModbusDatapoint(address=15),
            "PI Controller Overload": ModbusDatapoint(address=16),
            "Setpoint Not Reached": ModbusDatapoint(address=17),
            "No Device List": ModbusDatapoint(address=20),
            "AC Overload": ModbusDatapoint(address=21),
            "System Fault": ModbusDatapoint(address=22),
            "No Serial Number": ModbusDatapoint(address=23),
            # Alarms requiring HW reset (1x0026-1x0044)
            "Short Circuit X11": ModbusDatapoint(address=25),
            "Short Circuit X12": ModbusDatapoint(address=26),
            "Short Circuit X13": ModbusDatapoint(address=27),
            "Short Circuit X14": ModbusDatapoint(address=28),
            "SPI Flash Broken": ModbusDatapoint(address=29),
            "Radio Chip Broken": ModbusDatapoint(address=30),
            "Parameter File Revision": ModbusDatapoint(address=31),
            "Parameter File Format": ModbusDatapoint(address=32),
            "No ModBus ID": ModbusDatapoint(address=33),
            "No Application": ModbusDatapoint(address=34),
            "No Parameters": ModbusDatapoint(address=35),
            "Parameter Missing": ModbusDatapoint(address=36),
            "Parameter Value Error": ModbusDatapoint(address=37),
            "Parameter File Size": ModbusDatapoint(address=38),
            "Wrong Parameter File": ModbusDatapoint(address=39),
            "Check Duct Group SM": ModbusDatapoint(address=40),
            "Check Duct Group DC": ModbusDatapoint(address=41),
            "Previous Parameters Lost": ModbusDatapoint(address=42),
            "Factory Parameters Take Up": ModbusDatapoint(address=43),
            # More auto-reset alarms
            "No Supply Pressure from AHU": ModbusDatapoint(address=46),
            "No Exhaust Pressure from AHU": ModbusDatapoint(address=47),
            "Supply Duct 100% Open": ModbusDatapoint(address=48),
            "Exhaust Duct 100% Open": ModbusDatapoint(address=49),
            "Low Voltage Detect": ModbusDatapoint(address=50),
            "Duct Group Member Missing": ModbusDatapoint(address=52),
            "Negative Pressure": ModbusDatapoint(address=53),
            # Binary sensor for active alarm status
            "Active Alarms": ModbusDatapoint(address=5, entity_data=EntityDataBinarySensor(deviceClass=BinarySensorDeviceClass.PROBLEM, icon="mdi:bell")),
        }

        # ============================================
        # INPUT REGISTERS (3x) - Read-only data
        # ============================================
        self.Datapoints[GROUP_DEVICE_INFO] = {
            "Component Name ID": ModbusDatapoint(address=0),
            "Component Name": ModbusDatapoint(address=1, length=16, type=ModbusDataType.STRING),
            "Application ID": ModbusDatapoint(address=17),
            "HW Serial No": ModbusDatapoint(address=18),
            "SW Version": ModbusDatapoint(address=19),
        }

        self.Datapoints[GROUP_SENSORS] = {
            "Application State": ModbusDatapoint(
                address=21,
                entity_data=EntityDataSensor(
                    icon="mdi:state-machine",
                    enum={
                        0: "Init",
                        1: "Auto Normal",
                        2: "Auto Economy",
                        3: "Manual",
                        4: "Stand-by",
                        5: "Emergency",
                        6: "Night Cool"
                    }
                )
            ),
            "Time Since Boot Years": ModbusDatapoint(address=24, entity_data=EntityDataSensor(units="years", icon="mdi:clock-outline", enabledDefault=False)),
            "Time Since Boot Hours": ModbusDatapoint(address=25, entity_data=EntityDataSensor(units="hours", icon="mdi:clock-outline", enabledDefault=False)),
            "Time Since Boot Minutes": ModbusDatapoint(address=26, entity_data=EntityDataSensor(units=UnitOfTime.MINUTES, icon="mdi:clock-outline", enabledDefault=False)),
            # Temperature sensors with scaling 1:10
            "Regulator Temperature": ModbusDatapoint(
                address=27,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Room Unit 1 Temperature": ModbusDatapoint(
                address=28,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Room Unit 2 Temperature": ModbusDatapoint(
                address=29,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS,
                    enabledDefault=False
                )
            ),
            "Temperature Setpoint RU": ModbusDatapoint(
                address=30,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS,
                    icon="mdi:thermometer-auto"
                )
            ),
            "Battery Level RU": ModbusDatapoint(
                address=32,
                scaling=0.1,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.VOLTAGE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfElectricPotential.VOLT
                )
            ),
            "Room Temperature": ModbusDatapoint(
                address=59,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS
                )
            ),
            "Change Over Temperature": ModbusDatapoint(
                address=60,
                entity_data=EntityDataSensor(
                    deviceClass=SensorDeviceClass.TEMPERATURE,
                    stateClass=SensorStateClass.MEASUREMENT,
                    units=UnitOfTemperature.CELSIUS,
                    enabledDefault=False
                )
            ),
        }

        self.Datapoints[GROUP_OUTPUTS] = {
            "Input Analog 1": ModbusDatapoint(address=36, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Input Analog 2": ModbusDatapoint(address=37, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Input Analog 3": ModbusDatapoint(address=38, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Input Analog 4": ModbusDatapoint(address=39, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Output PWM 1": ModbusDatapoint(address=40, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:pulse", enabledDefault=False)),
            "Output PWM 2": ModbusDatapoint(address=41, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:pulse", enabledDefault=False)),
            "Output PWM 3": ModbusDatapoint(address=42, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:pulse", enabledDefault=False)),
            "Output PWM 4": ModbusDatapoint(address=43, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:pulse", enabledDefault=False)),
            "Output Analog 1": ModbusDatapoint(address=44, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Output Analog 2": ModbusDatapoint(address=45, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Output Analog 3": ModbusDatapoint(address=46, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "Output Analog 4": ModbusDatapoint(address=47, entity_data=EntityDataSensor(units=UnitOfElectricPotential.MILLIVOLT, icon="mdi:sine-wave", enabledDefault=False)),
            "PID Water Output": ModbusDatapoint(address=48, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:water-percent")),
            "PID ChangeOver Output": ModbusDatapoint(address=49, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:swap-horizontal", enabledDefault=False)),
            "Cool Water": ModbusDatapoint(address=52, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:snowflake")),
            "Warm Water": ModbusDatapoint(address=53, entity_data=EntityDataSensor(units=PERCENTAGE, icon="mdi:fire")),
        }

        # ============================================
        # HOLDING REGISTERS (4x) - Read/Write
        # ============================================
        self.Datapoints[GROUP_COMMANDS] = {
            "Operating Mode": ModbusDatapoint(
                address=1,
                entity_data=EntityDataSelect(
                    options={
                        1: "Normal",
                        3: "Manual",
                        4: "Stand-by",
                        5: "Emergency",
                        6: "Night Cool"
                    },
                    icon="mdi:cog"
                )
            ),
            "Relay in Emergency": ModbusDatapoint(
                address=0,
                entity_data=EntityDataSelect(
                    options={0: "Close", 1: "Open", 2: "No Action"},
                    icon="mdi:electric-switch"
                )
            ),
            "Room Number": ModbusDatapoint(
                address=2,
                entity_data=EntityDataNumber(
                    min_value=0,
                    max_value=32000,
                    step=1,
                    icon="mdi:door"
                )
            ),
        }

        self.Datapoints[GROUP_SETPOINTS] = {
            "TC1 Normal Cooling Setpoint": ModbusDatapoint(
                address=23,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=15,
                    max_value=30,
                    step=1
                )
            ),
            "TH1 Normal Heating Setpoint": ModbusDatapoint(
                address=24,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=15,
                    max_value=30,
                    step=1
                )
            ),
            "TC2 Economy Cooling Setpoint": ModbusDatapoint(
                address=25,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=10,
                    max_value=30,
                    step=1
                )
            ),
            "TH2 Economy Heating Setpoint": ModbusDatapoint(
                address=26,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=10,
                    max_value=30,
                    step=1
                )
            ),
            "Night Cool Temperature Setpoint": ModbusDatapoint(
                address=27,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=10,
                    max_value=20,
                    step=1
                )
            ),
            "Frost Guard Temperature": ModbusDatapoint(
                address=22,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=5,
                    max_value=15,
                    step=1
                )
            ),
            "Manual Temperature": ModbusDatapoint(
                address=62,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=0,
                    max_value=50,
                    step=1
                )
            ),
        }

        # Configuration settings
        self.Datapoints[ModbusDefaultGroups.CONFIG] = {
            "Valve Exercise": ModbusDatapoint(
                address=3,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.HOURS,
                    min_value=0,
                    max_value=72,
                    step=1,
                    icon="mdi:valve"
                )
            ),
            "Motion Timer": ModbusDatapoint(
                address=4,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MINUTES,
                    min_value=0,
                    max_value=20,
                    step=1,
                    icon="mdi:timer"
                )
            ),
            "General Warning Time": ModbusDatapoint(
                address=5,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MINUTES,
                    min_value=0,
                    max_value=60,
                    step=1,
                    icon="mdi:alarm"
                )
            ),
            "PI Overload Warning Time": ModbusDatapoint(
                address=6,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MINUTES,
                    min_value=0,
                    max_value=60,
                    step=1,
                    icon="mdi:alarm"
                )
            ),
            "Setpoint Warning Time": ModbusDatapoint(
                address=7,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MINUTES,
                    min_value=0,
                    max_value=60,
                    step=1,
                    icon="mdi:alarm"
                )
            ),
            "System Type": ModbusDatapoint(
                address=13,
                entity_data=EntityDataSelect(
                    options={1: "Heat", 2: "Cool", 3: "Change Over", 4: "Heat+Cool"},
                    icon="mdi:hvac"
                )
            ),
            "Number of Room Units": ModbusDatapoint(
                address=14,
                entity_data=EntityDataSelect(
                    options={1: "One", 2: "Two"},
                    icon="mdi:remote"
                )
            ),
            "Window Switch Config": ModbusDatapoint(
                address=15,
                entity_data=EntityDataSelect(
                    options={0: "Not Used", 1: "Normally Closed", 2: "Normally Open"},
                    icon="mdi:window-closed-variant"
                )
            ),
            "Occupancy Switch Config": ModbusDatapoint(
                address=16,
                entity_data=EntityDataSelect(
                    options={0: "Not Used", 1: "Normally Closed", 2: "Normally Open"},
                    icon="mdi:account-check"
                )
            ),
            "Actuator Type Cool": ModbusDatapoint(
                address=17,
                entity_data=EntityDataSelect(
                    options={1: "NC", 2: "0-10V", 3: "NO"},
                    icon="mdi:valve"
                )
            ),
            "Actuator Type Heat": ModbusDatapoint(
                address=18,
                entity_data=EntityDataSelect(
                    options={1: "NC", 2: "0-10V", 3: "NO"},
                    icon="mdi:valve"
                )
            ),
            "Room Unit Min Setpoint": ModbusDatapoint(
                address=28,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=0,
                    max_value=20,
                    step=1
                )
            ),
            "Room Unit Max Setpoint": ModbusDatapoint(
                address=29,
                entity_data=EntityDataNumber(
                    deviceClass=NumberDeviceClass.TEMPERATURE,
                    units=UnitOfTemperature.CELSIUS,
                    min_value=25,
                    max_value=50,
                    step=1
                )
            ),
            "RU Back to Auto State": ModbusDatapoint(
                address=34,
                entity_data=EntityDataNumber(
                    units=UnitOfTime.MINUTES,
                    min_value=0,
                    max_value=1200,
                    step=1,
                    icon="mdi:timer-refresh"
                )
            ),
            # PID parameters (scale 1:100)
            "P Term Heat": ModbusDatapoint(
                address=47,
                scaling=0.01,
                entity_data=EntityDataNumber(
                    min_value=0.1,
                    max_value=100,
                    step=0.01,
                    icon="mdi:tune",
                    enabledDefault=False
                )
            ),
            "I Term Heat": ModbusDatapoint(
                address=48,
                scaling=0.01,
                entity_data=EntityDataNumber(
                    min_value=0.1,
                    max_value=100,
                    step=0.01,
                    icon="mdi:tune",
                    enabledDefault=False
                )
            ),
            "P Term Cool": ModbusDatapoint(
                address=49,
                scaling=0.01,
                entity_data=EntityDataNumber(
                    min_value=0.1,
                    max_value=100,
                    step=0.01,
                    icon="mdi:tune",
                    enabledDefault=False
                )
            ),
            "I Term Cool": ModbusDatapoint(
                address=50,
                scaling=0.01,
                entity_data=EntityDataNumber(
                    min_value=0.1,
                    max_value=100,
                    step=0.01,
                    icon="mdi:tune",
                    enabledDefault=False
                )
            ),
            "P Term Change Over": ModbusDatapoint(
                address=51,
                scaling=0.01,
                entity_data=EntityDataNumber(
                    min_value=0.1,
                    max_value=100,
                    step=0.01,
                    icon="mdi:tune",
                    enabledDefault=False
                )
            ),
            "I Term Change Over": ModbusDatapoint(
                address=52,
                scaling=0.01,
                entity_data=EntityDataNumber(
                    min_value=0.1,
                    max_value=100,
                    step=0.01,
                    icon="mdi:tune",
                    enabledDefault=False
                )
            ),
        }

        # UI datapoints - calculated values
        self.Datapoints[GROUP_UI] = {
            "Current Alarms": ModbusDatapoint(entity_data=EntityDataSensor(icon="mdi:bell")),
        }

    def onAfterFirstRead(self):
        """Update device info after first successful read."""
        component_name = self.Datapoints[GROUP_DEVICE_INFO]["Component Name"].value
        if component_name:
            self.model = f"Conductor {component_name}"

        hw_serial = self.Datapoints[GROUP_DEVICE_INFO]["HW Serial No"].value
        if hw_serial:
            self.serial_number = str(hw_serial)

        sw_version = self.Datapoints[GROUP_DEVICE_INFO]["SW Version"].value
        if sw_version:
            self.sw_version = str(sw_version)

    def onAfterRead(self):
        """Process data after each read cycle."""
        alarms = self.Datapoints[GROUP_ALARMS]
        attrs = {}

        for dataPointName, data in alarms.items():
            if dataPointName in ["No Active Alarms", "Active Alarms"]:
                continue
            if data.value:
                attrs[dataPointName] = "ALARM"

        if "Active Alarms" in alarms and alarms["Active Alarms"].entity_data:
            alarms["Active Alarms"].entity_data.attrs = attrs
            no_active_alarms = alarms.get("No Active Alarms")
            if no_active_alarms:
                alarms["Active Alarms"].value = not no_active_alarms.value

        active = sorted(attrs.keys())
        state = ", ".join(active) if active else "None"
        self.Datapoints[GROUP_UI]["Current Alarms"].value = state
