"""Global temperature inputs."""

from __future__ import annotations

from .model import TrovisComponent, temperature


class Sensors(TrovisComponent):
    """Physical sensor inputs, e.g. Pt1000.

    Naming follows the manual abbreviations.
    """

    af1 = temperature(40010)  # AußenFühler 1 - outside_1
    af2 = temperature(40011)  # AußenFühler 2 - outside_2

    vf1 = temperature(40013)  # VorlaufFühler 1 - flow_1
    vf2 = temperature(40014)  # VorlaufFühler 2 - flow_2
    vf3 = temperature(40015)  # VorlaufFühler 3 - flow_3
    vf4 = temperature(40016)  # VorlaufFühler 4 - flow_4

    ruef1 = temperature(40017)  # RücklaufFühler 1 - return_1
    ruef2 = temperature(40018)  # RücklaufFühler 2 - return_2
    ruef3 = temperature(40019)  # RücklaufFühler 3 - return_3

    rf1 = temperature(40020)  # RaumFühler 1 - room_1
    rf2 = temperature(40021)  # RaumFühler 2 - room_2
    rf3 = temperature(40022)  # RaumFühler 3 - room_3

    sf1 = temperature(40023)  # SpeicherFühler 1 - water_storage_1
    sf2 = temperature(40024)  # SpeicherFühler 2 - water_storage_2

    fg1 = temperature(40026, unit="K")  # FernGeber 1 - remote_1
    fg2 = temperature(40027, unit="K")  # FernGeber 2 - remote_2

    sf3_fg3 = temperature(40025)  # SpeicherFühler/FernGeber 3