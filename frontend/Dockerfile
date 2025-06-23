# syntax=docker/dockerfile:1
FROM oven/bun:1.1.13-debian AS builder

WORKDIR /app

COPY . .

RUN bun install --frozen-lockfile
RUN bun run build

FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
