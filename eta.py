"""
Authors : inzapp

Github url : https://github.com/inzapp/eta-calculator

Copyright (c) 2023 Inzapp

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from time import perf_counter


class EtaCalculator:
    def __init__(self, iterations, buffer_size=100):
        self.iterations = iterations
        self.start_time = 0
        self.recent_times = []
        self.recent_iterations = []
        self.buffer_size = buffer_size

    def start(self):
        self.start_time = perf_counter()
        self.recent_iterations.append(0)
        self.recent_times.append(perf_counter())

    def end(self, return_sec=False):
        avg_ips = float(self.iterations) / (perf_counter() - self.start_time)
        elapsed_time = perf_counter() - self.start_time
        if return_sec:
            elapsed_time = elapsed_time
        else:
            elapsed_time = self.convert_to_time_str(int(elapsed_time))
        return avg_ips, elapsed_time

    def reset(self):
        self.recent_times = []
        self.recent_iterations = []

    def update_buffer(self, iteration_count):
        self.recent_times.append(perf_counter())
        self.recent_iterations.append(iteration_count)
        if len(self.recent_times) > self.buffer_size:
            self.recent_times.pop(0)
        if len(self.recent_iterations) > self.buffer_size:
            self.recent_iterations.pop(0)

    def convert_to_time_str(self, total_sec):
        times = []
        hh = total_sec // 3600
        times.append(str(hh).rjust(2, '0'))
        total_sec %= 3600
        mm = total_sec // 60
        times.append(str(mm).rjust(2, '0'))
        total_sec %= 60
        ss = total_sec
        times.append(str(ss).rjust(2, '0'))
        return ':'.join(times)

    def calculate(self, iteration_count, return_sec=False):
        self.update_buffer(iteration_count)
        elapsed_sec = self.recent_times[-1] - self.recent_times[0]
        total_iterations = iteration_count - self.recent_iterations[0]
        ips = total_iterations / elapsed_sec
        eta = (self.iterations - iteration_count) / ips
        elapsed_time = perf_counter() - self.start_time
        per = int(iteration_count / float(self.iterations) * 1000.0) / 10.0
        if return_sec:
            eta = eta
            elapsed_time = elapsed_time
        else:
            eta = self.convert_to_time_str(int(eta))
            elapsed_time = self.convert_to_time_str(int(elapsed_time))
        return eta, ips, elapsed_time, per


if __name__ == '__main__':
    from time import sleep
    total_iterations = 300
    eta_calculator = EtaCalculator(iterations=total_iterations)
    eta_calculator.start()
    iteration_count = 0
    while True:
        sleep(0.01)
        iteration_count += 1
        eta, ips, elapsed_time, per = eta_calculator.calculate(iteration_count)
        print(f'\r({per:.1f}%) [iteration: {iteration_count}/{total_iterations}] {elapsed_time}<{eta}, {ips:.2f}it/s', end='')
        if iteration_count == total_iterations:
            break
    avg_ips, elapsed_time = eta_calculator.end()
    eta_calculator.reset()
    print(f'\ntotal {total_iterations} iterations end successfully with avg IPS {avg_ips:.1f}, elapsed time : {elapsed_time}')

