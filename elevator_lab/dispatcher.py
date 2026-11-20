"""Builder 1 implements the student's policy here."""
from models import Elevator, Request, Decision
from rules import eligible_ids

def choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision:
    """Choose one eligible elevator according to POLICY.md; never mutate inputs."""
    raise NotImplementedError("Implement the policy in POLICY.md")
