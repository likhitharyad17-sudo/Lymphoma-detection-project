import os

test_file = r"D:\Lymphoma Detection Project\backend\tests\test_api.py"

with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()

prefix = """import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
"""
if "sys.path.insert" not in content:
    content = prefix + content

with open(test_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Added sys.path to test_api.py")
