import os
import time
import threading
import multiprocessing

def search_files(file_paths, keywords):
    result = {keyword: [] for keyword in keywords}
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file_path)
        except FileNotFoundError:
            print(f"File not found.")
        except PermissionError:
            print(f"Permission denied")
    return result


def threading_search(file_paths, keywords):
    num_threads = 16
    threads = []
    result = {keyword: [] for keyword in keywords}
    for i in range(num_threads):
        thread_file_paths = file_paths[i::num_threads]
        thread = threading.Thread(target=lambda: result.update(search_files(thread_file_paths, keywords)))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return result

def update_result(result, file_paths, keywords):
    result.update(search_files(file_paths, keywords))

def multiprocessing_search(file_paths, keywords):
    num_processes = 16
    with multiprocessing.Manager() as manager:
        result = manager.dict({keyword: manager.list() for keyword in keywords})
        processes = []
        for i in range(num_processes):
            process_file_paths = file_paths[i::num_processes]
            process = multiprocessing.Process(target=update_result, args=(result, process_file_paths, keywords))
            process.start()
            processes.append(process)
        for process in processes:
            process.join()
        return dict(result)

if __name__ == '__main__':
    file_paths = [f"files/file{i}.txt" for i in range(50)]
    keywords = ["no", "yes"]

    start_time = time.time()
    print(threading_search(file_paths, keywords))
    print("Threading: ", time.time() - start_time)

    start_time = time.time()
    print(multiprocessing_search(file_paths, keywords))
    print("Multiprocessing: ", time.time() - start_time)
