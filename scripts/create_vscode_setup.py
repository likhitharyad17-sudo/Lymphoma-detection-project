import os

project_root = r"D:\Lymphoma Detection Project"
vscode_dir = os.path.join(project_root, ".vscode")
os.makedirs(vscode_dir, exist_ok=True)

files = {}

# 1. .vscode/settings.json
files[".vscode/settings.json"] = """{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoSearchPaths": true,
  "python.analysis.extraPaths": [
    "${workspaceFolder}",
    "${workspaceFolder}/backend"
  ],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "backend/tests"
  ],
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/.git": true,
    "**/.pytest_cache": true,
    "**/__pycache__": true,
    "**/*.pyc": true
  },
  "terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}"
  }
}
"""

# 2. .vscode/launch.json
files[".vscode/launch.json"] = """{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "🚀 1. Run FastAPI Backend Server",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "backend.app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload"
      ],
      "jinja": true,
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      },
      "console": "integratedTerminal"
    },
    {
      "name": "🧪 2. Run PyTest Test Suite",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "backend/tests/test_api.py",
        "-v"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "🔬 3. Run Benchmark Evaluation",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/backend/training/evaluation/evaluate_and_benchmark.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "🧠 4. Train Deep Learning Models (GPU)",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/backend/training/experiments/train_all_models.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
"""

# 3. .vscode/tasks.json
files[".vscode/tasks.json"] = """{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "🚀 Start Full Stack (Backend + Frontend)",
      "dependsOn": [
        "Start FastAPI Backend",
        "Start React Frontend"
      ],
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Start FastAPI Backend",
      "type": "shell",
      "command": "${workspaceFolder}/venv/Scripts/python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload",
      "options": {
        "env": {
          "PYTHONPATH": "${workspaceFolder}"
        }
      },
      "isBackground": true,
      "problemMatcher": [],
      "presentation": {
        "group": "fullstack",
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start React Frontend",
      "type": "shell",
      "command": "npm run dev",
      "options": {
        "cwd": "${workspaceFolder}/frontend"
      },
      "isBackground": true,
      "problemMatcher": [],
      "presentation": {
        "group": "fullstack",
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "🧪 Run PyTest Suite",
      "type": "shell",
      "command": "${workspaceFolder}/venv/Scripts/pytest.exe backend/tests/test_api.py -v",
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "📦 Build Frontend for Production",
      "type": "shell",
      "command": "npm run build",
      "options": {
        "cwd": "${workspaceFolder}/frontend"
      },
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    }
  ]
}
"""

# 4. .vscode/extensions.json
files[".vscode/extensions.json"] = """{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode"
  ]
}
"""

# 5. Lymphoma_Detection.code-workspace
files["Lymphoma_Detection.code-workspace"] = """{
  "folders": [
    {
      "name": "Lymphoma Detection Project",
      "path": "."
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["backend/tests"]
  }
}
"""

# 6. Windows Batch Scripts
files["run_backend.bat"] = """@echo off
title Lymphoma Detection - FastAPI Backend Server
echo =======================================================
echo  Starting FastAPI Backend Server on http://localhost:8000
echo =======================================================
cd /d "%~dp0"
set PYTHONPATH=%CD%
.\\venv\\Scripts\\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause
"""

files["run_frontend.bat"] = """@echo off
title Lymphoma Detection - React Frontend Dashboard
echo =======================================================
echo  Starting React Frontend Dashboard on http://localhost:5173
echo =======================================================
cd /d "%~dp0\\frontend"
npm run dev
pause
"""

files["run_all.bat"] = """@echo off
title Lymphoma Detection - Full Stack Launcher
echo =======================================================
echo  Starting Lymphoma Detection Full Stack System...
echo =======================================================

cd /d "%~dp0"

echo [1/2] Launching Backend Server in new window...
start "Lymphoma Detection - Backend API (Port 8000)" cmd /k "cd /d "%~dp0" && set PYTHONPATH=%CD% && .\\venv\\Scripts\\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Launching Frontend Dashboard in new window...
start "Lymphoma Detection - React UI (Port 5173)" cmd /k "cd /d "%~dp0\\frontend" && npm run dev"

timeout /t 3 /nobreak >nul

echo Opening browser at http://localhost:5173...
start http://localhost:5173

echo.
echo =======================================================
echo  System is running!
echo  - Frontend Dashboard : http://localhost:5173
echo  - Backend REST API   : http://localhost:8000
echo  - Interactive Docs   : http://localhost:8000/docs
echo =======================================================
echo Press any key to exit this launcher window (servers remain running).
pause >nul
"""

files["run_tests.bat"] = """@echo off
title Lymphoma Detection - Automated Test Suite
echo =======================================================
echo  Running Automated PyTest Suite...
echo =======================================================
cd /d "%~dp0"
set PYTHONPATH=%CD%
.\\venv\\Scripts\\pytest.exe backend/tests/test_api.py -v
echo =======================================================
pause
"""

files["run_evaluation.bat"] = """@echo off
title Lymphoma Detection - Benchmark Evaluation
echo =======================================================
echo  Evaluating All 8 Deep Learning Models on Test Split...
echo =======================================================
cd /d "%~dp0"
set PYTHONPATH=%CD%
.\\venv\\Scripts\\python.exe backend/training/evaluation/evaluate_and_benchmark.py
echo =======================================================
pause
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Created all VS Code configurations and 1-click launchers successfully.")
