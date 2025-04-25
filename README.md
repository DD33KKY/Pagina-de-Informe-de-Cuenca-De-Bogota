# Análisis Hidrológico de Regímenes
"""
📄 Requerimiento de Visualización

Para acceder al informe hidrológico, se requiere:

- Descargar la totalidad del repositorio.
- Abrir el archivo `informe_hidrologico.html` con un navegador web.

Este archivo incluye el informe detallado de la cuenca del río Bogotá,
con todas las variables y análisis relevantes ya integrados.

⚠️ Nota importante:
No es necesario ejecutar código adicional. Solo se debe abrir el archivo HTML mencionado para visualizar el contenido completo.
"""
Este proyecto genera gráficos y tablas estadísticas para el análisis de regímenes de:
- Caudal
- Temperatura
- Humedad relativa
- Evaporación
- Precipitación

En tres escalas temporales:
- Anual
- Trimestral
- Mensual

## Requisitos

Para ejecutar el script es necesario tener instalado Python 3.7 o superior y las siguientes bibliotecas:

```
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
seaborn>=0.11.0
pillow>=9.0.0
scipy>=1.7.0
```

Puede instalar las dependencias ejecutando:

```
pip install -r requirements.txt
```

## Uso

### Generación de gráficos y análisis estadísticos

1. Asegúrese de tener los datos en la estructura de carpetas correcta:
   - Caudal medio mensual/Caudal medio mensual.csv
   - Temperatura Mensual/Temperatura Minima Mensual/Temperatura Minima Mensual.csv
   - Húmeda relativa calculada máxima diaria/Húmeda relativa calculada máxima diaria.csv
   - Evaporación total diaria SUM [EVTE_CON]/Evaporación total diaria SUM.csv
   - Datos/Precipitacion Mensual.csv

2. Ejecute el script principal para generar los gráficos y tablas estadísticas:

```
python analisis_hidrologico.py
```

3. Revise los resultados generados en la carpeta `figuras/`:
   - Gráficos mensuales, trimestrales y anuales para cada variable
   - Un gráfico comparativo con los regímenes mensuales de todas las variables
   - Diagramas de cajas y bigotes (boxplots) para análisis de distribución
   - Tablas estadísticas con medidas de tendencia central y dispersión
   - Análisis de frecuencias absolutas y relativas, simples y acumuladas




## Estructura de los gráficos y tablas

- **Gráficos de barras**: Para análisis mensual, trimestral y frecuencias
- **Gráficos de líneas**: Para análisis anual y frecuencias acumuladas
- **Diagrama de cajas y bigotes**: Para análisis de la distribución estadística mensual
- **Tablas estadísticas**: Incluyen la siguiente información:
  - Media, moda y mediana
  - Rango, varianza y desviación estándar
  - Coeficiente de variación
  - Valores máximos y mínimos
  - Cantidad de datos (n)
  - Número de clases y ancho de clase
- **Tablas de intervalos de clase**: Muestran:
  - Límites de los intervalos
  - Marca de clase
  - Frecuencia absoluta y relativa
  - Frecuencia absoluta y relativa acumulada

## Análisis estadístico

El proyecto incluye un análisis estadístico completo para las variables de caudal y precipitación, que permite:

1. **Análisis descriptivo**: Medidas de tendencia central y dispersión
2. **Análisis de distribución**: Mediante boxplots mensuales 
3. **Análisis de frecuencias**: Absolutas, relativas y acumuladas
4. **Análisis por intervalos de clase**: Determinados mediante la regla de Sturges

Todos estos análisis ayudan a comprender mejor la distribución temporal de las variables hidrológicas y su comportamiento a lo largo del tiempo. 

## Gráfico comparativo

El proyecto incluye un gráfico comparativo que muestra en un solo panel los regímenes mensuales de todas las variables analizadas (caudal, temperatura, humedad, evaporación y precipitación), facilitando la comparación visual de los patrones estacionales de cada variable y la identificación de posibles relaciones entre ellas. 


