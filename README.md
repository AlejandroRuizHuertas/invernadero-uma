# Proyecto Invernaderos UMA

<img src="https://tstoaddicts.com/wp-content/uploads/2016/04/screenshot-2016-04-16-22-19-46.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
     

Este es el repositorio de la asignatura de Seguridad en Sistemas Industriales y Ciberfísicos del Máster de Ingeniería Informática por la Universidad de Málaga. Aquí se encuentra el código de todos los componentes que conforman el sistema industrial (Interfaz gráfica, API REST, PLC) que posteriormente está simulado en GNS3.

# Integrantes

- Josep Rodríguez Rueda
- Alejandro Ruiz Huertas
- Pablo Tomás Toledano González
    
# Requisitos

Para ejecutar los diferentes servicios es necesario tener instalado Docker en nuestra máquina. Por otra parte, si se quiere trabajar en el código de alguna parte del proyecto, será necesario instalar software adicional.

## Front
- [Node con NPM](https://nodejs.org/en/download/)

## API
- [Python3](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community)

## Invernadero
- [Python3](https://www.python.org/downloads/)
- [RabbitMQ](https://www.rabbitmq.com/download.html)

# Instalación

El repositorio cuenta con un docker compose listo para lanzar todo el código en producción. Si se quisiera lanzar alguna parte por separado, lo único que habría que hacer es crear la imagen de forma individual.

1. Montar las imágenes.
```
docker compose build
```

2. Lanzamos los servicios.
```
docker compose up
```
3. Si queremos montar una imagen en específico, lo único que tenemos que indicar son los componentes.
```
docker compose up front
```

