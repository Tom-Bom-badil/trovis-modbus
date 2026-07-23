"""Static hydronic-configuration definitions for TROVIS system code numbers."""

from __future__ import annotations

from dataclasses import dataclass

FUNCTIONAL_SENSOR_ROLE_KEYS = (
    "af1",
    "af2",
    "vf1",
    "vf2",
    "vf3",
    "vf4",
    "ruef1",
    "ruef2",
    "ruef3",
    "rf1",
    "rf2",
    "rf3",
    "sf1",
    "sf2",
    "sf3",
)

_FUNCTIONAL_SENSOR_ROLE_KEY_SET = frozenset(FUNCTIONAL_SENSOR_ROLE_KEYS)


@dataclass(frozen=True, slots=True)
class ConfigurationTopology:
    """Static hydronic topology selected by one system code number."""

    hk1: bool = False
    hk2: bool = False
    hk3: bool = False
    ww: bool = False
    circulation: bool = False
    solar: bool = False
    buffer_storage: bool = False
    heat_exchanger: bool = False

    def __post_init__(self) -> None:
        if not any(
            (
                self.hk1,
                self.hk2,
                self.hk3,
                self.ww,
                self.circulation,
                self.solar,
                self.buffer_storage,
                self.heat_exchanger,
            )
        ):
            raise ValueError(
                "a configuration topology must contain at least one feature"
            )


@dataclass(frozen=True, slots=True)
class ConfigurationDefinition:
    """Static meaning of one TROVIS system code number.

    ``functional_sensor_roles`` lists sensor roles that may be used by the
    selected hydronic configuration. It does not describe which physical
    sensors are connected and must not hide additional free measurements.
    """

    code: int
    display_code: str
    topology: ConfigurationTopology
    functional_sensor_roles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.code <= 0:
            raise ValueError("code must be positive")

        expected_display_code = f"{self.code // 10}.{self.code % 10}"
        if self.display_code != expected_display_code:
            raise ValueError(
                f"display_code {self.display_code!r} does not match code "
                f"{self.code}: expected {expected_display_code!r}"
            )

        if len(set(self.functional_sensor_roles)) != len(self.functional_sensor_roles):
            raise ValueError(
                f"duplicate functional sensor roles for Anlage {self.display_code}"
            )

        unsupported_roles = (
            set(self.functional_sensor_roles) - _FUNCTIONAL_SENSOR_ROLE_KEY_SET
        )
        if unsupported_roles:
            raise ValueError(
                f"unsupported functional sensor roles for Anlage "
                f"{self.display_code}: {sorted(unsupported_roles)}"
            )
