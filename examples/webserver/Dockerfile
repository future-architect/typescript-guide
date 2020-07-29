# ここから下がビルド用イメージ

FROM node:12-buster AS builder

WORKDIR app
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

# ここから下が実行用イメージ

FROM node:12-buster-slim AS runner
WORKDIR /opt/app
COPY --from=builder /app/dist ./
USER node
EXPOSE 3000
CMD ["node", "/opt/app/index.js"]
