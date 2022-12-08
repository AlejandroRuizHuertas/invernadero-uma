# build environment
FROM node:14.13.1 as build
WORKDIR /app
# ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . ./

# Variables de entorno
ENV PORT=80
ENV REACT_APP_HTTPAPI=http://127.0.0.1:8000

RUN npm run build

# production environment
FROM nginx:stable-alpine
# Pasamos el fichero de configuración de nginx modificado para que al refrescarse el
#   navegador (F5) no salte el error 404 y vuevla al login
#   También para que funcione por https
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
#COPY server.key /etc/ssl/certs/server.key
#COPY server.pem /etc/ssl/certs/server.pem
COPY --from=build /app/build /usr/share/nginx/html

RUN apk update
RUN apk add openssl

RUN openssl req -x509 -nodes -days 365 -subj "/C=ES/ST=MA/O=Fresitas, Inc./CN=scadafresas.com" -addext "subjectAltName=DNS:scadafresas.com" -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt;

CMD ["nginx", "-g", "daemon off;"]