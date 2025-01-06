"""Support for Blueair binary sensors."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device import BlueairDataUpdateCoordinator
from .entity import BlueairEntity


async def async_setup_entry(
    hass: HomeAssistant, config_entry, async_add_entities
) -> None:
    """Set up the Blueair binary sensor entry."""

    devices: list[BlueairDataUpdateCoordinator] = hass.data[DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        # Don't add sensors to classic models
        if (
            device.model.startswith("classic") and not device.model.endswith("i")
        ) or device.model == "foobot":
            pass
        else:
            entities.extend(
                [
                    BlueairFilterStatusSensor(
                        f"{device.device_name}_filter_status", device
                    ),
                    BlueairChildLockSensor(f"{device.device_name}_child_lock", device),
                ]
            )

    async_add_entities(entities)


class BlueairFilterStatusSensor(BlueairEntity, BinarySensorEntity):
    """Monitors the status of the Filter."""

    entity_description = BinarySensorEntityDescription(
        key="filter_status",
        name="Filter Status",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:air-filter",
    )

    def __init__(self, name, device) -> None:
        """Initialize the filter_status sensor."""
        super().__init__("filter_status", name, device)
        self._state: str = False

    @property
    def is_on(self) -> bool:
        """Return the current filter_status."""
        if self._device.filter_status is None:
            return None
        return bool(str(self._device.filter_status) != "OK")


class BlueairChildLockSensor(BlueairEntity, BinarySensorEntity):
    """Monitors the status of the Child Lock."""

    entity_description = BinarySensorEntityDescription(
        key="child_lock",
        name="Child Lock",
        device_class=BinarySensorDeviceClass.LOCK,
        icon="mdi:lock",
    )

    def __init__(self, name, device) -> None:
        """Initialize the child_lock sensor."""
        super().__init__("child_lock", name, device)
        self._state: str = False

    @property
    def is_on(self) -> bool:
        """Return the current child_lock."""
        if self._device.child_lock is None:
            return None
        return bool(str(self._device.child_lock) == "0")
