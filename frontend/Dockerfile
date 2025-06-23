# syntax=docker/dockerfile:1
FROM oven/bun:1.1.13-debian AS builder

WORKDIR /app

# Copy files for build
COPY . .

RUN bun install --frozen-lockfile
RUN bun run build

# ---- Serve with Nginx ----
FROM nginx:stable-alpine

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Add custom Nginx config for SPA
COPY nginx.conf /etc/nginx/conf.d

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
