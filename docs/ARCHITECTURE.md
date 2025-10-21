# Architecture & Deployment Modes

This document explains the two deployment modes for **Formule in Movimento** and when to use each.

## The Two Architectures

### 1. Production (Multi-Site Infrastructure)

**Location**: `/home/gu/sites/formule-in-movimento/`

**Purpose**: Production deployment with SSL, multiple sites support

**How it works**:
- Part of the `/home/gu/sites/` multi-site infrastructure
- Uses nginx-proxy + acme-companion for automatic SSL
- Serves the Astro build from `frontend/dist/`
- Videos served from `media/` directory
- Automatic Let's Encrypt certificates
- Supports multiple domains and sites on one server

**When to use**:
- **Production deployment** on your server
- When you want automatic SSL with Let's Encrypt
- When running multiple educational sites (infinite_powers, formule-in-movimento, etc.)

**Files**:
- `/home/gu/sites/formule-in-movimento/docker-compose.yml` - Production config
- `/home/gu/sites/formule-in-movimento/nginx.conf` - Production nginx config
- `/home/gu/sites/formule-in-movimento/.env` - Domain configuration

### 2. Standalone (Development/Testing)

**Location**: `/home/gu/projects/formule-in-movimento/` (this directory)

**Purpose**: Self-contained deployment for development and testing

**How it works**:
- Independent deployment that doesn't require the multi-site infrastructure
- Runs on port 8080 (or configurable)
- Serves the Astro build from `frontend/dist/`
- Self-contained with its own nginx instance
- No automatic SSL (manual setup required)

**When to use**:
- **Local development and testing**
- Deploying to a different server without the multi-site infrastructure
- Quick testing of the site before production deployment
- Sharing the deployment setup with others via git

**Files**:
- `docker-compose.yml` - Standalone config (in this directory)
- `nginx.conf` - Standalone nginx config (in this directory)
- `Dockerfile` - Multi-stage build (builds Astro inside Docker)

## Directory Structure

```
/home/gu/
├── projects/                                   # Source Code
│   └── formule-in-movimento/                  # THIS DIRECTORY
│       ├── frontend/                          # Astro frontend
│       │   ├── src/                          # Source files
│       │   ├── dist/                         # Built site (generated)
│       │   └── package.json
│       ├── animations/                        # Manim Python scripts
│       ├── media/                            # Generated videos
│       │
│       ├── docker-compose.yml                # Standalone mode
│       ├── Dockerfile                        # Standalone mode
│       ├── nginx.conf                        # Standalone mode
│       ├── nginx-docker.conf                 # Standalone mode (Docker)
│       └── DEPLOYMENT.md                     # Standalone deployment guide
│
└── sites/                                      # Production Infrastructure
    ├── proxy/                                 # Shared nginx-proxy
    │   └── docker-compose.yml                # nginx-proxy + acme
    │
    └── formule-in-movimento/                 # Production config
        ├── docker-compose.yml                # Mounts frontend/dist/
        ├── Dockerfile                        # Simple nginx:alpine
        ├── nginx.conf                        # Production nginx
        └── .env                              # Domain settings
```

## Key Differences

| Feature | Production (Multi-Site) | Standalone |
|---------|------------------------|------------|
| **Location** | `/home/gu/sites/formule-in-movimento/` | `/home/gu/projects/formule-in-movimento/` |
| **SSL/HTTPS** | Automatic (Let's Encrypt) | Manual setup required |
| **Ports** | Managed by nginx-proxy (80, 443) | 8080 (configurable) |
| **Multiple sites** | Yes, designed for it | No, one site per deployment |
| **Complexity** | Higher (requires proxy infrastructure) | Lower (self-contained) |
| **Use case** | Production | Development/Testing |
| **Mounts** | `frontend/dist/` + `media/` | `frontend/dist/` + `media/` (same) |
| **In git** | No (in separate `/home/gu/sites/` repo) | Yes (portable) |

## Workflows

### Development Workflow

1. **Develop locally** (Standalone mode):
   ```bash
   cd /home/gu/projects/formule-in-movimento

   # Start Astro dev server
   cd frontend && npm run dev
   # Edit files, view at http://localhost:4321

   # OR: Test with standalone deployment
   make deploy-podman
   # View at http://localhost:8080
   ```

2. **Deploy to production** (Multi-site mode):
   ```bash
   cd /home/gu/projects/formule-in-movimento

   # Build Astro
   cd frontend && npm run build

   # Deploy via multi-site infrastructure
   cd /home/gu/sites
   ./deploy.sh formule deploy
   ```

### Content Update Workflow

#### 1. Update Frontend (Pages, Styles, Components)

```bash
cd /home/gu/projects/formule-in-movimento/frontend/src

# Edit files: pages/*.astro, components/*.vue, styles/*.css

# Build
cd .. && npm run build

# Deploy to production
cd /home/gu/sites
./deploy.sh formule restart
```

#### 2. Update Animations (Manim Videos)

```bash
cd /home/gu/projects/formule-in-movimento/animations/matematica/equazioni_lineari

# Edit Python file
vim equazioni_lineari.py

# Render
manim -pqh equazioni_lineari.py SceneName

# Videos go to: /home/gu/projects/formule-in-movimento/media/
# Production site picks them up immediately - no restart needed!
```

## Best Practices

### For Development

✅ **DO**:
- Use `npm run dev` for fast iteration with hot reload
- Use `make deploy-podman` to test the production build locally
- Keep standalone deployment files in git for portability

❌ **DON'T**:
- Don't commit `frontend/dist/` to git (it's generated)
- Don't commit `.env` files (they're environment-specific)
- Don't edit production configs (`/home/gu/sites/`) directly from the project

### For Production

✅ **DO**:
- Always build Astro before deploying: `cd frontend && npm run build`
- Use the `/home/gu/sites/deploy.sh` script for deployment
- Test with standalone mode before pushing to production
- Keep production configs in `/home/gu/sites/` (separate from project repo)

❌ **DON'T**:
- Don't deploy without building Astro first
- Don't bypass the multi-site infrastructure in production
- Don't expose ports directly (let nginx-proxy handle it)

## Migration Path

If you want to deploy this project elsewhere without the multi-site infrastructure:

1. Clone the repository
2. Build the Astro frontend: `cd frontend && npm run build`
3. Use standalone deployment: `make deploy-podman` or `docker-compose up -d`
4. For SSL, configure manually or use the Dockerfile for full Docker build

The standalone deployment files travel with the git repository, making the project portable!

## Summary

- **Production** = Use `/home/gu/sites/` infrastructure (automatic SSL, multi-site)
- **Development** = Use project's standalone files (quick testing, portable)
- **Both modes** serve the same Astro build from `frontend/dist/`
- **Videos** come from `media/` in both modes
- **Keep them separate** - production in `/home/gu/sites/`, development in project directory

This dual-mode approach gives you:
- ✅ Clean separation between infrastructure and application code
- ✅ Portability (project can be deployed anywhere via standalone mode)
- ✅ Production-grade deployment with SSL (multi-site infrastructure)
- ✅ Easy local testing (standalone mode)
