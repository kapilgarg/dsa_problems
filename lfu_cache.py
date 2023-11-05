from collections import defaultdict


class Node:
    def __init__(self, key, val, prev=None, next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next
        self.freq = 1


class DoubleLinkedList:
    def __init__(self):
        self.len = 0
        self.head = Node(0, 0)
        self.tail = Node(-1, 0)
        self.head.next, self.tail.prev = self.tail, self.head

    def insert_first(self, node):
        current_first = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = current_first
        current_first.prev = node
        self.len += 1

    def remove_last(self):
        if self.len == 0:
            return

        last_node = self.tail.prev
        last_node.prev.next = self.tail
        self.tail.prev = last_node.prev
        self.len -= 1
        return last_node

    def remove(self, node):
        prev, next = node.prev, node.next
        prev.next, next.prev = next, prev
        node.next = node.prev = None
        self.len -= 1


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data_map = {}
        self.freq_map = defaultdict(DoubleLinkedList)
        self.min_freq = 0

    def _remove(self, node):
        freq_list = self.freq_map[node.freq]
        freq_list.remove(node)

    def _insert(self, node):
        freq_list = self.freq_map[node.freq]
        freq_list.insert_first(node)

    def _update_min_freq(self, node):
        if self.min_freq == node.freq - 1 and self.freq_map[node.freq - 1].len == 0:
            self.min_freq = node.freq

    def get(self, key):
        if key not in self.data_map:
            return -1
        node = self.data_map.get(key)
        val = node.val

        self._remove(node)
        node.freq += 1
        self._insert(node)
        self._update_min_freq(node)
        return val

    def evict(self):
        dll = self.freq_map[self.min_freq]
        removed_node = dll.remove_last()
        del self.data_map[removed_node.key]
        self.capacity += 1
        if self.freq_map[self.min_freq].len == 0:
            self.min_freq = 1

    def put(self, key, val):
        if key in self.data_map:
            node = self.data_map.get(key)
            self._remove(node)
            node.freq += 1
            node.val = val
            self._insert(node)
            self._update_min_freq(node)

        else:
            if self.capacity == 0:
                self.evict()
            node = Node(key, val)
            dll = self.freq_map[node.freq]
            dll.insert_first(node)
            self.data_map[key] = node
            self.capacity -= 1
            self.min_freq = 1
