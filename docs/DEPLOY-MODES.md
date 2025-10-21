# Deployment Modes - Quick Reference

## Which Mode Should I Use?

### 🏭 Production (Multi-Site)
**Use when**: Deploying to your production server with SSL

```bash
# 1. Build frontend
cd /home/gu/projects/formule-in-movimento/frontend
npm run build

# 2. Deploy
cd /home/gu/sites
./deploy.sh formule deploy
```

**Config location**: `/home/gu/sites/formule-in-movimento/`
**Documentation**: `/home/gu/sites/formule-in-movimento/README.md`

---

### 🧪 Standalone (Development/Testing)
**Use when**: Testing locally or deploying without multi-site infrastructure

```bash
cd /home/gu/projects/formule-in-movimento
make deploy-podman  # or make deploy-docker
```

**Config location**: `/home/gu/projects/formule-in-movimento/` (this directory)
**Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Full Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete explanation of both modes
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Standalone deployment guide
- **[/home/gu/sites/DEPLOYMENT.md](/home/gu/sites/DEPLOYMENT.md)** - Multi-site infrastructure guide
- **[CLAUDE.md](CLAUDE.md)** - Development guidelines

## Common Questions

**Q: Which files are for production vs development?**

Production (in `/home/gu/sites/formule-in-movimento/`):
- `docker-compose.yml` - Mounts `frontend/dist/` and connects to proxy
- `nginx.conf` - Production nginx config
- `.env` - Domain configuration

Development (in this directory):
- `docker-compose.yml` - Standalone deployment
- `nginx.conf` / `nginx-docker.conf` - Standalone nginx configs
- `Dockerfile` - Full Docker build

**Q: Do I commit the deployment files to git?**

- ✅ YES: Standalone files (in project directory) - for portability
- ❌ NO: Production configs (in `/home/gu/sites/`) - environment-specific

**Q: Where do videos come from?**

Both modes serve videos from `/home/gu/projects/formule-in-movimento/media/`

**Q: What about SSL/HTTPS?**

- **Production**: Automatic via nginx-proxy + acme-companion
- **Standalone**: Manual setup required (or use for local testing only)
