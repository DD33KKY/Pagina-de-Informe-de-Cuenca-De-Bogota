# Informe de Análisis Hidrológico (Sitio Web)

Este proyecto presenta un informe completo sobre el análisis de regímenes hidrológicos y climáticos en formato de sitio web interactivo. Muestra los resultados del análisis de caudal, temperatura, humedad y evaporación en diferentes escalas temporales (mensual, trimestral y anual).

## Contenido

El informe web consta de:

- **Página principal HTML** (`informe_hidrologico.html`): Contiene todas las secciones del informe, incluyendo gráficos, interpretaciones y conclusiones.
- **Estilos CSS** (`styles.css`): Define la apariencia visual del informe.
- **Funcionalidades JavaScript** (`script.js`): Proporciona interactividad y mejora la experiencia del usuario.
- **Gráficos**: Visualizaciones generadas previamente con el script de análisis hidrológico ubicadas en la carpeta `figuras/`.

## Cómo visualizar el informe

### Opción 1: Visualización local

1. Asegúrese de que los siguientes archivos estén en la misma carpeta:
   - `informe_hidrologico.html`
   - `styles.css`
   - `script.js`
   - Carpeta `figuras/` con todos los gráficos generados

2. Abra el archivo `informe_hidrologico.html` en cualquier navegador web moderno (Chrome, Firefox, Edge o Safari).

### Opción 2: Servidor web local

Si desea una experiencia más completa, puede utilizar un servidor web local:

1. Si tiene Python instalado, puede iniciar un servidor web rápidamente:
   ```
   # Para Python 3.x
   python -m http.server
   
   # Para Python 2.x
   python -m SimpleHTTPServer
   ```

2. Luego, abra su navegador y vaya a `http://localhost:8000/informe_hidrologico.html`

### Opción 3: Publicación en un servidor web

Para compartir el informe con otras personas:

1. Suba todos los archivos mencionados anteriormente a un servidor web o servicio de alojamiento.
2. Asegúrese de mantener la misma estructura de carpetas.
3. Comparta el enlace correspondiente con sus colegas o interesados.

## Características del informe web

- **Diseño responsivo**: Se adapta a diferentes tamaños de pantalla (computadoras de escritorio, tablets y dispositivos móviles).
- **Navegación intuitiva**: Menú de navegación que permite acceder rápidamente a las diferentes secciones del informe.
- **Visualización mejorada de gráficos**: Al hacer clic en cualquier gráfico, se abrirá en tamaño completo para una mejor visualización.
- **Animaciones y transiciones**: Elementos visuales que mejoran la experiencia de lectura.
- **Información bien estructurada**: El informe está organizado en secciones claras con interpretaciones de los resultados.

## Estructura del informe

1. **Resumen Ejecutivo**: Visión general del análisis y hallazgos principales.
2. **Metodología**: Descripción de los datos utilizados y métodos de análisis.
3. **Análisis de Caudal**: Regímenes mensual, trimestral y anual con interpretaciones.
4. **Análisis de Temperatura**: Regímenes mensual, trimestral y anual con interpretaciones.
5. **Análisis de Humedad**: Regímenes mensual, trimestral y anual con interpretaciones.
6. **Análisis de Evaporación**: Regímenes mensual, trimestral y anual con interpretaciones.
7. **Análisis Comparativo**: Comparación entre las diferentes variables estudiadas.
8. **Conclusiones**: Principales hallazgos, implicaciones y recomendaciones.

## Requisitos técnicos

- Navegador web moderno con soporte para:
  - HTML5
  - CSS3
  - JavaScript ES6+
  - Bootstrap 5
  - Conexión a Internet para cargar bibliotecas externas (Bootstrap y Bootstrap Icons)

## Personalización

Si desea personalizar el informe:

- **Cambiar colores**: Modifique las variables de color en el archivo `styles.css`.
- **Agregar secciones**: Añada nuevas secciones siguiendo la estructura existente en el archivo HTML.
- **Cambiar gráficos**: Reemplace las imágenes en la carpeta `figuras/` manteniendo los mismos nombres de archivo.

## Notas adicionales

- Este informe está diseñado para mostrar los resultados del análisis hidrológico de manera clara y visual.
- Los gráficos deben generarse previamente utilizando el script `analisis_hidrologico.py`.
- Para información sobre cómo generar los gráficos, consulte el archivo README principal del proyecto. 