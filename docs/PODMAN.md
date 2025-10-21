# Podman Deployment Guide - Formule in Movimento

Quick reference guide for deploying **Formule in Movimento** using Podman.

## Why Podman?

- **Rootless**: Run containers without root privileges
- **Daemonless**: No background service required
- **Docker-compatible**: Drop-in replacement for Docker
- **Secure**: Better default security policies
- **Systemd integration**: Native systemd service support

## Prerequisites

### Install Podman

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install podman podman-compose
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install podman
pip install podman-compose  # Not in apt repos
```

**Arch Linux:**
```bash
sudo pacman -S podman podman-compose
```

### Verify Installation

```bash
podman --version
podman-compose --version
```

## Quick Start (Podman Compose)

This is the easiest method for local development/testing.

### 1. Build the Frontend

```bash
cd /home/gu/projects/formule-in-movimento/frontend
npm install  # if not already done
npm run build
cd ..
```

### 2. Start with Podman Compose

```bash
podman-compose up -d
```

**Expected output:**
```
Creating network formule-in-movimento_formule-network
Creating formule-in-movimento-nginx
```

### 3. Verify It's Running

```bash
podman ps
```

You should see:
```
CONTAINER ID  IMAGE              COMMAND               CREATED        STATUS        PORTS                 NAMES
abc123def456  nginx:alpine       nginx -g daemon o...  2 seconds ago  Up 2 seconds  0.0.0.0:8080->80/tcp  formule-in-movimento-nginx
```

### 4. Access the Site

Open your browser to: **http://localhost:8080**

## Common Podman Commands

### View Logs

```bash
# Live logs
podman-compose logs -f

# Or directly with podman
podman logs -f formule-in-movimento-nginx
```

### Stop the Container

```bash
podman-compose down
```

### Restart After Changes

```bash
# Rebuild frontend
cd frontend && npm run build && cd ..

# Restart container
podman-compose restart
```

### List Running Containers

```bash
podman ps
```

### List All Containers (including stopped)

```bash
podman ps -a
```

## Alternative: Direct Podman (Without Compose)

If you prefer not to use podman-compose:

### 1. Build the Image

```bash
cd /home/gu/projects/formule-in-movimento
podman build -t formule-in-movimento:latest .
```

### 2. Run the Container

```bash
podman run -d \
  --name formule-in-movimento \
  -p 8080:80 \
  formule-in-movimento:latest
```

### 3. Manage the Container

```bash
# View logs
podman logs -f formule-in-movimento

# Stop
podman stop formule-in-movimento

# Start again
podman start formule-in-movimento

# Remove
podman rm formule-in-movimento

# Remove image
podman rmi formule-in-movimento:latest
```

## Podman-Specific Features

### Run as Systemd Service

You can generate a systemd unit file to auto-start the container:

```bash
# Generate user systemd service
podman generate systemd --new --name formule-in-movimento-nginx \
  --files --restart-policy=always

# Move to systemd directory
mkdir -p ~/.config/systemd/user/
mv container-formule-in-movimento-nginx.service ~/.config/systemd/user/

# Enable and start
systemctl --user enable container-formule-in-movimento-nginx.service
systemctl --user start container-formule-in-movimento-nginx.service

# Check status
systemctl --user status container-formule-in-movimento-nginx.service
```

### Auto-start on Boot (Rootless)

```bash
# Enable lingering (allows user services to start at boot)
sudo loginctl enable-linger $USER

# Now your container will start automatically at system boot
```

### Podman Pod (Optional)

If you want to add more services (e.g., a database), use Podman pods:

```bash
# Create a pod
podman pod create --name formule-pod -p 8080:80

# Run nginx in the pod
podman run -d --pod formule-pod \
  -v ./frontend/dist:/usr/share/nginx/html:ro \
  -v ./media:/usr/share/nginx/html/media:ro \
  --name formule-nginx \
  nginx:alpine
```

## Troubleshooting

### Permission Issues with SELinux

If you're on Fedora/RHEL with SELinux, you might see permission errors:

**Problem**: "Permission denied" when accessing volumes

**Solution**: Add `:Z` flag to volumes in docker-compose.yml:

```yaml
volumes:
  - ./frontend/dist:/usr/share/nginx/html:ro,Z
  - ./media:/usr/share/nginx/html/media:ro,Z
```

Or temporarily disable SELinux for the container:

```bash
podman run --security-opt label=disable ...
```

### Port Already in Use

**Problem**: `Error: rootlessport cannot expose privileged port 80`

**Solution**: Use port 8080 (or higher) instead, which is what we're already doing:

```yaml
ports:
  - "8080:80"  # Host:Container
```

To use port 80, you'd need to run rootful:

```bash
sudo podman-compose up -d  # Not recommended
```

### podman-compose Not Found

**Problem**: `podman-compose: command not found`

**Solution**:

```bash
# Install via pip
pip install podman-compose

# Or on Fedora/RHEL
sudo dnf install podman-compose

# Verify
podman-compose --version
```

### Container Won't Start

**Problem**: Container exits immediately

**Solution**: Check logs:

```bash
podman logs formule-in-movimento-nginx

# or
podman-compose logs
```

Common issues:
- Build didn't complete: `cd frontend && npm run build`
- Port conflict: Change port in docker-compose.yml
- nginx config error: Check nginx-docker.conf syntax

### Media Files Not Loading

**Problem**: Videos return 404

**Solution**: Verify symlink and permissions:

```bash
# Check symlink exists
ls -la frontend/public/media

# Recreate if needed
cd frontend/public
ln -sf ../../media media
cd ../..

# Verify media directory has videos
ls -la media/matematica/

# Restart container
podman-compose restart
```

## Performance Tips

### Use --network=host for Better Performance

```bash
podman run -d \
  --name formule-in-movimento \
  --network=host \
  -v ./frontend/dist:/usr/share/nginx/html:ro \
  -v ./media:/usr/share/nginx/html/media:ro \
  nginx:alpine
```

Note: With `--network=host`, the container uses the host's network directly. Access at `http://localhost:80` (no port mapping needed).

### Cleanup Unused Resources

```bash
# Remove unused containers
podman container prune

# Remove unused images
podman image prune -a

# Remove everything unused
podman system prune -a
```

## Comparison: Podman vs Docker

| Feature | Docker | Podman |
|---------|--------|--------|
| Daemon | Required | No daemon |
| Root access | Usually required | Rootless by default |
| systemd integration | External tools | Native |
| Docker compatibility | Native | Almost 100% |
| Pods | Via Compose/Swarm | Native pods |
| Security | Good | Better defaults |

## Next Steps

- For production deployment, see **[DEPLOYMENT.md](DEPLOYMENT.md)**
- For SSL/HTTPS setup, see DEPLOYMENT.md "SSL/HTTPS Setup" section
- For CI/CD integration, adapt Docker examples to use `podman` commands

## Quick Commands Reference

```bash
# Start
podman-compose up -d

# Stop
podman-compose down

# View logs
podman-compose logs -f

# Rebuild after changes
cd frontend && npm run build && cd ..
podman-compose restart

# List containers
podman ps

# Shell into container
podman exec -it formule-in-movimento-nginx sh

# Check nginx config
podman exec formule-in-movimento-nginx nginx -t

# Reload nginx
podman exec formule-in-movimento-nginx nginx -s reload
```

---

**Happy deploying with Podman!** 🎉
