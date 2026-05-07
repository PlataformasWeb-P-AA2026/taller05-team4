#PASO A PASO DEL PROCESO 
## PRE ETAPA
Realizar la instalación de dependencias 
```bash
pip install beautifulsoup4 pandas pdfplumber requests
```
Esta librería permite:

- Leer archivos HTML.
- Leer archivos CSV.
- Extraer información desde PDF.
- Conectarse con CouchDB.

Debemos ejecutar tambien requirements.txt con el 

```bash
pip install -r requirements.txt
```

Con este codigo instalamos las dependencias del codigo que transforma los archivos a un .json indicado en la siguiente fase.
## PRIMERA ETAPA
En esta etapa transformamos los archivos .html ,.pdf y .csv para hacer que esta información se reescriba en un .json con los siguientes codigos fuentes:
1. .html a .json
![alt text](imagen.png)
2. .csv a .json
![alt text](imagen-1.png)
3. .pdf a .json 
![alt text](imagen-2.png)
Todo este codigo se encuentra junto en un archivo python que ejecuta los codigos de manera simultanea llamado generar_json que fue recomendacion de la IA Claude
![alt text](imagen-3.png)
Despues de ejecutar los codigos correspondientes para cada archivo realizamos el .json final para poder realizar las vistas

# Creación de la base de datos en CouchDB

Levantar el contenedor de CouchDB:

```bash
docker compose up -d
```

Verificar que el contenedor esté funcionando:

```bash
docker ps
```

La base de datos se crea desde la interfaz web de CouchDB.
![alt text](imagen-11.png)
![alt text](imagen-10.png)

# Carga de datos a CouchDB
Para importar el archivo JSON a la base de datos `jugadores` se utilizó el siguiente comando:

```bash
curl -u admin:admin \
-d @mundial_2026.json \
-H "Content-type: application/json" \
-X POST http://127.0.0.1:5984/jugadores/_bulk_docs
```

### Explicación

- `@mundial_2026.json` → archivo JSON con la información
- `127.0.0.1:5984` → host y puerto de CouchDB
- `jugadores` → nombre de la base de datos
- `_bulk_docs` → endpoint para importar múltiples documentos

Este script:

- Lee el archivo `mundial_2026.json`.
- Envía los documentos a CouchDB usando `_bulk_docs`.
- Inserta los registros en la base de datos `jugadores`.
![alt text](imagen-4.png)

# Creación de vistas

Dentro de CouchDB:

1. Ingresar a la base de datos `jugadores`.
2. Abrir la sección `Design Documents`.
3. Crear un nuevo Design Document llamado:

```plaintext
losjugadores
```

## Vista por club
![alt text](imagen-5.png)

## Vista por goles

![alt text](imagen-6.png)

## Vista por partidos

![alt text](imagen-7.png)

## Ejecución

Abrir una nueva terminal.

Ingresar a la carpeta frontend:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Ejecutar la aplicación:

```bash
npm run dev
```

Abrir en el navegador la dirección mostrada en la terminal.
![alt text](imagen-12.png)

## Personalización

- Se agregaron títulos.
- Se agregó pie de página.
- Se utilizaron colores institucionales de la universidad. 
```bash
(Regal Blue (Primary): HEX #01416F | RGB: 1, 65, 111 | CMYK: 99, 41, 0, 56Deep Sapphire (Accent): HEX #083866 | RGB: 8, 56, 102 | CMYK: 92, 45, 0, 60Tacha (Gold/Yellow): HEX #D4C05D | RGB: 212, 192, 93 | CMYK: 50, 58, 60, 17)
```