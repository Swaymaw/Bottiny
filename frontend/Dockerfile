FROM node:26
WORKDIR /app
COPY package.json ./
RUN npm i

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
