"""Native TROVIS date, recurring-date, and time value tests."""

from __future__ import annotations

from datetime import date, datetime, time

import pytest

from trovis_modbus import MonthDay, Trovis557x, TrovisValueValidationError


def test_temporal_metadata(trovis: Trovis557x) -> None:
    clock_date = trovis.clock.require_metadata_for("date")
    assert clock_date.value_kind == "date"
    assert clock_date.writable is True
    assert clock_date.temporal is not None
    assert clock_date.temporal.resolution == "day"
    assert clock_date.temporal.min_year == 2000
    assert clock_date.temporal.max_year == 2098

    summer_start = trovis.controller.require_metadata_for("summer_start")
    assert summer_start.value_kind == "month_day"
    assert summer_start.temporal is not None
    assert summer_start.temporal.resolution == "day"

    disinfection_start = trovis.hot_water.require_metadata_for(
        "disinfection_start"
    )
    assert disinfection_start.value_kind == "time"
    assert disinfection_start.temporal is not None
    assert disinfection_start.temporal.resolution == "minute"
    assert disinfection_start.temporal.min_time == time(0, 0)
    assert disinfection_start.temporal.max_time == time(23, 45)


def test_temporal_codecs(trovis: Trovis557x) -> None:
    time_field = trovis.clock._register_fields["time"]
    assert time_field.decode([1430]) == time(14, 30)
    assert time_field.decode([2360]) is None
    assert time_field.encode(time(8, 5)) == [805]

    date_field = trovis.clock._register_fields["date"]
    assert date_field.decode([2106, 2026]) == date(2026, 6, 21)
    assert date_field.decode([3102, 2025]) is None
    assert date_field.encode(date(2027, 1, 2)) == [201, 2027]

    month_day_field = trovis.controller._register_fields["summer_start"]
    assert month_day_field.decode([1505]) == MonthDay(15, 5)
    assert month_day_field.decode([3102]) is None
    assert month_day_field.encode(MonthDay(29, 2)) == [2902]


async def test_clock_native_writes(trovis: Trovis557x) -> None:
    unit = trovis.clock._unit

    await trovis.clock.set_time(time(8, 15))
    assert (await unit.read_holding_registers(99, 1))[0] == 815

    await trovis.clock.set_date(date(2027, 1, 2))
    assert (await unit.read_holding_registers(100, 1))[0] == 201
    assert (await unit.read_holding_registers(101, 1))[0] == 2027

    await trovis.clock.async_update()
    assert trovis.clock.time == time(8, 15)
    assert trovis.clock.date == date(2027, 1, 2)


async def test_datetime_write(trovis: Trovis557x) -> None:
    await trovis.clock.set_datetime(datetime(2028, 12, 31, 23, 45))
    await trovis.clock.async_update()
    assert trovis.clock.datetime == datetime(2028, 12, 31, 23, 45)


async def test_recurring_date_and_disinfection_writes(
    trovis: Trovis557x,
) -> None:
    unit = trovis.controller._unit

    await trovis.controller.set_summer_start(MonthDay(1, 4))
    assert (await unit.read_holding_registers(112, 1))[0] == 104

    await trovis.hot_water.set_disinfection_start(time(20, 15))
    await trovis.hot_water.set_disinfection_stop(time(22, 0))
    assert (await unit.read_holding_registers(1831, 1))[0] == 2015
    assert (await unit.read_holding_registers(1832, 1))[0] == 2200


@pytest.mark.parametrize(
    "value",
    [time(12, 0, 1), time(12, 0, 0, 1)],
)
def test_time_rejects_subminute_precision(
    trovis: Trovis557x,
    value: time,
) -> None:
    field = trovis.clock._register_fields["time"]
    with pytest.raises(TrovisValueValidationError):
        field.encode(value)


def test_disinfection_time_rejects_out_of_range_value(
    trovis: Trovis557x,
) -> None:
    field = trovis.hot_water._register_fields["disinfection_start"]
    assert field.decode([2350]) is None
    with pytest.raises(TrovisValueValidationError):
        field.encode(time(23, 50))


def test_date_rejects_unsupported_year(trovis: Trovis557x) -> None:
    field = trovis.clock._register_fields["date"]
    with pytest.raises(TrovisValueValidationError):
        field.encode(date(2099, 1, 1))
