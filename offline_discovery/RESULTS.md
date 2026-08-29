# Offline Discovery Results

## Experiment

The system receives five local observations of a hidden deterministic function and no rule definition. Internet/network access is blocked. Three additional observations are withheld until after hypothesis generation.

Hidden benchmark rule (not supplied to the discovery procedure): `y = 3*x^2 + 2*x - 5`.

## Observed result

| Metric | Result |
|---|---:|
| Network isolated | PASS |
| Local training observations | 5 |
| Held-out observations | 3 |
| Discovered coefficients | `(-5, 2, 3)` |
| Discovered degree | 2 |
| Held-out predictions | `[28, 51, 80]` |
| Expected held-out values | `[28, 51, 80]` |
| Exact generalization | PASS |
| Knowledge persisted | PASS |

## Interpretation

The experiment demonstrates **closed-world rule discovery**: a bounded discovery engine can infer a previously hidden rule from local observations and produce predictions that exactly generalize to unseen observations without internet retrieval.

It does **not** prove open-ended scientific discovery or AGI. The hypothesis space is deliberately bounded and the environment is synthetic. The next research step is to replace the polynomial search with a richer local simulator and connect the experiment to the production PrometheusAgent/MetaMind interface, including an independent verifier and repeated hypothesis/experiment cycles.

## Reproducibility

Run:

```bash
python -m unittest offline_discovery.test_benchmark -v
python -m unittest offline_discovery.test_integration -v
python -m offline_discovery.benchmark
python -m offline_discovery.offline_agent
```

CI executes the same benchmark and integration test on the feature branch and pull requests.
