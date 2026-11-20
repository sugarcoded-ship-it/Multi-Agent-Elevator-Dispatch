"""Builder 1 implements the student's policy here."""
from models import Elevator, Request, Decision
from rules import eligible_ids

def choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision:
    """Choose one eligible elevator according to POLICY.md; never mutate inputs."""
    eligible_set = set(eligible_ids(elevators, request))
    candidates = [e for e in elevators if e.id in eligible_set]

    # Rule 1: no eligible elevator -> WAIT.
    if not candidates:
        return Decision(None, "Rule 1: no elevator is eligible (full, or moving the wrong way / caller not on its route); defer the call.")

    # Rule 2: exactly one eligible elevator -> select it.
    if len(candidates) == 1:
        only = candidates[0]
        return Decision(only.id, f"Rule 2: {only.id} is the only eligible elevator.")

    # Rule 3: both eligible and exactly one idle -> select the idle elevator.
    idle = [e for e in candidates if e.direction == "idle"]
    if len(idle) == 1:
        chosen = idle[0]
        moving = next(e for e in candidates if e is not chosen)
        reason = (f"Rule 3: both eligible; {chosen.id} is the only idle elevator, and my policy "
                  f"prefers an idle car over a moving one so the moving car's passengers get no extra pickup")
        if request.floor in moving.stops:
            reason += (f" ({moving.id} already stops at floor {request.floor}, "
                       f"but the idle car is still preferred)")
        return Decision(chosen.id, reason + ".")

    # Rule 4: both idle or both moving -> tie-breaker: lower load_kg, then A.
    state = "idle" if len(idle) == 2 else "moving"
    first, second = candidates
    if first.load_kg != second.load_kg:
        chosen = min(candidates, key=lambda e: e.load_kg)
        return Decision(chosen.id, f"Rule 4 tie-breaker: both eligible and both {state}; {chosen.id} has the lower load ({chosen.load_kg} kg).")
    chosen = "A" if any(e.id == "A" for e in candidates) else min(e.id for e in candidates)
    return Decision(chosen, f"Rule 4 tie-breaker: both eligible and both {state} with equal load ({first.load_kg} kg); select A.")
