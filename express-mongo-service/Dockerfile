FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3030

ENV PORT=3030
ENV MONGO_URI=mongodb://mongo:27017/dealershipsDB

CMD ["node", "server.js"]
