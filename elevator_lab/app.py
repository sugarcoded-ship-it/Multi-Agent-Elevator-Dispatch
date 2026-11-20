"""Builder 2 implements a readable scenario display here."""
from dispatcher import choose_elevator
from scenarios import SCENARIOS
from models import Decision

def run_scenarios(scenarios, output_fn=print) -> list[Decision]:
    """Show each snapshot, call the dispatcher once, display and return decisions."""
    raise NotImplementedError("Implement the scenario display")

if __name__ == "__main__":
    run_scenarios(SCENARIOS)
