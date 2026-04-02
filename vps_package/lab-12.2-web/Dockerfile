# --- Stage 1: Build Web ---
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
# Export for web
RUN NODE_OPTIONS=--max-old-space-size=2048 npx expo export --platform web

# --- Stage 2: Serve Web ---
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
