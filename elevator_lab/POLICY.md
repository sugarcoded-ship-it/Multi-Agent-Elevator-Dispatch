# My dispatch policy

## Priorities

- What I prioritise: the passengers already inside a moving elevator. They should not be delayed by an extra stop for a new caller when a free (idle) elevator can take the call instead.
- My exact selection rule (applied only after `eligible_ids`):
  1. If no elevator is eligible, return WAIT (`Decision(None, reason)`).
  2. If only one elevator is eligible, select it.
  3. If both are eligible and exactly one is idle, select the idle elevator, even if it is farther from the caller. Load and an already-scheduled stop at the caller's floor do not change this.
  4. If both are eligible and both are idle, or both are moving, go to the tie-breaker.
- My deterministic tie-breaker:
  1. Select the elevator with the lower `load_kg`.
  2. If the loads are equal, select A.
- A tradeoff I accept: the caller may wait longer. If a moving car is very close (or already stopping at the caller's floor) and the idle car is far away, my rule still sends the idle car. Example: A at floor 6 going down with a stop at 5, B idle at floor 1, call at 5 down → my rule sends B up 4 floors, and the lobby loses its free car.

## Predictions before implementation

| Scenario | My expected selection | Why it follows my policy | Benefit and cost / who is affected |
|---|---|---|---|
| S1 | B | Both eligible; B is idle and A is moving, so the idle car wins (rule 3). | Benefit: A's 2 passengers are not delayed by an extra stop. Cost: B leaves floor 4 and is no longer free for other calls. |
| S3 | B | Both eligible; B is idle, so it wins. A's scheduled stop at 5 does not change my rule. | Benefit: A stays lighter and B is only 1 floor away. Cost: A was stopping at 5 anyway, so using B adds a trip that wasn't strictly needed. |
| S6: A starts at floor 6 instead of 8 | B | Both eligible (A: 195 kg ≤ 520, going down, and 5 is between its floor 6 and its stop 1; B: idle). B is idle, so it wins (rule 3). Both cars are only 1 floor from the caller, so distance would not separate them anyway. | Benefit: A's 2 passengers are not delayed. Cost: A passes floor 5 almost immediately, so the caller would wait about the same with either car, but B gives up being free. |

## Another defensible policy

- An alternative priority: use the car that is already passing. If a moving car is eligible, prefer it over an idle car, so idle cars stay free for other calls and no extra trip is started.
- A scenario where it could choose differently, and why: in S1 and S3 this alternative would select A, because A is already travelling down past floor 5 (and in S3 already stopping there). My policy selects B in both, because I care more about not delaying A's passengers.
