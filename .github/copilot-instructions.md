<<<<<<< HEAD
## Purpose
This file tells AI coding agents how to be immediately productive in this repository.

## Big picture
- **Project type**: Home Assistant custom components for Modbus devices.
- **Key area**: device drivers live under `ha-modbus_devices/custom_components/modbus_devices/devices/` (example: `Eastron/SDM630.py`).

## What to inspect first
- Open: `ha-modbus_devices/custom_components/modbus_devices/devices/Eastron/SDM630.py` to understand the device-module layout and register-handling patterns.
- Look for: class definitions, mapping dictionaries (register → field), helper functions for read/write, and any constants used across modules.

## Common patterns and conventions in this repo
- Device modules are organized per vendor under `devices/<Vendor>/`.
- Expect each device file to contain one or more classes/functions that wrap Modbus register access — inspect how register addresses and scaling factors are represented.
- Naming: modules and classes use the device model name (e.g., `SDM630`) — follow the same naming when adding drivers.

## Integration and cross-component touchpoints
- Custom component root: `ha-modbus_devices/custom_components/modbus_devices/` — agents should scan here for platform registration, setup functions, and shared utilities.
- Shared utilities (if present) typically live adjacent to the integration package; prefer reuse over duplication.

## Developer workflows (quick, discoverable commands)
- To find device modules: `rg "custom_components/modbus_devices/devices" -n || true`.
- To search for common functions: `rg "async_setup" -n || true` and `rg "register" -n || true`.

## How an AI agent should operate here
- Always open the device module first to extract concrete register maps and example usages (no speculative changes before reading code).
- When adding or modifying a device, mirror existing file layout, naming, and register representation styles.
- Provide small, focused patches. Include unit-like smoke checks when possible (a minimal script that imports the module and exercises its register mapping is sufficient).

## Examples to reference
- Example device file: `ha-modbus_devices/custom_components/modbus_devices/devices/Eastron/SDM630.py` — use it as the canonical pattern for vendor/device structure and register handling.

## PR and commit guidance for agents
- Keep changes scoped to one device or one shared utility per PR.
- Include a short description referencing the device file(s) changed and why.

## When you need more context
- If important runtime behavior or CI commands are missing from the repo, ask the maintainer for: how to run Home Assistant dev mode for this integration, relevant dependencies, and any expected test commands.

If anything in this guidance is unclear or incomplete, tell me what additional files or workflows you want me to inspect and I will iterate.
=======
# Modbus Devices Integration - Copilot Instructions

## Purpose
This file provides essential knowledge for AI coding agents to be immediately productive in this Home Assistant integration.

## Big Picture Architecture
This integration provides a framework for adding Modbus devices (TCP/RTU) via a driver-based architecture.
- **Core Logic**: `coordinator.py` handles polling and updates. `rtu_bus.py` manages shared serial access for RTU devices.
- **Device Drivers**: Located in `custom_components/modbus_devices/devices/<Manufacturer>/<Model>.py`. All drivers inherit from `ModbusDevice` in `devices/modbusdevice.py`.
- **Entity Generation**: Entities (sensors, switches, etc.) are automatically created by iterating over `self.Datapoints` defined in the device driver.

## Developer Workflows
- **Adding a New Device**:
  1. Create `devices/<Manufacturer>/<Model>.py`.
  2. Inherit from `ModbusDevice`.
  3. Define `manufacturer` and `model`.
  4. Implement `loadDatapoints()` by populating `self.Datapoints` with `ModbusGroup` keys and `ModbusDatapoint` values.
  5. Register the new class in `devices/helpers.py`.
- **Debugging**: Check `home-assistant.log`. Logging is initialized with `_LOGGER = logging.getLogger(__name__)`.

## Project-Specific Conventions & Patterns
- **Datapoint Definition**: Use `ModbusDatapoint(address=..., scaling=..., entity_data=EntityData*(...))`.
  - Example: `ModbusDatapoint(address=11, scaling=0.1, entity_data=EntityDataSensor(deviceClass=SensorDeviceClass.TEMPERATURE))`
- **Scaling**: Applied automatically during read/write. A scaling of `0.1` means Modbus value `215` becomes `21.5`.
- **Groups**: Use `ModbusGroup(ModbusMode.*, ModbusPollMode.*)` to control polling (e.g., `POLL_ON` for frequent, `POLL_ONCE` for static info).
- **Device Info**: Use the `onAfterFirstRead` hook to set `self.sw_version` or `self.serial_number` from polled registers.
- **Configuration UI**: The `CONFIG` group in `Datapoints` provides a selection-based configuration interface in HA.

## Recommended Templates & Starting Points
- **Swegon CASA (Inheritance)**: See `devices/Swegon/CASA_Base.py` and its subclasses (e.g., `CASA_R4.py`). This is the preferred pattern for families of devices with shared registers.
- **LKSystems ARCHUB (Dynamic)**: See `devices/LKSystems/ARCHUB.py` for **dynamic entity generation**. It reads device state (e.g., number of zones) and creates entities accordingly in `onAfterFirstRead`.
- **Standard Driver**: `devices/Eastron/SDM630.py` is a clean example of a standard single-device driver.

## Integration Points
- **PyModbus**: Uses the asynchronous version of `pymodbus`.
- **RTU Sharing**: `RTUBusManager` ensures sequential access for multiple devices on one serial port.

## Key Files
- `devices/modbusdevice.py`: The base class for all drivers.
- `devices/datatypes.py`: Contains `ModbusDatapoint`, `ModbusGroup`, and `EntityData*` definitions.
- `coordinator.py`: Manages the lifecycle and polling of the connected device.

>>>>>>> b95a8ba (docs: Add AI agent instructions)
