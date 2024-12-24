import time
import numpy as np
from optimized_mac.mac import OptimizedMAC
import hmac
import hashlib
from cryptography.hazmat.primitives import hashes, hmac as crypto_hmac
from optimized_mac.utils import get_process_usage


def run_benchmark(message_sizes, num_iterations=100):
    key = b'secret_key_12345'

    def crypto_hmac_generate(message):
        h = crypto_hmac.HMAC(key, hashes.SHA256())
        h.update(message)
        return h.finalize()

    implementations = {
        'Traditional HMAC': lambda m: hmac.new(key, m, hashlib.sha256).digest(),
        'Optimized MAC': lambda m: OptimizedMAC(key).generate(m),
        'Crypto HMAC': crypto_hmac_generate
    }

    results = {'time': {}, 'memory': {}, 'cpu': {}}

    for size in message_sizes:
        message = b'A' * size
        print(f"\nProcessing message size: {size} bytes")

        for impl_name, impl_func in implementations.items():
            print(f"  Running implementation: {impl_name}")
            times, memory_usage, cpu_percent = [], [], []

            for _ in range(num_iterations):
                import gc
                gc.collect()

                start_cpu, start_mem = get_process_usage()
                start_time = time.perf_counter_ns()

                impl_func(message)

                end_time = time.perf_counter_ns()
                end_cpu, end_mem = get_process_usage()

                times.append((end_time - start_time) / 1e9)
                cpu_percent.append((end_cpu - start_cpu) * 100)
                memory_usage.append(end_mem - start_mem)

            avg_time = np.mean(times)
            avg_memory = np.mean(memory_usage)
            avg_cpu = np.mean(cpu_percent)

            results['time'].setdefault(impl_name, []).append(avg_time)
            results['memory'].setdefault(impl_name, []).append(avg_memory)
            results['cpu'].setdefault(impl_name, []).append(avg_cpu)

            print(f"    Avg Time: {avg_time * 1e6:.2f} µs")
            print(f"    Avg Memory: {avg_memory:.0f} bytes")
            print(f"    Avg CPU: {avg_cpu:.6f}%")

    return results
