# taller05
### Alberto Herrera, Antonella Parra
## Integración de datos y uso de CouchDB

Integrar datos de múltiples fuentes (HTML, CSV, PDF), transformarlos en un formato común y almacenarlos en CouchDB para su posterior consulta mediante vistas, desde vite


## Archivos proporcionados
* Fuente 1: fuente_html_europa.html
* Fuente 2: fuente_csv_sudamerica.csv
* Fuente 3: fuente_pdf_norteamerica_asia.pdf

## Acciones

1. Leer la información de cada fuente, de tal forma que se pueda tener un JSON que se posible importarlo a COUCHDB. Es posible que no todos los registros tengan los mismos campos. Recuerde el formato requerido por COUCHDB
```
{ "docs": [ { ... }, { ... } ] }

```

El archivo JSON debe llamarse así: mundial_2026.json

1.1. Se debe explicar el proceso para la generación de json; además debe ser replicable. Usar la carpeta formato-json, en la mismas ejecutar todo el proceso.
1.2. La BD se de llamar jugadores
1.3. Finalmente cargar el JSON, no usar curl, usar un script de Python

2. Generar tres vistas

2.1. En Design Document debe ir: losjugadores
2.2. En Index name debe ir: por_club, despúes por_goles, por_partidos
2.3. Cada vista debe seguir la siguiente estructura, según corresponda

```
function(doc) {
  if (doc.club_actual) {
    emit(doc.club_actual, doc);
  }
}
```
3. Usar la aplicación de vite compartida de la carpeta fronted, agregar titulos y pie de página, además usar los colore de la universidad.

## Entregables

* Script(s) replicables de la carpeta formato-json
* Archivo mundial_2026.json
* Evidencia de carga en CouchDB (agregar en evidencias.md)
* Capturas del frontend funcionando (agregar en evidencias.md)





NOTA: Para la ejecucion de este proyecto de forma organizada revisar el archivo evidencias.md :D
