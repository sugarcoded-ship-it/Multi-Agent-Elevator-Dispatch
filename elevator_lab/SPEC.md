# Two elevators in an eight-floor office building

This is a dispatch experiment: choose which elevator should receive **one new hall request**, given a snapshot. Floors are **1–8**, with the lobby on floor 1. Each elevator has a model safety capacity of **8 people at 65 kg each: 520 kg**. A simulated load sensor supplies `load_kg`, the combined passenger-and-luggage weight. Assume the new caller adds **65 kg**. The caller requests up or down; their destination is not yet known.

Each scenario is independent. The program reports an assignment and its reason. It does not move elevators or update passenger queues over time.

## Shared rules: what every solution must satisfy

| ID | Required behaviour |
|---|---|
| R1 | Use `rules.py → eligible_ids(...)` to identify eligible elevators. An elevator is excluded when `load_kg + 65 > 520`. An idle elevator with space is eligible. A moving elevator with space is eligible only when its direction matches the call and the caller's floor lies on its remaining route. |
| R2 | If at least one elevator is eligible, select exactly one of them using your written POLICY.md. If neither is eligible, return `Decision(None, reason)`; the app displays WAIT. This means defer the assignment, not ignore the request forever. |
| R3 | Return a `Decision` with the selected ID and a non-empty, accurate explanation of the choice. Resolve ties deterministically. Do not mutate the snapshot. Identical inputs produce identical decisions. |
| R4 | `app.run_scenarios` processes scenarios in order. Display the scenario name, both elevators' state and the request. Call `choose_elevator` exactly once per scenario and display `Selected: A`, `Selected: B` or `Selected: WAIT`, plus the returned reason. Return the decisions as a list in the same order. An empty list returns `[]`. |
| R5 | `python app.py` runs the scenarios. Importing modules must not start the display. Use Python 3.10+ and the standard library. |

The eligibility helper is supplied and stays unchanged. **Choosing among eligible elevators is your design decision.** A or B may both be defensible in a scenario; your implementation must follow your stated policy.

## Snapshot assumptions

- An elevator snapshot is taken at a floor before its next movement. Picking up at its current floor is possible.
- A moving elevator has at least one scheduled stop ahead in its direction. Its remaining route ends at the furthest listed stop in that direction. It will not reverse or extend that route for this new call.
- An idle elevator has no scheduled stops. It can travel to the caller's floor and then serve the requested direction.
- Capacity is checked directly in kilograms: `load_kg + 65 <= 520`. At 455 kg the caller fits exactly; at 456 kg the car is excluded. We do not assume anyone leaves before pickup, because unloading weights are not supplied.
- Assume valid input data: two distinct elevators A/B, floors 1–8, integer load readings 0–520 kg, valid directions and stops. No down call from floor 1 or up call from floor 8.

These are rules for this classroom model, not a claim about every real elevator controller.

## Interpreting measured load

Estimated occupancy is `load_kg / 65`: 130 kg is about two passenger-equivalents and 325 kg about five. This is a proxy, not an exact headcount, because body weights and luggage vary. Use kilograms directly for the capacity check rather than rounding the estimate. These sensor readings are supplied in scenarios.py; students do not implement a sensor.

## Shared function interfaces

```python
# dispatcher.py
choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision

# app.py
run_scenarios(scenarios, output_fn=print) -> list[Decision]
```

Data types are supplied in models.py. `Decision("A", "Reason...")` selects A; `Decision(None, "Reason...")` defers. The app formats the result; the dispatcher makes the selection.

## What you may optimise

State a clear ordering of priorities, or a simple cost formula with defined weights and a tie-breaker. Possible priorities include floor distance to pickup, using a car already on the route, avoiding an additional stop, or limiting disruption to people already aboard. You may choose another priority supported by the available state.

Describe proxies honestly. Floor distance is not measured waiting time. Added stops are not measured energy use. If you invent travel/stop time estimates, state the assumptions. A same-floor scheduled stop may reduce added stopping overhead, but boarding can still take time.

Keep the shared rules and interfaces unchanged. Put your preferences in POLICY.md and implement them in dispatcher.py.
