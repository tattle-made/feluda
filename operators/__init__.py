# This file makes the operators directory a Python package
# It allows Python to find the operator modules when they are imported

# Add the operators directory to the Python path
#import importlib.util
import os
import sys

# Get the absolute path of the operators directory
operators_dir = os.path.dirname(os.path.abspath(__file__))

# Add the operators directory to sys.path if it's not already there
if operators_dir not in sys.path:
    sys.path.append(operators_dir)

# Add each operator subdirectory to the Python path
for item in os.listdir(operators_dir):
    item_path = os.path.join(operators_dir, item)
    if os.path.isdir(item_path) and not item.startswith('__'):
        if item_path not in sys.path:
            sys.path.append(item_path)
