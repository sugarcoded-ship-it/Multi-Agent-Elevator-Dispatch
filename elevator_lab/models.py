"""Supplied snapshot data types. Floors are 1–8; floor 1 is the lobby."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Elevator:
    id: str
    floor: int
    direction: str  # "idle", "up", "down"
    load_kg: int   # simulated sensor reading: passengers + luggage, 0–520 kg
    stops: tuple[int, ...] = ()  # remaining scheduled stops

@dataclass(frozen=True)
class Request:
    floor: int
    direction: str  # "up" or "down"; destination is not known

@dataclass(frozen=True)
class Decision:
    elevator_id: str | None  # "A", "B", or None when neither is eligible
    reason: str

@dataclass(frozen=True)
class Scenario:
    name: str
    elevators: tuple[Elevator, Elevator]
    request: Request
