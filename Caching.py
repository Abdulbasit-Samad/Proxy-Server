import time
import heapq
from collections import defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {} # stores key-value pairs
        self.freq = defaultdict(list) # stores keys by their frequency of use
        self.min_freq = 0 # minimum frequency of use in the cache

    def __getitem__(self, key):
        if key not in self.cache:
            return -1
        
        # Get the value and update the frequency of use
        value, count = self.cache[key]
        self.freq[count].remove(key)
        if not self.freq[count]:
            del self.freq[count]
        self.freq[count+1].append(key)
        self.cache[key] = (value, count+1)
        return value

    def __setitem__(self, key, value):
        if self.capacity <= 0:
            return
        
        # If the key is already in the cache, update its value and frequency of use
        if key in self.cache:
            _, count = self.cache[key]
            self.freq[count].remove(key)
            if not self.freq[count]:
                del self.freq[count]
            self.freq[count+1].append(key)
            self.cache[key] = (value, count+1)
        
        # If the key is not in the cache, add it and remove the least frequently used key if necessary
        else:
            if len(self.cache) >= self.capacity:
                min_freq_keys = self.freq[self.min_freq]
                key_to_evict = heapq.heappop(min_freq_keys)
                del self.cache[key_to_evict]
            self.cache[key] = (value, 1)
            self.freq[1].append(key)
            self.min_freq = 1

    def __contains__(self, key):
        return key in self.cache

    def __len__(self):
        return len(self.cache)

class LRUCache:
    def __init__(self, maxsize=None):
        self.cache = {}
        self.timestamp = {}
        self.maxsize = maxsize

    def __getitem__(self, key):
        # Move the key to the end of the cache
        value = self.cache[key]
        del self.cache[key]
        self.cache[key] = value
        return value

    def __setitem__(self, key, value):
        # Remove the least recently used key if the cache is full
        if self.maxsize is not None and len(self.cache) >= self.maxsize:
            oldest_key = min(self.timestamp, key=self.timestamp.get)
            del self.cache[oldest_key]
            del self.timestamp[oldest_key]

        # Add the key to the end of the cache
        self.cache[key] = value
        self.timestamp[key] = time.time()

    def __contains__(self, key):
        return key in self.cache

    def __len__(self):
        return len(self.cache)
