FROM node:22-alpine

WORKDIR /app

COPY package*.json /app/
RUN npm install

COPY . /app/

RUN chmod +x run.sh

CMD ["/app/run.sh"]
