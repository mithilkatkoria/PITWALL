# Final computational evidence plan

This verification work follows the 63-page master. It is not a stakeholder-driven development iteration. Existing test outputs and application code will be retained.

SC05: use the recorded five-lap fixture and independent expected lap times 92, 114.2, 92, 91.55 and 91.1 seconds. Check every lap and cumulative time with absolute error <= 1e-9 seconds, no relative tolerance, and exact deterministic replay. Preserve printed differences, JUnit XML, command and source hashes using the existing runner. Then run the full suite.

Comparison latency: time compare() alone for 2 strategies x 50 laps, 20 x 50 and the maximum 20 x 500. Construct inputs before timing. Warm up once per size and measure five repeats with perf_counter. Retain all values, minimum, maximum, mean and median. No GUI latency or human responsiveness claim follows from these measurements. No retrospective pass threshold is invented.

SC04 and SC14 human interpretation and responsiveness remain uncompleted. A prospective software iteration requires actual feedback and a design recorded before implementation.
