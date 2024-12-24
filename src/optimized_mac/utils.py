import psutil


def get_process_usage():
    process = psutil.Process()
    cpu = process.cpu_times().user + process.cpu_times().system
    memory = process.memory_info().rss
    return cpu, memory
