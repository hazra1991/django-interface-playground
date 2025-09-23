import threading
import time

# Create thread-local storage
local_context = threading.local()

def worker(id):
    setattr(local_context ,threading.current_thread().name,f"Thread-{id}-data")
    # local_context.value = f"Thread-{id}-data"      or use this way
    time.sleep(2)
    print(local_context.__dict__)
    # print(f"[{threading.current_thread().name}] value = {thread_local_data.value}")

threads = []

for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
setattr(local_context ,"user_id",f"This is main thread")

print(local_context.__dict__)

for t in threads:
    t.join()
