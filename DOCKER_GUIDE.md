# 🐳 Docker Deployment Guide

## Quick Start with Docker

Run the application in a Docker container without installing dependencies locally.

---

## Prerequisites

- Docker installed (https://www.docker.com/products/docker-desktop)
- `.env` file with credentials (create if not exists)
- Git repository initialized

---

## Method 1: Docker Compose (Recommended - Easiest)

### Step 1: Create .env File
```bash
cd "e:\python job automation"
```

Create `.env` inside the directory:
```
NAUKRI_EMAIL=ssagayaraj37@gmail.com
NAUKRI_PASSWORD=Sagayam@123
```

### Step 2: Run with Docker Compose
```bash
docker-compose up --build
```

**Output:**
```
naukri-automation_1  | [2024-01-15 10:30:00] Starting Gunicorn...
naukri-automation_1  | [2024-01-15 10:30:02] Application running on http://0.0.0.0:5000
```

### Step 3: Access Web UI
Open browser: http://localhost:5000

### Step 4: Stop Container
```bash
docker-compose down
```

---

## Method 2: Docker CLI (Manual Build)

### Step 1: Build Image
```bash
docker build -t naukri-automation .
```

Expected output:
```
Successfully built abc123def456
Successfully tagged naukri-automation:latest
```

### Step 2: Run Container
```bash
docker run -p 5000:5000 \
  -e NAUKRI_EMAIL=ssagayaraj37@gmail.com \
  -e NAUKRI_PASSWORD=Sagayam@123 \
  -v ./data:/app/data \
  naukri-automation
```

### Step 3: Access Application
**Web UI**: http://localhost:5000
**API Health**: http://localhost:5000/api/health

### Step 4: Stop Container
```bash
docker stop <container_id>
```

---

## Docker Hub Deployment

### Step 1: Login to Docker Hub
```bash
docker login
```

### Step 2: Tag Image
```bash
docker tag naukri-automation:latest your-username/naukri-automation:latest
docker tag naukri-automation:latest your-username/naukri-automation:v1.0.0
```

### Step 3: Push to Docker Hub
```bash
docker push your-username/naukri-automation:latest
docker push your-username/naukri-automation:v1.0.0
```

### Step 4: Others Can Pull & Run
```bash
docker run -p 5000:5000 \
  -e NAUKRI_EMAIL=your-email \
  -e NAUKRI_PASSWORD=your-password \
  your-username/naukri-automation:latest
```

---

## Cloud Platform Deployment

### AWS ECR (Elastic Container Registry)

```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag naukri-automation 123456789.dkr.ecr.us-east-1.amazonaws.com/naukri-automation:latest

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/naukri-automation:latest

# Deploy to ECS/Fargate using AWS Console or CLI
```

### Google Cloud Run

```bash
# Authenticate
gcloud auth login
gcloud config set project my-project

# Build and push
gcloud builds submit --tag gcr.io/my-project/naukri-automation .

# Deploy
gcloud run deploy naukri-automation \
  --image gcr.io/my-project/naukri-automation:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars NAUKRI_EMAIL=your-email,NAUKRI_PASSWORD=your-password
```

### Azure Container Registry

```bash
# Login
az acr login --name myregistry

# Build
az acr build -r myregistry -t naukri-automation .

# Deploy (Web App for Containers)
# Use Azure Portal to create Web App and point to registry
```

### DigitalOcean App Platform

```bash
# Use doctl CLI
doctl auth init

# Deploy from Dockerfile
doctl apps create --spec app.yaml
```

---

## Docker Compose Advanced Configuration

### With Volume Persistence
```yaml
volumes:
  - ./data:/app/data           # Job storage
  - ./logs:/app/logs           # Application logs
  - ./config:/app/config       # Configuration files
```

### With Environment File
```bash
# Create .env file
docker-compose --env-file .env up
```

### With Multiple Containers

To add PostgreSQL database:

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - NAUKRI_EMAIL=${NAUKRI_EMAIL}
      - NAUKRI_PASSWORD=${NAUKRI_PASSWORD}
      - DATABASE_URL=postgresql://user:password@db:5432/naukri_jobs

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=naukri
      - POSTGRES_PASSWORD=naukri
      - POSTGRES_DB=naukri_jobs
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Troubleshooting

### Port Already in Use
```bash
# Use different port
docker run -p 8080:5000 naukri-automation

# Access at http://localhost:8080
```

### Container Exits Immediately
```bash
# Check logs
docker logs <container_id>

# Run interactively for debugging
docker run -it naukri-automation /bin/bash
```

### Environment Variables Not Set
```bash
# Verify variables are loaded
docker exec <container_id> env | grep NAUKRI

# Run with verbose logging
docker run -e FLASK_ENV=debug naukri-automation
```

### Build Issues

```bash
# Clear Docker cache and rebuild
docker build --no-cache -t naukri-automation .

# Check disk space
docker system df

# Remove unused images/containers
docker system prune -a
```

---

## Performance Tuning

### Gunicorn Workers
Adjust in Dockerfile:
```dockerfile
CMD ["gunicorn", "--workers", "8", "--threads", "2", "wsgi:app"]
```

### Memory Limits
```bash
docker run -m 512m naukri-automation
```

### CPU Limits
```bash
docker run --cpus="1.5" naukri-automation
```

---

## Monitoring

### View Logs
```bash
docker logs -f <container_id>
```

### Check Container Stats
```bash
docker stats <container_id>
```

### Inspect Container
```bash
docker inspect <container_id>
```

---

## Continuous Integration with Docker

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      
      - name: Build image
        run: docker build -t naukri-automation .
      
      - name: Run tests
        run: docker run naukri-automation python -m pytest
```

---

## Security Best Practices

1. **Never commit .env file** - Add to .gitignore
2. **Use secrets management** - Docker secrets, HashiCorp Vault, etc.
3. **Regular image updates** - Keep base image (python:3.11) updated
4. **Scan for vulnerabilities**:
   ```bash
   docker scan naukri-automation
   ```
5. **Run as non-root** (optional enhancement):
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

---

## Version Control

### Include in Git
- ✅ Dockerfile
- ✅ docker-compose.yml
- ✅ .dockerignore
- ✅ DEPLOYMENT_GUIDE.md

### Exclude from Git
- ❌ `.env` file
- ❌ `node_modules/` or `venv/`
- ❌ Large data files
- ❌ Logs and temporary files

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `docker build -t naukri-automation .` | Build image |
| `docker run -p 5000:5000 naukri-automation` | Run container |
| `docker compose up` | Start with docker-compose |
| `docker logs <container_id>` | View logs |
| `docker stop <container_id>` | Stop container |
| `docker rm <container_id>` | Remove container |
| `docker push repo/naukri-automation` | Push to registry |

---

## Next Steps

1. **Test locally**: `docker-compose up`
2. **Verify web UI**: http://localhost:5000
3. **Test search functionality**
4. **Push to Docker Hub** for easy sharing
5. **Deploy to cloud platform** of your choice

---

**Version**: 1.0.0
**Last Updated**: Current Session
**Status**: ✅ Ready for Container Deployment
