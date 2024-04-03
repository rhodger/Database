FROM node:latest

EXPOSE 3000

WORKDIR code

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "start"]
