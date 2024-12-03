import multiprocessing
import time
import os

def search_keywords_in_files_multiprocessing(files, keywords, queue):
    results = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        results[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    queue.put(results)

def multiprocessing_search(file_list, keywords):
    num_processes = min(len(file_list), multiprocessing.cpu_count())
    chunk_size = len(file_list) // num_processes
    processes = []
    queue = multiprocessing.Queue()

    for i in range(num_processes):
        chunk = file_list[i * chunk_size:(i + 1) * chunk_size]
        process = multiprocessing.Process(target=search_keywords_in_files_multiprocessing, args=(chunk, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    combined_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        partial_results = queue.get()
        for keyword, files in partial_results.items():
            combined_results[keyword].extend(files)

    return combined_results


if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"] 
    keywords = ["example", "keyword"]
    start = time.time()
    multiprocessing_results = multiprocessing_search(files, keywords)
    end = time.time()
    print("Multiprocessing Results:", multiprocessing_results)
    print(f"Multiprocessing Time taken: {end - start} seconds")
