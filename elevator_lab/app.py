"""Builder 2 implements a readable scenario display here."""
from dispatcher import choose_elevator
from scenarios import SCENARIOS
from models import Decision


def _format_elevator(elevator) -> str:
    """Describe one elevator snapshot for display (no dispatch logic)."""
    stops = ", ".join(str(stop) for stop in elevator.stops) if elevator.stops else "none"
    return (
        f"  Elevator {elevator.id}: floor {elevator.floor}, {elevator.direction}, "
        f"load {elevator.load_kg} kg, stops: {stops}"
    )


def run_scenarios(scenarios, output_fn=print) -> list[Decision]:
    """Show each snapshot, call the dispatcher once, display and return decisions."""
    decisions: list[Decision] = []
    for scenario in scenarios:
        output_fn(f"=== {scenario.name} ===")
        for elevator in scenario.elevators:
            output_fn(_format_elevator(elevator))
        request = scenario.request
        output_fn(f"  Request: floor {request.floor}, going {request.direction}")

        decision = choose_elevator(scenario.elevators, scenario.request)
        selected = decision.elevator_id if decision.elevator_id is not None else "WAIT"
        output_fn(f"Selected: {selected}")
        output_fn(f"Reason: {decision.reason}")
        output_fn("")
        decisions.append(decision)
    return decisions


if __name__ == "__main__":
    run_scenarios(SCENARIOS)
