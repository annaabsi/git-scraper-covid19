[![scraper-daily](https://github.com/annaabsi/git-scraper-covid19/actions/workflows/main.yml/badge.svg)](https://github.com/annaabsi/git-scraper-covid19/actions/workflows/main.yml)

<!-- PROJECT HEADER -->
<br />
<p align="center">
  <a href="#">
    <img src="https://data.larepublica.pe/avance-vacunacion-covid-19-peru/logo.png" alt="Logo" width="30%" >
  </a>

  <h3 align="center">Casos confirmados y muertes por la Covid-19 en Perú</h3>
  
  <p align="center">
    <a href="https://data.larepublica.pe/envivo-casos-confirmados-muertes-coronavirus-peru/">Publicación</a>
  </p>
</p>

<hr>

## Instalación 

### Linux (Probado en Python 3.8.1+)

Automatizado con [Github Actions](.github/workflows/main.yml)

Instalación
```bash
# Instala requerimientos de Python
pip3 install -r requirements.txt
```

Obtener resultados
```bash
# Casos positivos de Covid-19
python3 scraper-positivos.py
# Fallecidos por Covid-19
python3 scraper-fallecidos.py
# Finalmente realizar commit
```


## Descripción

El programa consta de dos scripts separados: 
- scraper-positivos: obtiene [datos de "Datos Abiertos Perú"](https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa) sobre casos positivos de COVID-19 - MINSA.
- scraper-fallecidos: obtiene [datos de "Datos Abiertos Perú"](https://www.datosabiertos.gob.pe/dataset/fallecidos-por-covid-19-ministerio-de-salud-minsa) sobre fallecidos por COVID-19 - MINSA.

### *scraper-positivos.py*

Genera distintas tablas de salida con sus respetivas columnas que se encuentran dentro de la carpeta [resultados/](resultados/)


1. [positivos/departamentos](positivos/departamentos): Casos positivos según tipo de prueba por departamento `FECHA_RESULTADO,AG,PCR,PR`.
2. [positivos_diarios.csv](resultados/positivos_diarios.csv): `FECHA_RESULTADO,AG,PCR,PR`
3. [positivos_acumulados.csv](resultados/positivos_acumulados.csv): `FECHA_RESULTADO,AG,PCR,PR`
4. [positivos_por_departamentos.csv](resultados/positivos_por_departamentos.csv): `DEPARTAMENTO,METODODX,POBLACION,INDICE`
5. [positivos_por_edades.csv](resultados/positivos_por_edades.csv): `GRUPO_ETARIO,POSITIVOS,POBLACION,PORCENTAJE`
6. [fecha_corte_positivos.json](resultados/fecha_corte_positivos.json): `fecha_corte`


### *scraper-fallecidos.py*

Genera distintas tablas de salida con sus respetivas columnas que se encuentran dentro de la carpeta [resultados/](resultados/)

1. [fallecidos/departamentos](fallecidos/departamentos): Casos fallecidos según tipo de prueba por departamento `FECHA_RESULTADO,AG,PCR,PR`.
2. [fallecidos_diarios.csv](resultados/fallecidos_diarios.csv): `FECHA_RESULTADO,AG,PCR,PR`
3. [fallecidos_acumulados.csv](resultados/fallecidos_acumulados.csv): `FECHA_RESULTADO,AG,PCR,PR`
4. [fallecidos_por_departamentos.csv](resultados/fallecidos_por_departamentos.csv): `DEPARTAMENTO,METODODX,POBLACION,INDICE`
5. [fallecidos_por_edades.csv](resultados/fallecidos_por_edades.csv): `GRUPO_ETARIO,POSITIVOS,POBLACION,PORCENTAJE`
6. [fecha_corte_fallecidos.json](resultados/fecha_corte_fallecidos.json): `fecha_corte`
