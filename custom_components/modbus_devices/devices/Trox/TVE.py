import logging

from ..modbusdevice import ModbusDevice
from ..datatypes import ModbusDatapoint, ModbusGroup, ModbusDefaultGroups, ModbusMode, ModbusPollMode
from ..datatypes import EntityDataSensor, EntityDataNumber, EntityDataSelect, EntityDataBinarySensor

from homeassistant.const import UnitOfVolumeFlowRate, UnitOfElectricPotential, UnitOfTime
from homeassistant.const import PERCENTAGE, DEGREE
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.number import NumberDeviceClass

_LOGGER = logging.getLogger(__name__)

# Define groups
GROUP_0 = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)
GROUP_DEVICE_INFO = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_ON)
GROUP_UI = ModbusGroup(ModbusMode.HOLDING, ModbusPollMode.POLL_OFF)

class Device(ModbusDevice):
    # Override static device information
    manufacturer="Trox"
    model="TVE"

    def loadDatapoints(self):
        # GROUP 0
        self.Datapoints[GROUP_0] = {
            "Setpoint Flowrate": ModbusDatapoint(address=0, scaling=0.01, entity_data=EntityDataNumber(units=PERCENTAGE, min_value=0, max_value=100, step=1)),
            "Override": ModbusDatapoint(address=1, entity_data=EntityDataSelect(options={0: "None", 1: "Open", 2: "Closed", 3: "Q Min", 4: "Q Max"})),
            "Command": ModbusDatapoint(address=2, entity_data=EntityDataSelect(options={0: "None", 1: "Synchronization", 2: "Test", 4: "Reset"})),
            "Position": ModbusDatapoint(address=4, scaling=0.01, entity_data=EntityDataSensor(stateClass=SensorStateClass.MEASUREMENT,units=PERCENTAGE)),
            "Position Degrees": ModbusDatapoint(address=5, entity_data=EntityDataSensor(stateClass=SensorStateClass.MEASUREMENT,units=DEGREE)),
            "Flowrate Percent": ModbusDatapoint(address=6, scaling=0.01, entity_data=EntityDataSensor(stateClass=SensorStateClass.MEASUREMENT,units=PERCENTAGE)),
            "Flowrate Actual": ModbusDatapoint(address=7, entity_data=EntityDataSensor(deviceClass=SensorDeviceClass.VOLUME_FLOW_RATE, stateClass=SensorStateClass.MEASUREMENT, units=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR, icon="mdi:weather-windy")),
            "Analog Setpoint": ModbusDatapoint(address=8, scaling=0.001, entity_data=EntityDataSensor(stateClass=SensorStateClass.MEASUREMENT,units=UnitOfElectricPotential.VOLT)),
        }

        # DEVICE_INFO - Read-only
        self.Datapoints[GROUP_DEVICE_INFO] = {
            "FW": ModbusDatapoint(address=103),
            "Status": ModbusDatapoint(address=104),
        }

        # CONFIGURATION - Read/Write
        self.Datapoints[ModbusDefaultGroups.CONFIG] = {
            "105 Q Min Percent": ModbusDatapoint(address=105, scaling=0.01, entity_data=EntityDataNumber(units=PERCENTAGE, min_value=0, max_value=100, step=1)),
            "106 Q Max Percent": ModbusDatapoint(address=106, scaling=0.01, entity_data=EntityDataNumber(units=PERCENTAGE, min_value=0, max_value=100, step=1)),
            "108 Action on Bus Timeout": ModbusDatapoint(address=108, entity_data=EntityDataSelect(options={0: "None", 1: "Open", 2: "Closed", 3: "Q Min", 4: "Q Max"})),
            "109 Bus Timeout": ModbusDatapoint(address=109, entity_data=EntityDataNumber(units=UnitOfTime.SECONDS, min_value=0, max_value=100, step=1)),
            "120 Q Min": ModbusDatapoint(address=120, entity_data=EntityDataNumber(deviceClass=NumberDeviceClass.VOLUME_FLOW_RATE, units=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR, icon="mdi:weather-windy")),
            "121 Q Max": ModbusDatapoint(address=121, entity_data=EntityDataNumber(deviceClass=NumberDeviceClass.VOLUME_FLOW_RATE, units=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR, icon="mdi:weather-windy")),
            "122 Interface Mode": ModbusDatapoint(address=122, entity_data=EntityDataSelect(options={0: "Modbus RTU", 1: "Analogue", 2: "Hybrid"})),
            "130 Modbus Address": ModbusDatapoint(address=130),
            "201 Volume Flow Unit": ModbusDatapoint(address=201, entity_data=EntityDataSelect(options={0: "L/s", 1: "m³/h", 6: "cfm"})),
            "231 Signal Voltage": ModbusDatapoint(address=231, entity_data=EntityDataSelect(options={0: "0-10V", 1: "2-10V"})),
            "568 Modbus Parameters": ModbusDatapoint(address=568),
            "569 Modbus Response Delay": ModbusDatapoint(address=569, entity_data=EntityDataNumber(units=UnitOfTime.MILLISECONDS, min_value=0, max_value=255, step=1)),
            "572 Switching Threshold": ModbusDatapoint(address=572),
        }

        # UI Datapoints that don't connect directly with modbus address
        self.Datapoints[GROUP_UI] = {
            "Active Alarms": ModbusDatapoint(entity_data=EntityDataBinarySensor(deviceClass=BinarySensorDeviceClass.PROBLEM, icon="mdi:bell"))
        }

    def onAfterFirstRead(self):
        # We need to adjust scaling of flow values depending on a configuration value
        flowUnits = UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR
        match self.Datapoints[ModbusDefaultGroups.CONFIG]["201 Volume Flow Unit"].value:
            case 0:
                flowUnits = UnitOfVolumeFlowRate.LITERS_PER_SECOND
            case 1:
                flowUnits = UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR
            case 6:
                flowUnits = UnitOfVolumeFlowRate.CUBIC_FEET_PER_MINUTE
        self.Datapoints[GROUP_0]["Flowrate Actual"].entity_data.units = flowUnits
        self.Datapoints[ModbusDefaultGroups.CONFIG]["120 Q Min"].entity_data.units = flowUnits
        self.Datapoints[ModbusDefaultGroups.CONFIG]["121 Q Max"].entity_data.units = flowUnits

    def onAfterRead(self):
        self.sw_version = self.Datapoints[GROUP_DEVICE_INFO]["FW"].value

        # Handle alarms
        alarms = self.Datapoints[GROUP_DEVICE_INFO]["Status"].value

        actAlarm = False
        attrs = {}
        if (alarms & (1 << 4)) != 0:
            attrs.update({"Mechanical Overload":"ALARM"})
            actAlarm = True
        if (alarms & (1 << 7)) != 0:
            attrs.update({"Internal Activity":"WARNING"})
        if (alarms & (1 << 9)) != 0:
            attrs.update({"Bus Timeout":"WARNING"})

        self.Datapoints[GROUP_UI]["Active Alarms"].value = actAlarm
        self.Datapoints[GROUP_UI]["Active Alarms"].entity_data.attrs = attrs