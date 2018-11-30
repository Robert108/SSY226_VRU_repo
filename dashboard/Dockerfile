FROM node:9-alpine

WORKDIR /usr/src/app
VOLUME /volume

COPY package*.json ./
RUN npm install --production

COPY public public
COPY src src

RUN npm run build

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["rm -rf /volume/* && cp -r build/* /volume"]
