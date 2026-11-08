import logging
from .CASA_Base import GROUP_SETPOINTS, GROUP_UNIT_STATUSES, ModbusDefaultGroups, GROUP_SENSORS, GROUP_UI, Device as BaseDevice
from ..datatypes import ModbusDatapoint, ModbusSensor, ModbusBinarySensor
from homeassistant.const import PERCENTAGE, REVOLUTIONS_PER_MINUTE

_LOGGER = logging.getLogger(__name__)

class Device(BaseDevice):
    # Override static device information
    model="CASA R7"

    def loadDatapoints(self):
        super().loadDatapoints()

        # Modify scaling
        self.Datapoints[GROUP_SETPOINTS]["Temperature Setpoint"].scaling = 1
        self.Datapoints[GROUP_UNIT_STATUSES]["Heat Exchanger"].scaling = 0.1
        self.Datapoints[GROUP_SENSORS]["Absolute Humidity"].scaling=0.01
        self.Datapoints[GROUP_SENSORS]["Absolute Humidity SP"].scaling=0.01

        # Replace HE output with HE RPM
        self.Datapoints[GROUP_UNIT_STATUSES].pop("Heat Exchanger")
        self.Datapoints[GROUP_SENSORS]["Heat Exchanger RPM"] = ModbusSensor(address=6233, scaling=1.0, units=REVOLUTIONS_PER_MINUTE, icon="mdi:hvac")

        # Add entities
        self.Datapoints[GROUP_UNIT_STATUSES]["Summer_Cooling_Active"] = ModbusBinarySensor(address=6333)

        # Modify scaling on configuration tags
        self.Datapoints[ModbusDefaultGroups.CONFIG]["Night Cooling FreshAir Max"].scaling=1
        self.Datapoints[ModbusDefaultGroups.CONFIG]["Night Cooling FreshAir Start"].scaling=1
        self.Datapoints[ModbusDefaultGroups.CONFIG]["Night Cooling RoomTemp Start"].scaling=1
        self.Datapoints[ModbusDefaultGroups.CONFIG]["Night Cooling SupplyTemp Min"].scaling=1