import threading
import time
import os
from queue import Queue

def search_keywords_in_files_threading(files, keywords, results):
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        results[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

def threaded_search(file_list, keywords):
    threads = []
    results = {keyword: [] for keyword in keywords}
    queue = Queue()

    for file in file_list:
        queue.put(file)

    def worker():
        while not queue.empty():
            file = queue.get()
            search_keywords_in_files_threading([file], keywords, results)

    for _ in range(min(len(file_list), 4)):  # Максимум 4 потоки
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]  # Додайте ваші файли
    keywords = ["example", "keyword"]
    start = time.time()
    threading_results = threaded_search(files, keywords)
    end = time.time()
    print("Threading Results:", threading_results)
    print(f"Threading Time taken: {end - start} seconds")
