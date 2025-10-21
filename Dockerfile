# Multi-stage Dockerfile for Formule in Movimento
# Stage 1: Build the Astro frontend
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build the Astro site
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy nginx configuration
COPY nginx-docker.conf /etc/nginx/conf.d/default.conf

# Copy built site from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# NOTE: Media files are mounted as a volume at runtime (not copied)
# Use: docker run -v ./media:/usr/share/nginx/html/media ...

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
