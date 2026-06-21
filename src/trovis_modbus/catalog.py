"""The full Trovis 557x register / coil / derived catalog.

This is a faithful port of the Samson Trovis 557x Home Assistant YAML package
(github.com/Tom-Bom-badil/samson_trovis_557x, HomeAssistant/trovis557x): every
register address, data type, scaling factor, unit and enum mapping. Keys are the
original YAML ``unique_id``s so the surface can be cross-checked one-to-one.
"""

from __future__ import annotations

from .model import CoilDef, DerivedDef, RegisterDef

# Common shape for a temperature register: int16, 0.1 scaling, NaN sentinel.
_TEMP = {
    "data_type": "int16",
    "scale": 0.1,
    "precision": 1,
    "device_class": "temperature",
    "nan_value": 32767,
}


def _temp(
    key: str, name: str, address: int, group: str, *, unit: str = "°C", **extra: object
) -> RegisterDef:
    return RegisterDef(
        key=key, name=name, address=address, group=group, unit=unit, **_TEMP, **extra
    )  # type: ignore[arg-type]


# --- Controller / Regler -----------------------------------------------------

_REGLER_REGISTERS: list[RegisterDef] = [
    RegisterDef("trovis_r_modell", "Trovis Regler Modell", 0, "regler"),
    RegisterDef(
        "trovis_r_anlage",
        "Trovis Regler Hydraulik (Anlage)",
        1,
        "regler",
        scale=0.1,
        precision=1,
    ),
    RegisterDef(
        "trovis_r_firmware",
        "Trovis Regler Firmwareversion",
        2,
        "regler",
        scale=0.01,
        precision=2,
    ),
    RegisterDef("trovis_r_hardware", "Trovis Regler Hardwareversion", 3, "regler"),
    RegisterDef(
        "trovis_r_sonderfunktionen", "Trovis Regler Sonderfunktionen", 4, "regler"
    ),
    RegisterDef("trovis_r_seriennummer", "Trovis Regler Seriennummer", 5, "regler"),
    RegisterDef("trovis_r_fehlerstatus", "Trovis Regler Fehlerstatus", 149, "regler"),
    RegisterDef("trovis_r_schalteroben", "Trovis Regler Schalter oben", 102, "regler"),
    RegisterDef(
        "trovis_r_schaltermitte", "Trovis Regler Schalter mitte", 103, "regler"
    ),
    RegisterDef(
        "trovis_r_schalterunten", "Trovis Regler Schalter unten", 104, "regler"
    ),
    RegisterDef(
        "trovis_r_sommer_at_min",
        "Trovis Regler AT Grenzwert",
        116,
        "regler",
        data_type="int16",
        scale=0.1,
        precision=1,
        unit="°C",
        device_class="temperature",
        nan_value=32767,
        min_value=0,
        max_value=30,
    ),
    RegisterDef(
        "trovis_r_at_verzoegerung",
        "Trovis Regler AT Verzoegerung",
        117,
        "regler",
        data_type="int16",
        unit="K",
        device_class="temperature",
        min_value=1,
        max_value=6,
    ),
    RegisterDef(
        "trovis_r_schreibzugriff",
        "Trovis Regler Schreibzugriff setzen",
        144,
        "regler",
        writable=True,
    ),
]

# --- Sensors / Messwerte (Fühler) --------------------------------------------

_MESSWERTE_REGISTERS: list[RegisterDef] = [
    _temp("trovis_f_AF1", "Trovis Fühler Außen 1 (AF1)", 9, "messwerte"),
    _temp("trovis_f_AF2", "Trovis Fühler Außen 2 (AF2)", 10, "messwerte"),
    _temp("trovis_f_SF1", "Trovis Fühler Speicher 1 (SF1)", 22, "messwerte"),
    _temp("trovis_f_SF2", "Trovis Fühler Speicher 2 (SF2)", 23, "messwerte"),
    _temp("trovis_f_RF1", "Trovis Fühler Raum 1 (RF1)", 19, "messwerte"),
    _temp("trovis_f_RF2", "Trovis Fühler Raum 2 (RF2)", 20, "messwerte"),
    _temp("trovis_f_RF3", "Trovis Fühler Raum 3 (RF3)", 21, "messwerte"),
    _temp("trovis_f_VF1", "Trovis Fühler Vorlauf 1 (VF1)", 12, "messwerte"),
    _temp("trovis_f_VF2", "Trovis Fühler Vorlauf 2 (VF2)", 13, "messwerte"),
    _temp("trovis_f_VF3", "Trovis Fühler Vorlauf 3 (VF3)", 14, "messwerte"),
    _temp("trovis_f_VF4", "Trovis Fühler Vorlauf 4 (VF4)", 15, "messwerte"),
    _temp("trovis_f_RueF1", "Trovis Fühler Rücklauf 1 (RüF1)", 16, "messwerte"),
    _temp("trovis_f_RueF2", "Trovis Fühler Rücklauf 2 (RüF2)", 17, "messwerte"),
    _temp("trovis_f_RueF3", "Trovis Fühler Rücklauf 3 (RüF3)", 18, "messwerte"),
    _temp("trovis_f_FG1", "Trovis Fühler Ferngeber 1 (FG1)", 25, "messwerte", unit="K"),
    _temp("trovis_f_FG2", "Trovis Fühler Ferngeber 2 (FG2)", 26, "messwerte", unit="K"),
    _temp(
        "trovis_f_SF3_FG3",
        "Trovis Fühler Speicher/Ferngeber 3 (SF3/FG3)",
        24,
        "messwerte",
    ),
]

# --- Heating circuits 1-3 (identical layout, offset by 200 registers) --------

_HK_LABEL = {1: "Hk1", 2: "Hk2", 3: "Hk3"}


def _heating_circuit_registers(n: int) -> list[RegisterDef]:
    group = f"hk{n}"
    label = _HK_LABEL[n]
    base = 1000 + 200 * (n - 1)
    return [
        RegisterDef(
            f"trovis_hk{n}_betriebsart",
            f"Trovis {label} Betriebsart",
            105 + 2 * (n - 1),
            group,
        ),
        RegisterDef(
            f"trovis_hk{n}_stellsignal",
            f"Trovis {label} 3Pkt Stellsignal",
            106 + 2 * (n - 1),
            group,
            data_type="int16",
            nan_value=32767,
        ),
        _temp(f"trovis_hk{n}_vlsoll", f"Trovis {label} VL Soll", base - 1, group),
        _temp(
            f"trovis_hk{n}_raumsoll_tag",
            f"Trovis {label} Raumsoll Tag",
            base + 2,
            group,
        ),
        _temp(
            f"trovis_hk{n}_raumsoll_nacht",
            f"Trovis {label} Raumsoll Nacht",
            base + 3,
            group,
        ),
        _temp(f"trovis_hk{n}_vl_min", f"Trovis {label} VL min", base + 1, group),
        _temp(f"trovis_hk{n}_vl_max", f"Trovis {label} VL max", base, group),
        RegisterDef(
            f"trovis_hk{n}_steigung",
            f"Trovis {label} VL Steigung",
            base + 5,
            group,
            data_type="int16",
            scale=0.1,
            precision=1,
            min_value=0.2,
            max_value=3.2,
            nan_value=32767,
        ),
        _temp(
            f"trovis_hk{n}_niveau",
            f"Trovis {label} VL Niveau",
            base + 6,
            group,
            max_value=30,
        ),
        _temp(
            f"trovis_hk{n}_rl_fusspunkt",
            f"Trovis {label} RL Fusspunkt",
            base + 11,
            group,
        ),
        _temp(f"trovis_hk{n}_rl_niveau", f"Trovis {label} RL Niveau", base + 9, group),
        _temp(
            f"trovis_hk{n}_rl_steigung", f"Trovis {label} RL Steigung", base + 8, group
        ),
        _temp(f"trovis_hk{n}_rl_max", f"Trovis {label} RL max", base + 10, group),
    ]


# --- Heating circuit 4 / hot water -------------------------------------------

_HK4_REGISTERS: list[RegisterDef] = [
    RegisterDef("trovis_hk4_betriebsart", "Trovis Hk4 Betriebsart", 111, "hk4"),
    _temp("trovis_hk4_soll", "Trovis Hk4 SOLL TW", 1799, "hk4"),
    _temp("trovis_hk4_maxsoll", "Trovis Hk4 maxSOLL TW", 1800, "hk4"),
    _temp("trovis_hk4_minsoll", "Trovis Hk4 minSOLL TW", 1801, "hk4"),
    _temp("trovis_hk4_schaltdifferenz", "Trovis Hk4 Schaltdifferenz TW", 1802, "hk4"),
    _temp("trovis_hk4_ueberhoehung", "Trovis Hk4 Ueberhoehung TW", 1803, "hk4"),
    RegisterDef(
        "trovis_hk4_nachlauf_slp",
        "Trovis Hk4 Nachlauf SLP",
        1804,
        "hk4",
        data_type="int16",
        scale=0.1,
        precision=1,
        nan_value=32767,
    ),
    _temp("trovis_hk4_max_ladetemp", "Trovis Hk4 maxLadetemperatur TW", 1805, "hk4"),
    _temp("trovis_hk4_haltewert", "Trovis Hk4 Haltewert TW", 1806, "hk4"),
    _temp("trovis_hk4_max_rl", "Trovis Hk4 maxRL TW", 1827, "hk4"),
    _temp(
        "trovis_hk4_desinfektionstemp",
        "Trovis Hk4 Desinfektionstemperatur TW",
        1829,
        "hk4",
    ),
]

# --- Date / time / schedules -------------------------------------------------

_ZEIT_REGISTERS: list[RegisterDef] = [
    RegisterDef("trovis_z_datum", "Trovis Regler Datum", 100, "zeit"),
    RegisterDef("trovis_z_jahr", "Trovis Regler Jahr", 101, "zeit"),
    RegisterDef("trovis_z_uhrzeit", "Trovis Regler Uhrzeit", 99, "zeit"),
    RegisterDef(
        "trovis_z_hk123_sommer_ein", "Trovis Hk123 Sommerbetrieb ein", 112, "zeit"
    ),
    RegisterDef(
        "trovis_z_hk123_sommer_aus", "Trovis Hk123 Sommerbetrieb aus", 113, "zeit"
    ),
    RegisterDef(
        "trovis_z_hk123_sommer_ein_tage",
        "Trovis Hk123 Sommerbetrieb ein Tage",
        114,
        "zeit",
    ),
    RegisterDef(
        "trovis_z_hk123_sommer_aus_tage",
        "Trovis Hk123 Sommerbetrieb aus Tage",
        115,
        "zeit",
    ),
    RegisterDef(
        "trovis_z_hk4_desinfektionstag", "Trovis Hk4 Desinfektionstag", 1830, "zeit"
    ),
    RegisterDef(
        "trovis_z_hk4_desinfektionsstart", "Trovis Hk4 Desinfektionsstart", 1831, "zeit"
    ),
    RegisterDef(
        "trovis_z_hk4_desinfektionsende", "Trovis Hk4 Desinfektionsende", 1832, "zeit"
    ),
    RegisterDef(
        "trovis_z_hk4_desinfektionsdauer", "Trovis Hk4 Desinfektionsdauer", 1838, "zeit"
    ),
]

REGISTERS: list[RegisterDef] = [
    *_REGLER_REGISTERS,
    *_MESSWERTE_REGISTERS,
    *_heating_circuit_registers(1),
    *_heating_circuit_registers(2),
    *_heating_circuit_registers(3),
    *_HK4_REGISTERS,
    *_ZEIT_REGISTERS,
]


# --- Coils -------------------------------------------------------------------

_REGLER_COILS: list[CoilDef] = [
    CoilDef("trovis_r_sammelstoerung", "Trovis Regler Sammelstoerung", 0, "regler"),
    CoilDef(
        "trovis_r_handbetriebsperrung",
        "Trovis Regler Sperrung Handbetrieb",
        149,
        "regler",
        writable=True,
    ),
    CoilDef(
        "trovis_r_drehschaltersperrung",
        "Trovis Regler Sperrung Drehschalter",
        150,
        "regler",
        writable=True,
    ),
]


def _heating_circuit_coils(n: int) -> list[CoilDef]:
    group = f"hk{n}"
    label = _HK_LABEL[n]
    base = 999 + 200 * (n - 1)
    return [
        CoilDef(
            f"trovis_hk{n}_handbetrieb",
            f"Trovis {label} Handbetrieb",
            4 + (n - 1),
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_automatikbetrieb",
            f"Trovis {label} Automatikbetrieb",
            base,
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_tagbetrieb", f"Trovis {label} Tagbetrieb", base + 1, group
        ),
        CoilDef(
            f"trovis_hk{n}_nachtbetrieb",
            f"Trovis {label} Nachtbetrieb",
            base + 2,
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_haltebetrieb",
            f"Trovis {label} Haltebetrieb",
            base + 3,
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_stuetzbetrieb",
            f"Trovis {label} Stuetzbetrieb",
            base + 4,
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_aufheizbetrieb",
            f"Trovis {label} Aufheizbetrieb",
            base + 5,
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_rlbegrenzung",
            f"Trovis {label} Ruecklauftemperaturbegrenzung",
            base + 6,
            group,
        ),
        CoilDef(
            f"trovis_hk{n}_atabschaltung",
            f"Trovis {label} AT Abschaltung",
            base + 7,
            group,
        ),
        CoilDef(f"trovis_hk{n}_standby", f"Trovis {label} Standby", base + 8, group),
        CoilDef(
            f"trovis_hk{n}_frostschutz", f"Trovis {label} Frostschutz", base + 9, group
        ),
        CoilDef(
            f"trovis_hk{n}_up{n}", f"Trovis {label} Umwaelzpumpe", 56 + (n - 1), group
        ),
    ]


_HK4_COILS: list[CoilDef] = [
    CoilDef("trovis_hk4_handbetrieb", "Trovis Hk4 Handbetrieb", 7, "hk4"),
    CoilDef("trovis_hk4_automatikbetrieb", "Trovis Hk4 Automatikbetrieb", 1799, "hk4"),
    CoilDef("trovis_hk4_desinfektion", "Trovis Hk4 Desinfektion aktiv", 1800, "hk4"),
    CoilDef("trovis_hk4_twvorrang", "Trovis Hk4 TW Vorrang", 1801, "hk4"),
    CoilDef(
        "trovis_hk4_maxladetemp", "Trovis Hk4 Maximale Ladetemperatur", 1802, "hk4"
    ),
    CoilDef(
        "trovis_hk4_rlbegrenzung",
        "Trovis Hk4 Ruecklauftemperaturbegrenzung",
        1803,
        "hk4",
    ),
    CoilDef("trovis_hk4_standby", "Trovis Hk4 Standby", 1804, "hk4"),
    CoilDef("trovis_hk4_frostschutz", "Trovis Hk4 Frostschutz", 1805, "hk4"),
    CoilDef("trovis_hk4_zwangsladung", "Trovis Hk4 Zwangsladung", 1806, "hk4"),
    CoilDef("trovis_hk4_solar_up1", "Trovis Hk4 Solar UP1", 1807, "hk4"),
    CoilDef("trovis_hk4_sf2zwangsladung", "Trovis Hk4 SF2 Zwangsladung", 1808, "hk4"),
    CoilDef(
        "trovis_hk4_zwischenheizbetrieb", "Trovis Hk4 Zwischenheizbetrieb", 1830, "hk4"
    ),
    CoilDef("trovis_hk4_slp", "Trovis HK4 Speicherladepumpe", 59, "hk4"),
    CoilDef("trovis_hk4_zp", "Trovis HK4 Zirkulationspumpe", 60, "hk4"),
]

_ZEIT_COILS: list[CoilDef] = [
    CoilDef(
        "trovis_r_autosommerzeit",
        "Trovis Regler Auto Sommerzeit",
        136,
        "zeit",
        writable=True,
    ),
    CoilDef("trovis_r_sommerbetrieb", "Trovis Regler Sommerbetrieb", 8, "zeit"),
]

COILS: list[CoilDef] = [
    *_REGLER_COILS,
    *_heating_circuit_coils(1),
    *_heating_circuit_coils(2),
    *_heating_circuit_coils(3),
    *_HK4_COILS,
    *_ZEIT_COILS,
]


# --- Derived (template) values -----------------------------------------------
# Device-meaningful values computed from registers/coils. Pure-UI template
# sensors from the YAML (button clicks, gesamtstatus, *_sim_*) are intentionally
# excluded: they depend on dashboard input_number helpers, not the device.

DERIVED: list[DerivedDef] = [
    DerivedDef("trovis_z_datum_formatiert", "Trovis Regler Datum (formatiert)", "zeit"),
    DerivedDef(
        "trovis_z_sommerbetrieb_ein_formatiert",
        "Trovis Sommerbetrieb ein (formatiert)",
        "zeit",
    ),
    DerivedDef(
        "trovis_z_sommerbetrieb_aus_formatiert",
        "Trovis Sommerbetrieb aus (formatiert)",
        "zeit",
    ),
    DerivedDef(
        "trovis_z_uhrzeit_formatiert", "Trovis Regler Uhrzeit (formatiert)", "zeit"
    ),
    DerivedDef(
        "trovis_z_hk4_desinfektionstag_formatiert",
        "Trovis Hk4 Desinfektionstag (formatiert)",
        "zeit",
    ),
    DerivedDef(
        "trovis_z_hk4_desinfektionsstart_formatiert",
        "Trovis HK4 Desinfektionsstart (formatiert)",
        "zeit",
    ),
    DerivedDef(
        "trovis_z_hk4_desinfektionsende_formatiert",
        "Trovis HK4 Desinfektionsende (formatiert)",
        "zeit",
    ),
    DerivedDef(
        "trovis_z_hk4_desinfektionsdauer_formatiert",
        "Trovis HK4 Desinfektionsdauer (formatiert)",
        "zeit",
    ),
    DerivedDef(
        "trovis_r_schalter_oben_formatiert",
        "Trovis Schalter oben (formatiert)",
        "regler",
    ),
    DerivedDef(
        "trovis_r_schalter_mitte_formatiert",
        "Trovis Schalter mitte (formatiert)",
        "regler",
    ),
    DerivedDef(
        "trovis_r_schalter_unten_formatiert",
        "Trovis Schalter unten (formatiert)",
        "regler",
    ),
    DerivedDef(
        "trovis_hk1_betriebsart_formatiert",
        "Trovis Hk1 Betriebsart (formatiert)",
        "hk1",
    ),
    DerivedDef(
        "trovis_hk2_betriebsart_formatiert",
        "Trovis Hk2 Betriebsart (formatiert)",
        "hk2",
    ),
    DerivedDef(
        "trovis_hk3_betriebsart_formatiert",
        "Trovis Hk3 Betriebsart (formatiert)",
        "hk3",
    ),
    DerivedDef(
        "trovis_hk4_betriebsart_formatiert",
        "Trovis Hk4 Betriebsart (formatiert)",
        "hk4",
    ),
    DerivedDef("trovis_hk4_tagestemperaturen", "Trovis Hk4 Tagestemperaturen", "hk4"),
    DerivedDef("trovis_hk4_nachttemperaturen", "Trovis Hk4 Nachttemperaturen", "hk4"),
    DerivedDef("trovis_hk4_ladetemperatur", "Trovis Hk4 Ladetemperatur", "hk4"),
    DerivedDef("trovis_hk123_heizkurven", "Trovis Hk123 Heizkurven", "hk1"),
]

REGISTERS_BY_KEY: dict[str, RegisterDef] = {r.key: r for r in REGISTERS}
COILS_BY_KEY: dict[str, CoilDef] = {c.key: c for c in COILS}
ALL_KEYS: list[str] = (
    [r.key for r in REGISTERS] + [c.key for c in COILS] + [d.key for d in DERIVED]
)
