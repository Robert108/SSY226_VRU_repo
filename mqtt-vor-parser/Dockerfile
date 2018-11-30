FROM node:9-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --production

COPY parser.js ./

CMD ["node", "parser"]
