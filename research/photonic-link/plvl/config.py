"""Strict, unit-bearing configuration; all defaults are synthetic assumptions."""
from dataclasses import dataclass, field, fields, asdict
import math


def number(value, name, low=-math.inf, high=math.inf):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: finite number required")
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name}: outside [{low}, {high}]")


def integer(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{name}: integer in [{low}, {high}] required")


@dataclass(frozen=True)
class Clock:
    offset_s: float = 0.0
    skew_ppm: float = 0.0
    drift_ppm_per_s: float = 0.0
    tick_ps: int = 100

    def validate(self):
        number(self.offset_s, "offset_s", -1, 1)
        number(self.skew_ppm, "skew_ppm", -1000, 1000)
        number(self.drift_ppm_per_s, "drift_ppm_per_s", -100, 100)
        integer(self.tick_ps, "tick_ps", 1, 10**9)


@dataclass(frozen=True)
class Arm:
    length_km: float = 1.0
    attenuation_db_per_km: float = 0.2
    insertion_loss_db: float = 1.0
    coupling: float = 0.7
    detector_efficiency: float = 0.7
    dark_rate_per_port_hz: float = 100.0
    dead_time_s: float = 50e-9
    jitter_sigma_s: float = 200e-12
    group_index: float = 1.468
    electronics_delay_s: float = 0.0
    loss_db_per_environment: float = 0.0
    delay_s_per_environment: float = 0.0
    rotation_y_rad: float = 0.0
    rotation_z_rad: float = 0.0
    rotation_y_rate_rad_per_s: float = 0.0
    rotation_y_rad_per_environment: float = 0.0
    rotation_z_rad_per_environment: float = 0.0
    dephasing_probability: float = 0.0
    analyzer_angle_deg: float = 0.0
    clock: Clock = field(default_factory=Clock)

    def validate(self):
        bounds = {
            "length_km": (0, 1000), "attenuation_db_per_km": (0, 100),
            "insertion_loss_db": (0, 1000), "coupling": (0, 1),
            "detector_efficiency": (0, 1), "dark_rate_per_port_hz": (0, 1e7),
            "dead_time_s": (0, 1), "jitter_sigma_s": (0, 1e-3),
            "group_index": (1, 10), "electronics_delay_s": (0, .1),
            "loss_db_per_environment": (-100, 100),
            "delay_s_per_environment": (-1e-3, 1e-3),
            "rotation_y_rad": (-1e6, 1e6), "rotation_z_rad": (-1e6, 1e6),
            "rotation_y_rate_rad_per_s": (-1e6, 1e6),
            "rotation_y_rad_per_environment": (-1e6, 1e6),
            "rotation_z_rad_per_environment": (-1e6, 1e6),
            "dephasing_probability": (0, 1), "analyzer_angle_deg": (-360, 360),
        }
        for key, (low, high) in bounds.items():
            number(getattr(self, key), key, low, high)
        if not isinstance(self.clock, Clock):
            raise ValueError("Clock object required")
        self.clock.validate()


@dataclass(frozen=True)
class Experiment:
    schema: str = "plvl.config.v1"
    provenance: str = "synthetic_design_assumption"
    duration_ps: int = 100_000_000_000
    window_ps: int = 2000
    cell_ps: int = 5_000_000_000
    pair_rate_hz: float = 200_000.0
    singlet_visibility: float = 0.98
    environment_sigma: float = 1.0
    environment_tau_s: float = 0.1
    calibration_anchors: int = 101
    calibration_jitter_sigma_s: float = 100e-12
    seed: int = 1701
    arm_a: Arm = field(default_factory=Arm)
    arm_b: Arm = field(default_factory=Arm)

    @property
    def duration_s(self):
        return self.duration_ps * 1e-12

    def validate(self):
        if self.schema != "plvl.config.v1" or self.provenance != "synthetic_design_assumption":
            raise ValueError("Only explicit v1 synthetic configurations supported")
        integer(self.duration_ps, "duration_ps", 1, 10**13)
        integer(self.window_ps, "window_ps", 1, self.duration_ps)
        integer(self.cell_ps, "cell_ps", 1, self.duration_ps)
        if self.duration_ps % self.window_ps or self.duration_ps % self.cell_ps:
            raise ValueError("Duration must contain integer numbers of bins and model cells")
        if self.duration_ps // self.cell_ps > 10000:
            raise ValueError("At most 10000 model cells")
        number(self.pair_rate_hz, "pair_rate_hz", 0, 1e8)
        number(self.singlet_visibility, "singlet_visibility", 0, 1)
        number(self.environment_sigma, "environment_sigma", 0, 10)
        number(self.environment_tau_s, "environment_tau_s", 1e-9, 1e6)
        number(self.calibration_jitter_sigma_s, "calibration_jitter_sigma_s", 0, 1e-3)
        integer(self.calibration_anchors, "calibration_anchors", 5, 10001)
        if self.calibration_anchors % 2 != 1:
            raise ValueError("Odd anchor count: both endpoints belong to training")
        integer(self.seed, "seed", 0, 2**63-1)
        for arm in (self.arm_a, self.arm_b):
            if not isinstance(arm, Arm):
                raise ValueError("Arm object required")
            arm.validate()
        expected = self.duration_s * (self.pair_rate_hz +
                    2*(self.arm_a.dark_rate_per_port_hz+self.arm_b.dark_rate_per_port_hz))
        if expected > 2_000_000:
            raise ValueError("v0.1 in-memory simulation limited to 2 million expected arrivals")
        return self

    def to_dict(self):
        return asdict(self)


def strict_construct(cls, obj):
    if not isinstance(obj, dict):
        raise ValueError(f"{cls.__name__}: JSON object required")
    allowed = {f.name for f in fields(cls)}
    if obj.keys() - allowed:
        raise ValueError(f"Unknown {cls.__name__} fields: {sorted(obj.keys()-allowed)}")
    data = dict(obj)
    if cls is Experiment:
        for key in ("arm_a", "arm_b"):
            if key in data:
                data[key] = strict_construct(Arm, data[key])
    if cls is Arm and "clock" in data:
        data["clock"] = strict_construct(Clock, data["clock"])
    return cls(**data)


def from_dict(obj):
    return strict_construct(Experiment, obj).validate()
