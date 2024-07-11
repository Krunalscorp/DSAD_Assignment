#!/usr/bin/env python
# coding: utf-8

# Defininf the class node for doubly linked list
class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None

# Creating a class called DoublyLinkedList
class DoublyLinkedList:
    def __init__(self, capacity=None):
        self.head = None
        self.tail = None
        self.size = 0
        self.capacity = capacity
        
# This function can append the node        
    def append(self, value):
        # This will check if the nodes are exceeding the capacity defined by the user
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
            
# This will delete any node
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

# The following function will calculate the moving average till the last entry in the list
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
                    break
                current = current.next

            return moving_averages
        except Exception as e:
            print(f"Error calculating moving average: {e}")
            return []

# The following function will calculate the sudden change till beyond user-defined threshold value
    def detect_sudden_changes(self, threshold):
        try:
            if threshold <= 0:
                raise ValueError("Threshold must be greater than zero")

            changes = []
            current = self.head
            while current and current.next:
                change = abs(current.value - current.next.value)
                if change > threshold:
                    changes.append((round(current.value, 2), round(current.next.value, 2), round(change, 2)))
                current = current.next
            return changes
        except Exception as e:
            print(f"Error detecting sudden changes: {e}")
            return []

# Upon calling this function, it takes input_file 'inputPS03.txt' and reads it to calculate parameters and generate the output file 'outputPS03.txt'
def process_stock_prices(input_file, output_file, capacity=None):
    try:
        dll = DoublyLinkedList(capacity=capacity)

        with open(input_file, 'r') as file:
            lines = file.readlines()

        if not lines:
            raise ValueError(f"Input file is empty")
        
        try:
            if not lines[0].strip().split('=')[0] == 'stock_prices':
                raise ValueError(f"Stock Prices data is not available.")
            
            if not lines[1].strip().split('=')[0] == 'moving_average_window':
                raise ValueError(f"Moving Average Window value is not available.")
            
            if not lines[2].strip().split('=')[0] == 'threshold':
                raise ValueError(f"Threshold value is not available.")
        
            stock_prices = lines[0].strip().split('=')[1]
            moving_average_window = lines[1].strip().split('=')[1]
            threshold = lines[2].strip().split('=')[1]
        except IndexError:
            raise ValueError(f"Input Data is not correct.")

        # Check if moving_average_window and threshold are integer vales
        if not moving_average_window.isdigit():
            raise ValueError(f"Invalid input: Moving Average Window is not an Integer")
        
        if not threshold.isdigit():
            raise ValueError(f"Invalid input: Threshold is not an Integer")

        # TypeCast to integer
        moving_average_window = int(moving_average_window)
        threshold = int(threshold)

        prices = stock_prices.split(',')
        for price in prices:
            price = price.strip()
            if not price.replace('.', '', 1).isdigit():
                raise ValueError(f"Invalid input: {price} is not a number")
            try:
                value = float(price) if '.' in price else float(price)
                value = round(value, 2)  # Round the value to 2 decimal points
                dll.append(value)
            except RuntimeError as e:
                print(f"Error appending value {price}: {e}")

        moving_averages = dll.calculate_moving_average(moving_average_window)
        sudden_changes = dll.detect_sudden_changes(threshold)

        with open(output_file, 'w') as file:
            file.write("Moving Average of the last {} prices: {}\n".format(moving_average_window, moving_averages))
            file.write("Sudden Changes: {}\n".format(sudden_changes))
    except Exception as e:
        print(f"Error processing stock prices: {e}")

input_file = 'inputPS03.txt'
output_file = 'outputPS03.txt'
capacity = 50  # capacity of the nodes can be changed here. For now, it's set to 50, if entries exceed 50 it will generate an error

process_stock_prices(input_file, output_file, capacity)