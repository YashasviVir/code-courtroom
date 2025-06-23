# syntax=docker/dockerfile:1
FROM oven/bun:1.1.13-alpine AS builder

WORKDIR /app

COPY package.json bun.lock* .npmrc* ./
COPY tsconfig*.json ./
COPY public ./public
COPY src ./src
COPY vite.config.* ./
COPY eslint.config.js* ./
COPY components.json* ./

RUN bun install --frozen-lockfile
RUN bun run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY --from=builder /app/public /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
