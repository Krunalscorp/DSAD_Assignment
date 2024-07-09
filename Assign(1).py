#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Creating node class for doubly linked list
class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None


# In[3]:


class DoublyLinkedList:
    def __init__(self, capacity= None):
        self.head = None
        self.tail = None
        self.size = 0
        self.capacity = capacity

    def append(self, value):
        if self.capacity is not None and self.size >= self.capacity:
            raise RuntimeError(f"Cannot append: List is full (capacity: {self.capacity})")

        try:
            new_node = Node(value)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            self.size += 1
        except Exception as e:
            print(f"Error appending value {value}: {e}")

    def delete(self, value):
        try:
            if not self.head:
                raise ValueError("List is empty")

            current = self.head
            while current:
                if current.value == value:
                    if current.prev:
                        current.prev.next = current.next
                    if current.next:
                        current.next.prev = current.prev
                    if current == self.head:
                        self.head = current.next
                    if current == self.tail:
                        self.tail = current.prev
                    self.size -= 1
                    return
                current = current.next
            raise ValueError(f"Value {value} not found in the list")
        except Exception as e:
            print(f"Error deleting value {value}: {e}")

    def calculate_moving_average(self, window):
        try:
            if self.size == 0:
                raise ValueError("Cannot calculate moving average: list is empty")

            if window <= 0 or window > self.size:
                raise ValueError("Invalid window size")
                
            moving_averages = []
            current = self.head

            while current:
                window_sum = 0
                temp = current
                count = 0
                while temp and count < window:
                    window_sum += temp.value
                    temp = temp.next
                    count += 1
                if count == window:
                    moving_averages.append(round(window_sum / window, 2))
                if not current.next or not current.next.next:
                    break  # Break if there are not enough elements left for another full window
                current = current.next

            return moving_averages
        except Exception as e:
            print(f"Error calculating moving average: {e}")
            return []

    def detect_sudden_changes(self, threshold):
        try:
            if threshold <= 0:
                raise ValueError("Threshold must be greater than zero")

            changes = []
            current = self.head
            while current and current.next:
                change = abs(current.value - current.next.value)
                if change > threshold:
                    changes.append((current.value, current.next.value, change))
                current = current.next
            return changes
        except Exception as e:
            print(f"Error detecting sudden changes: {e}")
            return []


# In[5]:


def process_stock_prices(input_file, output_file, moving_average_window, threshold):
    try:
        # Create DoublyLinkedList instance
        dll = DoublyLinkedList()

        # Read stock prices from input file
        with open(input_file, 'r') as file:
            for line in file:
                prices = line.strip().split(',')
                for price in prices:
                    dll.append(int(price))

        # Calculate Moving Average
        moving_averages = dll.calculate_moving_average(moving_average_window)

        # Detect Sudden Changes
        sudden_changes = dll.detect_sudden_changes(threshold)

        # Write results to output file
        with open(output_file, 'w') as file:
            file.write("Moving Average of the last {} prices: {}\n".format(moving_average_window, moving_averages))
            file.write("Sudden Changes: {}\n".format(sudden_changes))
    except Exception as e:
        print(f"Error processing stock prices: {e}")

# Example usage
input_file = r'inputPS03.txt'
output_file = r'outputPS03.txt'
moving_average_window = 3
threshold = 10

process_stock_prices(input_file, output_file, moving_average_window, threshold)


# In[ ]:




