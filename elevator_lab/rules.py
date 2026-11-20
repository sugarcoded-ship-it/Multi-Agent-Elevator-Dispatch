"""Supplied eligibility rules. Preferences belong in dispatcher.py."""
from models import Elevator, Request

MAX_LOAD_KG = 520
ASSUMED_PASSENGER_KG = 65

def eligible_ids(elevators: tuple[Elevator, Elevator], request: Request) -> list[str]:
    result = []
    for elevator in elevators:
        if elevator.load_kg + ASSUMED_PASSENGER_KG > MAX_LOAD_KG:
            continue
        if elevator.direction == "idle":
            result.append(elevator.id)
        elif elevator.direction == request.direction and elevator.stops:
            if elevator.direction == "up" and elevator.floor <= request.floor <= max(elevator.stops):
                result.append(elevator.id)
            elif elevator.direction == "down" and min(elevator.stops) <= request.floor <= elevator.floor:
                result.append(elevator.id)
    return result
