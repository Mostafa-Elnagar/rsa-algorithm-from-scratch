import multiprocessing
import os
import random

NUM_CORES = os.cpu_count()
# Subtract 1 to account for the main thread
THREAD_MAX = NUM_CORES - 1 if NUM_CORES is not None else 1

def _search_number(start, end, e, phi, result_value, stop_event):
    while True:
        d = random.randrange(start, end)
        # Check if the number satisfies the condition
        if (d * e) % phi == 1:
            result_value.value = d
            stop_event.set()
            break
        

def _run_processes(num_processes, e, phi):
    # Create a shared value and event for communication and synchronization
    result_value = multiprocessing.Value('i', -1)
    stop_event = multiprocessing.Event()

    # Calculate the range for each process
    start = 2 
    end = phi
    step = (end - start) // num_processes

    # Create a list to store the process objects
    processes = []

    # Create and start the processes
    for i in range(num_processes):
        process_start = start + i * step
        process_end = process_start + step if i < num_processes - 1 else end
        process = multiprocessing.Process(target=_search_number, args=(process_start, process_end, e, phi, result_value, stop_event))
        processes.append(process)
        process.start()

    # Wait for the stop event to be set by any process
    stop_event.wait()

    # Terminate all other processes
    for process in processes:
        process.terminate()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Retrieve the result
    d = result_value.value
    
    return d

def gen_private(e, phi, num_processes):
    return _run_processes(num_processes, e, phi)