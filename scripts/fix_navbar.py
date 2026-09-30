import os

project_root = r"D:\Lymphoma Detection Project"
navbar_path = os.path.join(project_root, "frontend", "src", "components", "Navbar.jsx")

with open(navbar_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Microscopic,", "Microscope,")

with open(navbar_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed Navbar.jsx import.")
