"""Support for Blueair sensors."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device import BlueairDataUpdateCoordinator
from .entity import BlueairEntity

NAME_TEMPERATURE = "Temperature"
NAME_HUMIDITY = "Humidity"


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Blueair sensors from config entry."""
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
                    BlueairTemperatureSensor(
                        f"{device.device_name}_temperature", device
                    ),
                    BlueairHumiditySensor(f"{device.device_name}_humidity", device),
                    BlueairCO2Sensor(f"{device.device_name}_co2", device),
                    BlueairVOCSensor(f"{device.device_name}_voc", device),
                    BlueairAllPollutionSensor(
                        f"{device.device_name}_all_pollution", device
                    ),
                    BlueairPM1Sensor(f"{device.device_name}_pm1", device),
                    BlueairPM10Sensor(f"{device.device_name}_pm10", device),
                    BlueairPM25Sensor(f"{device.device_name}_pm25", device),
                ]
            )
    async_add_entities(entities)


class BlueairTemperatureSensor(BlueairEntity, SensorEntity):
    """Monitors the temperature."""

    entity_description = SensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    )

    def __init__(self, name, device) -> None:
        """Initialize the temperature sensor."""
        super().__init__(NAME_TEMPERATURE, name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current temperature."""
        if self._device.temperature is None:
            return None
        return round(self._device.temperature, 1)


class BlueairHumiditySensor(BlueairEntity, SensorEntity):
    """Monitors the humidity."""

    entity_description = SensorEntityDescription(
        key="humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
    )

    def __init__(self, name, device) -> None:
        """Initialize the humidity sensor."""
        super().__init__(NAME_HUMIDITY, name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current humidity."""
        if self._device.humidity is None:
            return None
        return round(self._device.humidity, 0)


class BlueairCO2Sensor(BlueairEntity, SensorEntity):
    """Monitors the CO2."""

    entity_description = SensorEntityDescription(
        key="co2",
        name="CO2",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    )

    def __init__(self, name, device) -> None:
        """Initialize the CO2 sensor."""
        super().__init__("co2", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current co2."""
        if self._device.co2 is None:
            return None
        return round(self._device.co2, 0)


class BlueairVOCSensor(BlueairEntity, SensorEntity):
    """Monitors the VOC."""

    entity_description = SensorEntityDescription(
        key="voc",
        name="VOC",
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
    )

    def __init__(self, name, device) -> None:
        """Initialize the VOC sensor."""
        super().__init__("voc", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current voc."""
        if self._device.voc is None:
            return None
        return round(self._device.voc, 0)


class BlueairAllPollutionSensor(BlueairEntity, SensorEntity):
    """Monitors the all pollution."""

    entity_description = SensorEntityDescription(
        key="all_pollution",
        name="All Pollution",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:molecule",
    )

    def __init__(self, name, device) -> None:
        """Initialize the all pollution sensor."""
        super().__init__("all_pollution", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current all pollution."""
        if self._device.all_pollution is None:
            return None
        return round(self._device.all_pollution, 0)


class BlueairPM1Sensor(BlueairEntity, SensorEntity):
    """Monitors the pm1."""

    entity_description = SensorEntityDescription(
        key="pm1",
        name="PM1",
        device_class=SensorDeviceClass.PM1,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )

    def __init__(self, name, device) -> None:
        """Initialize the pm1 sensor."""
        super().__init__("pm1", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current pm1."""
        if self._device.pm1 is None:
            return None
        return round(self._device.pm1, 0)


class BlueairPM10Sensor(BlueairEntity, SensorEntity):
    """Monitors the pm10."""

    entity_description = SensorEntityDescription(
        key="pm10",
        name="PM10",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )

    def __init__(self, name, device) -> None:
        """Initialize the pm10 sensor."""
        super().__init__("pm10", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current pm10."""
        if self._device.pm10 is None:
            return None
        return round(self._device.pm10, 0)


class BlueairPM25Sensor(BlueairEntity, SensorEntity):
    """Monitors the pm25."""

    entity_description = SensorEntityDescription(
        key="pm25",
        name="PM2.5",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )

    def __init__(self, name, device) -> None:
        """Initialize the pm25 sensor."""
        super().__init__("pm25", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float:
        """Return the current pm25."""
        if self._device.pm25 is None:
            return None
        return round(self._device.pm25, 0)
