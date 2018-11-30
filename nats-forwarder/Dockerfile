FROM node:9-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --production

COPY forwarder.js ./

CMD ["node", "forwarder"]
