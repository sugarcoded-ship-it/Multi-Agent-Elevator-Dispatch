"""Supplied independent snapshots. Add your own scenario at the end."""
from models import Elevator, Request, Scenario

SCENARIOS = [
    Scenario("S1 Passing car or idle car?", (
        Elevator("A", 8, "down", 130, (1,)),
        Elevator("B", 4, "idle", 0),
    ), Request(5, "down")),
    Scenario("S2 Heavier load aboard", (
        Elevator("A", 8, "down", 325, (1,)),
        Elevator("B", 4, "idle", 0),
    ), Request(5, "down")),
    Scenario("S3 A already stops there", (
        Elevator("A", 8, "down", 130, (5, 1)),
        Elevator("B", 4, "idle", 0),
    ), Request(5, "down")),
    Scenario("S4 Nearest car is full", (
        Elevator("A", 6, "down", 520, (1,)),
        Elevator("B", 2, "idle", 0),
    ), Request(5, "down")),
    Scenario("S5 Neither can serve now", (
        Elevator("A", 6, "up", 130, (8,)),
        Elevator("B", 4, "down", 520, (1,)),
    ), Request(5, "down")),
    Scenario("S6 Passing car one floor away", (
        Elevator("A", 6, "down", 130, (1,)),
        Elevator("B", 4, "idle", 0),
    ), Request(5, "down")),
]
