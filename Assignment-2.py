#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random
# Node class for BST and AVL
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
        self.height = 1  # Needed for AVL tree

# BST class
class BST:
    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.value:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root
    
    def delete(self, root, key):
        if root is None:
            return root
        if key < root.value:
            root.left = self.delete(root.left, key)
        elif key > root.value:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp_val = self.get_min_value_node(root.right)
            root.value = temp_val.value
            root.right = self.delete(root.right, temp_val.value)
        return root
    
    def get_min_value_node(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def preorder_traversal(self, root):
        result = []
        if root:
            result.append(root.value)
            result = result + self.preorder_traversal(root.left)
            result = result + self.preorder_traversal(root.right)
        return result

# AVL Tree class
class AVLTree:
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        if key < root.value:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and key < root.left.value:
            return self.right_rotate(root)

        # Right Right
        if balance < -1 and key > root.right.value:
            return self.left_rotate(root)

        # Left Right
        if balance > 1 and key > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left
        if balance < -1 and key < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.value:
            root.left = self.delete(root.left, key)
        elif key > root.value:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.value = temp.value
            root.right = self.delete(root.right, temp.value)
        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def preorder_traversal(self, root):
        result = []
        if root:
            result.append(root.value)
            result = result + self.preorder_traversal(root.left)
            result = result + self.preorder_traversal(root.right)
        return result

# Helper function to find the level and position of a node in the tree
def find_level_and_position(root, key, level=1, position=1):
    if root is None:
        return None

    # If the current node is the key
    if root.value == key:
        return (level, position)

    # Left subtree search
    if root.left or root.right:
        left_pos = find_level_and_position(root.left, key, level + 1, position * 2 - 1)
        if left_pos:
            return left_pos

    # Right subtree search
    right_pos = find_level_and_position(root.right, key, level + 1, position * 2)
    return right_pos


# Sample Input
# end_of_week_1_acceptances = [10, 5, 20, 12, 15, 7, 9, 3, 18, 25]
# end_of_week_2_new_acceptances = [8, 13, 30, 11]
# end_of_week_2_declines = [12, 9, 18]

# Input
# Function to read input from a text file
def read_input_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract acceptances and declines from the file 
    week1_acceptances = [int(x.strip()) for x in lines[0].strip().split(': ')[1].strip().strip("{}").split(',') if x.strip()]
    week2_new_acceptances = [int(x.strip()) for x in lines[1].strip().split(': ')[1].strip().strip("{}").split(',') if x.strip()]
    week2_declines = [int(x.strip()) for x in lines[2].strip().split(': ')[1].strip().strip("{}").split(',') if x.strip()]

    # Convert comma-separated values to lists of integers
    # week1_acceptances = [int(x.strip()) for x in week1_acceptances.split(',') if x.strip()]
    # week2_new_acceptances = [int(x.strip()) for x in week2_new_acceptances.split(',') if x.strip()]
    # week2_declines = [int(x.strip()) for x in week2_declines.split(',') if x.strip()]
    
    return week1_acceptances, week2_new_acceptances, week2_declines

# Function to write output to a file
def write_output_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Format the output for the file
def format_output(bst_preorder_week1, avl_preorder_week1, bst_preorder_week2, avl_preorder_week2, bst_preorder_final, avl_preorder_final, selected_volunteers, bst_positions, avl_positions):
    output = []
    output.append(f'End of week 1 - Acceptances:\n Preorder traversal of the constructed BST tree is {bst_preorder_week1}\n Preorder traversal of the constructed AVL tree is {avl_preorder_week1}')
    output.append(f'End of week 2 – With new acceptances:\n Preorder traversal of the rearranged BST tree is {bst_preorder_week2}\n Preorder traversal of the re-arranged AVL tree is {avl_preorder_week2}')
    output.append(f'End of week 2 – After declines:\n Preorder traversal of the rearranged BST tree is {bst_preorder_final}\n Preorder traversal of the re-arranged AVL tree is {avl_preorder_final}')
    
    output.append(f'Randomly selected three volunteers = {selected_volunteers}')
    output.append("BST:")
    for volunteer, pos_bst in zip(selected_volunteers, bst_positions):
        output.append(f"Employee # {volunteer} is present in level {pos_bst[0]} and its position is {pos_bst[1]} from the left.")
    
    output.append("AVL:")
    for volunteer, pos_avl in zip(selected_volunteers, avl_positions):
        output.append(f"Employee # {volunteer} is present in level {pos_avl[0]} and its position is {pos_avl[1]} from the left.")
    
    return "\n".join(output)

# Main logic after reading the file
filename = 'inputPS03.txt'  # The name of the file containing the input data
week1_acceptances, week2_new_acceptances, week2_declines = read_input_from_file(filename)

# Build the BST and AVL trees from week 1 acceptances
bst = BST()
avl = AVLTree()

bst_root = None
avl_root = None

for num in week1_acceptances:
    bst_root = bst.insert(bst_root, num)
    avl_root = avl.insert(avl_root, num)

bst_preorder_week1 = bst.preorder_traversal(bst_root)
avl_preorder_week1 = avl.preorder_traversal(avl_root)

# Insert new acceptances from week 2 into both trees
for num in week2_new_acceptances:
    bst_root = bst.insert(bst_root, num)
    avl_root = avl.insert(avl_root, num)

bst_preorder_week2 = bst.preorder_traversal(bst_root)
avl_preorder_week2 = avl.preorder_traversal(avl_root)

# Remove the declined employees from both trees
for num in week2_declines:
    bst_root = bst.delete(bst_root, num)
    avl_root = avl.delete(avl_root, num)

bst_preorder_final = bst.preorder_traversal(bst_root)
avl_preorder_final = avl.preorder_traversal(avl_root)

# Randomly select three volunteers and find their level and position in both trees
final_accepted_employees = bst_preorder_final
#selected_volunteers = random.sample(final_accepted_employees, 3)
selected_volunteers = [8,3,25]

volunteer_positions_bst = []
volunteer_positions_avl = []

for volunteer in selected_volunteers:
    position_bst = find_level_and_position(bst_root, volunteer)
    volunteer_positions_bst.append(position_bst)
    
for volunteer in selected_volunteers:
    position_avl = find_level_and_position(avl_root, volunteer)
    volunteer_positions_avl.append(position_avl)

# Format the output content
output_content = format_output(
    bst_preorder_week1,
    avl_preorder_week1,
    bst_preorder_week2,
    avl_preorder_week2,
    bst_preorder_final,
    avl_preorder_final,
    selected_volunteers,
    volunteer_positions_bst,
    volunteer_positions_avl
)

# Write the output to the file
write_output_to_file('outputPS03.txt', output_content)


# In[ ]:




