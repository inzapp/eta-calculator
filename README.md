# ETA calculator
The ETA calculator is a simple utility that provides status information for python loops

Predicts ETA based on the time spent to date when looping

The difference from tqdm is that predictions for looping can be returned as variable

## Usage

How to use it is as follows

``` python
total_iterations = 500
eta_calculator = EtaCalculator(iterations=total_iterations)
eta_calculator.start()
for i in range(total_iterations):
    # your task here
    progress_str = eta_calculator.update(i + 1)
    print(progress_str)
avg_ips, elapsed_time = eta_calculator.end()
eta_calculator.reset()
print(f'\ntotal {total_iterations} iterations end successfully with avg IPS {avg_ips:.1f}, elapsed time : {elapsed_time}')
```

If you run the snippet above, it will be output as follows

If you simply change the commented line to time.sleep(0.1) and run it, it will be executed as follows

```
[Iteration: 1/500(0.2%), 10.06it/s, 00:00:00<00:00:49]
[Iteration: 2/500(0.4%), 10.00it/s, 00:00:00<00:00:49]
[Iteration: 3/500(0.6%), 9.99it/s, 00:00:00<00:00:49]
...
[Iteration: 498/500(99.6%), 9.94it/s, 00:00:50<00:00:00]
[Iteration: 499/500(99.8%), 9.94it/s, 00:00:50<00:00:00]
[Iteration: 500/500(100.0%), 9.94it/s, 00:00:50<00:00:00]

total 500 iterations end successfully with avg IPS 9.9, elapsed time : 00:00:50
```

## Nested loop

ETACalculator can be useful for benchmarking in a nested loop

If you know only the total iteration of the Nested loop, you can benchmark it as if you were measuring one loop

```python
loop_iters_1 = 50
loop_iters_2 = 50
total_iterations = loop_iters_1 * loop_iters_2
eta_calculator = EtaCalculator(iterations=total_iterations)
iteration_count = 0
eta_calculator.start()
for _ in range(loop_iters_1):
    for _ in range(loop_iters_2):
        # your task here
        iteration_count += 1
        progress_str = eta_calculator.update(iteration_count)
```
