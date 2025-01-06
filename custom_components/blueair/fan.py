"""Support for Blueair fans."""

from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device import BlueairDataUpdateCoordinator
from .entity import BlueairEntity


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Blueair fans from config entry."""
    devices: list[BlueairDataUpdateCoordinator] = hass.data[DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        if device.model != "foobot":
            entities.extend(
                [
                    BlueairFan(f"{device.device_name}_fan", device),
                ]
            )
    async_add_entities(entities)


class BlueairFan(BlueairEntity, FanEntity):
    """Controls Fan."""

    def __init__(self, name, device) -> None:
        """Initialize the temperature sensor."""
        super().__init__("Fan", name, device)
        self._state: float = None

    @property
    def supported_features(self) -> int:
        """Return the supported features of the fan."""
        # If the fan_mode property is supported, enable support for presets
        if self._device.fan_mode_supported:
            return FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE
        return FanEntityFeature.SET_SPEED

    @property
    def is_on(self) -> int:
        """Return true if the fan is on."""
        return self._device.is_on

    @property
    def percentage(self) -> int | None:
        """Return the current speed percentage."""
        if self._device.fan_speed is not None:
            return int(round(self._device.fan_speed * 33.33, 0))
        return 0

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        if self._device.fan_mode_supported:
            return self._device.fan_mode
        return None

    @property
    def preset_modes(self) -> list | None:
        """Return the list of available preset modes."""
        if self._device.fan_mode_supported:
            return ["auto"]
        return None

    async def async_set_percentage(self, percentage: int) -> None:
        """Set fan speed percentage."""
        if percentage == 100:
            new_speed = "3"
        elif percentage > 50:
            new_speed = "2"
        elif percentage > 20:
            new_speed = "1"
        else:
            new_speed = "0"

        await self._device.set_fan_speed(new_speed)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the fan."""
        await self._device.set_fan_speed("0")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the fan."""
        await self._device.set_fan_speed("2")

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        await self._device.set_fan_mode(preset_mode)

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return 3
