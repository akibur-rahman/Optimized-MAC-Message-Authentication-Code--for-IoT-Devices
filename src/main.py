from benchmarks.benchmark import run_benchmark
from benchmarks.plot import plot_results

if __name__ == "__main__":
    message_sizes = [64, 256, 1024, 4096, 16384]
    num_iterations = 100

    print("Starting benchmark...")
    print(f"Message sizes: {message_sizes}")
    print(f"Number of iterations per message size: {num_iterations}\n")

    results = run_benchmark(message_sizes, num_iterations)

    print("\nBenchmark completed!")
    print("\nSummary of results (average per message size):")
    for metric, data in results.items():
        print(f"\n{metric.capitalize()}:")
        for impl, values in data.items():
            print(f"  {impl}: {values}")

    print("\nPlotting results...")
    plot_results(results, message_sizes)
    print("Plots generated!")
