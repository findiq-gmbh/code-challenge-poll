FROM node:20-alpine

RUN apk add --no-cache curl
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
RUN npm install @sveltejs/adapter-node
COPY . .
RUN npm run build
EXPOSE 3000
ENV NODE_ENV=production

CMD ["node", "build/index.js"]
