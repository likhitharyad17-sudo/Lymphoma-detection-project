import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# 1. Dockerfile Backend
files["backend/Dockerfile"] = """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    libgl1 libglib2.0-0 libgomp1 && \\
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# 2. Dockerfile Frontend
files["frontend/Dockerfile"] = """FROM node:20-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

# 3. Docker Compose
files["docker-compose.yml"] = """version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - LYMPHOMA_CONFIDENCE_THRESHOLD=0.80
    volumes:
      - ./backend/uploads:/app/backend/uploads
      - ./lymphoma_predictions.db:/app/lymphoma_predictions.db

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
"""

# 4. .env.example
files[".env.example"] = """PROJECT_NAME="Attention Augmented Residual Deep Learning Framework for Lymphoma Detection"
PROJECT_VERSION="2.0.0"
SECRET_KEY="your-secure-secret-key"
LYMPHOMA_CONFIDENCE_THRESHOLD=0.80
DATABASE_URL="sqlite:///./lymphoma_predictions.db"
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Created Dockerfiles, docker-compose.yml, and .env.example successfully.")
