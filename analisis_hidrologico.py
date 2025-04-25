import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import MaxNLocator
from calendar import month_abbr
import matplotlib.dates as mdates
from datetime import datetime
from scipy import stats
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.table import Table

# Configuración de estilo para los gráficos
plt.style.use('ggplot')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# Crear directorio para guardar las figuras
if not os.path.exists('figuras'):
    os.makedirs('figuras')

# Nombres de los meses en español
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
trimestres = ['Ene-Mar', 'Abr-Jun', 'Jul-Sep', 'Oct-Dic']

# Función para agregar por periodos (mensual, trimestral, anual)
def agregar_por_periodo(df, fecha_col, valor_col, periodo):
    df = df.copy()
    if isinstance(df[fecha_col].iloc[0], str):
        df[fecha_col] = pd.to_datetime(df[fecha_col])
    
    df['año'] = df[fecha_col].dt.year
    df['mes'] = df[fecha_col].dt.month
    
    # Agregar trimestre
    df['trimestre'] = ((df['mes'] - 1) // 3) + 1
    
    if periodo == 'mensual':
        agregado = df.groupby(['año', 'mes'])[valor_col].mean().reset_index()
        # Calcular el promedio por mes a lo largo de todos los años
        promedio_mensual = agregado.groupby('mes')[valor_col].mean().reset_index()
        return promedio_mensual
    
    elif periodo == 'trimestral':
        agregado = df.groupby(['año', 'trimestre'])[valor_col].mean().reset_index()
        # Calcular el promedio por trimestre a lo largo de todos los años
        promedio_trimestral = agregado.groupby('trimestre')[valor_col].mean().reset_index()
        return promedio_trimestral
    
    elif periodo == 'anual':
        promedio_anual = df.groupby('año')[valor_col].mean().reset_index()
        return promedio_anual
    
    return None

# Función para crear gráficos
def crear_grafico(df, x_col, y_col, titulo, xlabel, ylabel, ruta_guardado, tipo='barras', color='#4472C4'):
    plt.figure(figsize=(14, 8))
    
    if tipo == 'barras':
        ax = sns.barplot(x=x_col, y=y_col, data=df, color=color)
        
        # Para mensual, cambiar los nombres de los meses a español
        if x_col == 'mes':
            plt.xticks(range(len(meses)), meses)
        
        # Para trimestral, cambiar a nombres de trimestres
        elif x_col == 'trimestre':
            plt.xticks(range(len(trimestres)), trimestres)
            
        # Añadir valores sobre las barras
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'bottom', 
                       xytext = (0, 5), 
                       textcoords = 'offset points')
    
    elif tipo == 'lineas':
        plt.plot(df[x_col], df[y_col], marker='o', linewidth=2.5, color=color)
        
        # Para series anuales, limitar el número de años mostrados
        if x_col == 'año':
            plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
            plt.xticks(rotation=45)
        
        # Añadir puntos y valores
        for i, txt in enumerate(df[y_col]):
            plt.annotate(f'{txt:.2f}', 
                        (df[x_col].iloc[i], df[y_col].iloc[i]), 
                        xytext=(0, 10),
                        textcoords='offset points',
                        ha='center')
    
    # Configuración adicional del gráfico
    plt.title(titulo, fontsize=18, pad=20)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tight_layout()
    
    # Guardar la figura
    plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    plt.close()

# Cargar los datos de caudal
def analizar_caudal():
    print("Analizando datos de caudal...")
    try:
        caudal_df = pd.read_csv('Caudal medio mensual/Caudal medio mensual.csv')
        caudal_df['Fecha'] = pd.to_datetime(caudal_df['Fecha'])
        
        # Análisis mensual
        caudal_mensual = agregar_por_periodo(caudal_df, 'Fecha', 'Valor', 'mensual')
        crear_grafico(caudal_mensual, 'mes', 'Valor', 
                     'Régimen Mensual de Caudal', 
                     'Mes', 'Caudal (m³/s)', 
                     'figuras/caudal_mensual.png', 'barras', '#4472C4')
        
        # Análisis trimestral
        caudal_trimestral = agregar_por_periodo(caudal_df, 'Fecha', 'Valor', 'trimestral')
        crear_grafico(caudal_trimestral, 'trimestre', 'Valor', 
                     'Régimen Trimestral de Caudal', 
                     'Trimestre', 'Caudal (m³/s)', 
                     'figuras/caudal_trimestral.png', 'barras', '#4472C4')
        
        # Análisis anual
        caudal_anual = agregar_por_periodo(caudal_df, 'Fecha', 'Valor', 'anual')
        crear_grafico(caudal_anual, 'año', 'Valor', 
                     'Régimen Anual de Caudal', 
                     'Año', 'Caudal (m³/s)', 
                     'figuras/caudal_anual.png', 'lineas', '#4472C4')
        
        print("Análisis de caudal completado.")
    except Exception as e:
        print(f"Error en el análisis de caudal: {e}")

# Cargar los datos de temperatura
def analizar_temperatura():
    print("Analizando datos de temperatura...")
    try:
        # El archivo tiene un formato diferente, con filas iniciales de metadatos
        # Vamos a leer el archivo como texto y procesarlo manualmente
        temp_file = 'Temperatura Mensual/Temperatura Minima Mensual/Temperatura Minima Mensual.csv'
        
        # Leer y parsear manualmente el archivo
        temp_data = []
        with open(temp_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Encontrar dónde comienzan los datos reales
            data_start = 0
            for i, line in enumerate(lines):
                if line.startswith('Fecha'):
                    data_start = i + 2  # Saltar la fila de encabezado y la siguiente línea en blanco
                    break
            
            # Extraer datos
            for i in range(data_start, len(lines)):
                line = lines[i].strip()
                if line and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 3 and parts[0] and parts[2]:
                        fecha = parts[0].strip()
                        # El valor está en la 3ra columna (índice 2)
                        valor_str = parts[2].strip()
                        if valor_str:
                            try:
                                valor = float(valor_str)
                                temp_data.append({'Fecha': fecha, 'Valor': valor})
                            except ValueError:
                                pass  # Ignorar valores no convertibles
        
        # Convertir a DataFrame
        if not temp_data:
            raise ValueError("No se pudieron extraer datos de temperatura del archivo")
        
        temp_min_df = pd.DataFrame(temp_data)
        temp_min_df['Fecha'] = pd.to_datetime(temp_min_df['Fecha'])
        
        # Análisis mensual
        temp_mensual = agregar_por_periodo(temp_min_df, 'Fecha', 'Valor', 'mensual')
        crear_grafico(temp_mensual, 'mes', 'Valor', 
                     'Régimen Mensual de Temperatura Mínima', 
                     'Mes', 'Temperatura (°C)', 
                     'figuras/temperatura_mensual.png', 'barras', '#ED7D31')
        
        # Análisis trimestral
        temp_trimestral = agregar_por_periodo(temp_min_df, 'Fecha', 'Valor', 'trimestral')
        crear_grafico(temp_trimestral, 'trimestre', 'Valor', 
                     'Régimen Trimestral de Temperatura Mínima', 
                     'Trimestre', 'Temperatura (°C)', 
                     'figuras/temperatura_trimestral.png', 'barras', '#ED7D31')
        
        # Análisis anual
        temp_anual = agregar_por_periodo(temp_min_df, 'Fecha', 'Valor', 'anual')
        crear_grafico(temp_anual, 'año', 'Valor', 
                     'Régimen Anual de Temperatura Mínima', 
                     'Año', 'Temperatura (°C)', 
                     'figuras/temperatura_anual.png', 'lineas', '#ED7D31')
        
        print("Análisis de temperatura completado.")
    except Exception as e:
        print(f"Error en el análisis de temperatura: {e}")

# Cargar los datos de humedad
def analizar_humedad():
    print("Analizando datos de humedad...")
    try:
        humedad_df = pd.read_csv('Húmeda relativa calculada máxima diaria/Húmeda relativa calculada máxima diaria.csv')
        humedad_df['Fecha'] = pd.to_datetime(humedad_df['Fecha'])
        
        # Análisis mensual
        humedad_mensual = agregar_por_periodo(humedad_df, 'Fecha', 'Valor', 'mensual')
        crear_grafico(humedad_mensual, 'mes', 'Valor', 
                     'Régimen Mensual de Humedad Relativa Máxima', 
                     'Mes', 'Humedad Relativa (%)', 
                     'figuras/humedad_mensual.png', 'barras', '#70AD47')
        
        # Análisis trimestral
        humedad_trimestral = agregar_por_periodo(humedad_df, 'Fecha', 'Valor', 'trimestral')
        crear_grafico(humedad_trimestral, 'trimestre', 'Valor', 
                     'Régimen Trimestral de Humedad Relativa Máxima', 
                     'Trimestre', 'Humedad Relativa (%)', 
                     'figuras/humedad_trimestral.png', 'barras', '#70AD47')
        
        # Análisis anual
        humedad_anual = agregar_por_periodo(humedad_df, 'Fecha', 'Valor', 'anual')
        crear_grafico(humedad_anual, 'año', 'Valor', 
                     'Régimen Anual de Humedad Relativa Máxima', 
                     'Año', 'Humedad Relativa (%)', 
                     'figuras/humedad_anual.png', 'lineas', '#70AD47')
        
        print("Análisis de humedad completado.")
    except Exception as e:
        print(f"Error en el análisis de humedad: {e}")

# Cargar los datos de evaporación
def analizar_evaporacion():
    print("Analizando datos de evaporación...")
    try:
        evaporacion_df = pd.read_csv('Evaporación total diaria SUM [EVTE_CON]/Evaporación total diaria SUM.csv')
        evaporacion_df['Fecha'] = pd.to_datetime(evaporacion_df['Fecha'])
        
        # Análisis mensual
        # Para la evaporación, primero obtenemos el mes de la fecha
        evaporacion_df['mes'] = evaporacion_df['Fecha'].dt.month
        evaporacion_mensual = evaporacion_df.groupby('mes')['Valor'].mean().reset_index()
        
        crear_grafico(evaporacion_mensual, 'mes', 'Valor', 
                     'Régimen Mensual de Evaporación', 
                     'Mes', 'Evaporación (mm)', 
                     'figuras/evaporacion_mensual.png', 'barras', '#5B9BD5')
        
        # Análisis trimestral
        evaporacion_df['trimestre'] = ((evaporacion_df['mes'] - 1) // 3) + 1
        evaporacion_trimestral = evaporacion_df.groupby('trimestre')['Valor'].mean().reset_index()
        
        crear_grafico(evaporacion_trimestral, 'trimestre', 'Valor', 
                     'Régimen Trimestral de Evaporación', 
                     'Trimestre', 'Evaporación (mm)', 
                     'figuras/evaporacion_trimestral.png', 'barras', '#5B9BD5')
        
        # Análisis anual
        evaporacion_df['año'] = evaporacion_df['Fecha'].dt.year
        evaporacion_anual = evaporacion_df.groupby('año')['Valor'].mean().reset_index()
        
        crear_grafico(evaporacion_anual, 'año', 'Valor', 
                     'Régimen Anual de Evaporación', 
                     'Año', 'Evaporación (mm)', 
                     'figuras/evaporacion_anual.png', 'lineas', '#5B9BD5')
        
        print("Análisis de evaporación completado.")
    except Exception as e:
        print(f"Error en el análisis de evaporación: {e}")

# Cargar los datos de precipitación
def analizar_precipitacion():
    print("Analizando datos de precipitación...")
    try:
        precipitacion_df = pd.read_csv('Datos/Precipitacion Mensual.csv')
        # Convertir la columna de fecha a formato datetime
        precipitacion_df['system:time_start'] = pd.to_datetime(precipitacion_df['system:time_start'])
        
        # Renombrar columnas para mantener consistencia con otras funciones
        precipitacion_df = precipitacion_df.rename(columns={'system:time_start': 'Fecha', 'precipitation': 'Valor'})
        
        # Análisis mensual
        precipitacion_mensual = agregar_por_periodo(precipitacion_df, 'Fecha', 'Valor', 'mensual')
        crear_grafico(precipitacion_mensual, 'mes', 'Valor', 
                     'Régimen Mensual de Precipitación', 
                     'Mes', 'Precipitación (mm)', 
                     'figuras/precipitacion_mensual.png', 'barras', '#9B59B6')
        
        # Análisis trimestral
        precipitacion_trimestral = agregar_por_periodo(precipitacion_df, 'Fecha', 'Valor', 'trimestral')
        crear_grafico(precipitacion_trimestral, 'trimestre', 'Valor', 
                     'Régimen Trimestral de Precipitación', 
                     'Trimestre', 'Precipitación (mm)', 
                     'figuras/precipitacion_trimestral.png', 'barras', '#9B59B6')
        
        # Análisis anual
        precipitacion_anual = agregar_por_periodo(precipitacion_df, 'Fecha', 'Valor', 'anual')
        crear_grafico(precipitacion_anual, 'año', 'Valor', 
                     'Régimen Anual de Precipitación', 
                     'Año', 'Precipitación (mm)', 
                     'figuras/precipitacion_anual.png', 'lineas', '#9B59B6')
        
        print("Análisis de precipitación completado.")
    except Exception as e:
        print(f"Error en el análisis de precipitación: {e}")

# Función para crear un gráfico comparativo de los promedios mensuales
def crear_grafico_comparativo():
    print("Creando gráfico comparativo de variables...")
    try:
        # Cargamos los datos de cada variable para obtener sus promedios mensuales
        caudal_df = pd.read_csv('Caudal medio mensual/Caudal medio mensual.csv')
        caudal_df['Fecha'] = pd.to_datetime(caudal_df['Fecha'])
        caudal_mensual = agregar_por_periodo(caudal_df, 'Fecha', 'Valor', 'mensual')
        
        # Temperatura - usando la misma lógica de parseo que en la función analizar_temperatura
        temp_file = 'Temperatura Mensual/Temperatura Minima Mensual/Temperatura Minima Mensual.csv'
        temp_data = []
        with open(temp_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            data_start = 0
            for i, line in enumerate(lines):
                if line.startswith('Fecha'):
                    data_start = i + 2
                    break
            
            for i in range(data_start, len(lines)):
                line = lines[i].strip()
                if line and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 3 and parts[0] and parts[2]:
                        fecha = parts[0].strip()
                        valor_str = parts[2].strip()
                        if valor_str:
                            try:
                                valor = float(valor_str)
                                temp_data.append({'Fecha': fecha, 'Valor': valor})
                            except ValueError:
                                pass
        
        if not temp_data:
            raise ValueError("No se pudieron extraer datos de temperatura del archivo")
        
        temp_min_df = pd.DataFrame(temp_data)
        temp_min_df['Fecha'] = pd.to_datetime(temp_min_df['Fecha'])
        temp_mensual = agregar_por_periodo(temp_min_df, 'Fecha', 'Valor', 'mensual')
        
        # Humedad
        humedad_df = pd.read_csv('Húmeda relativa calculada máxima diaria/Húmeda relativa calculada máxima diaria.csv')
        humedad_df['Fecha'] = pd.to_datetime(humedad_df['Fecha'])
        humedad_mensual = agregar_por_periodo(humedad_df, 'Fecha', 'Valor', 'mensual')
        
        # Evaporación
        evaporacion_df = pd.read_csv('Evaporación total diaria SUM [EVTE_CON]/Evaporación total diaria SUM.csv')
        evaporacion_df['Fecha'] = pd.to_datetime(evaporacion_df['Fecha'])
        evaporacion_df['mes'] = evaporacion_df['Fecha'].dt.month
        evaporacion_mensual = evaporacion_df.groupby('mes')['Valor'].mean().reset_index()
        
        # Precipitación
        precipitacion_df = pd.read_csv('Datos/Precipitacion Mensual.csv')
        precipitacion_df['system:time_start'] = pd.to_datetime(precipitacion_df['system:time_start'])
        precipitacion_df = precipitacion_df.rename(columns={'system:time_start': 'Fecha', 'precipitation': 'Valor'})
        precipitacion_mensual = agregar_por_periodo(precipitacion_df, 'Fecha', 'Valor', 'mensual')
        
        # Gráfico comparativo - Ahora con 6 subplots (3x2)
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))
        
        # Caudal (arriba a la izquierda)
        sns.barplot(x='mes', y='Valor', data=caudal_mensual, color='#4472C4', ax=axes[0, 0])
        axes[0, 0].set_title('Régimen Mensual de Caudal')
        axes[0, 0].set_xlabel('Mes')
        axes[0, 0].set_ylabel('Caudal (m³/s)')
        axes[0, 0].set_xticks(range(len(meses)))
        axes[0, 0].set_xticklabels(meses)
        
        # Temperatura (arriba a la derecha)
        sns.barplot(x='mes', y='Valor', data=temp_mensual, color='#ED7D31', ax=axes[0, 1])
        axes[0, 1].set_title('Régimen Mensual de Temperatura Mínima')
        axes[0, 1].set_xlabel('Mes')
        axes[0, 1].set_ylabel('Temperatura (°C)')
        axes[0, 1].set_xticks(range(len(meses)))
        axes[0, 1].set_xticklabels(meses)
        
        # Humedad (en medio a la izquierda)
        sns.barplot(x='mes', y='Valor', data=humedad_mensual, color='#70AD47', ax=axes[1, 0])
        axes[1, 0].set_title('Régimen Mensual de Humedad Relativa Máxima')
        axes[1, 0].set_xlabel('Mes')
        axes[1, 0].set_ylabel('Humedad Relativa (%)')
        axes[1, 0].set_xticks(range(len(meses)))
        axes[1, 0].set_xticklabels(meses)
        
        # Evaporación (en medio a la derecha)
        sns.barplot(x='mes', y='Valor', data=evaporacion_mensual, color='#5B9BD5', ax=axes[1, 1])
        axes[1, 1].set_title('Régimen Mensual de Evaporación')
        axes[1, 1].set_xlabel('Mes')
        axes[1, 1].set_ylabel('Evaporación (mm)')
        axes[1, 1].set_xticks(range(len(meses)))
        axes[1, 1].set_xticklabels(meses)
        
        # Precipitación (abajo a la izquierda)
        sns.barplot(x='mes', y='Valor', data=precipitacion_mensual, color='#9B59B6', ax=axes[2, 0])
        axes[2, 0].set_title('Régimen Mensual de Precipitación')
        axes[2, 0].set_xlabel('Mes')
        axes[2, 0].set_ylabel('Precipitación (mm)')
        axes[2, 0].set_xticks(range(len(meses)))
        axes[2, 0].set_xticklabels(meses)
        
        # Dejar el último subplot vacío o usar para información adicional
        axes[2, 1].axis('off')  # Desactivar el subplot vacío
        
        plt.tight_layout()
        plt.suptitle('Comparación de Regímenes Mensuales', fontsize=20, y=1.02)
        
        # Guardar figura
        plt.savefig('figuras/comparacion_regimenes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Gráfico comparativo completado.")
    except Exception as e:
        print(f"Error en la creación del gráfico comparativo: {e}")

# Nuevas funciones para análisis estadístico y gráficos avanzados

def calcular_estadisticas(df, valor_col):
    """
    Calcula estadísticas descriptivas para una serie de datos.
    """
    valores = df[valor_col].dropna()
    n = len(valores)
    minimo = valores.min()
    maximo = valores.max()
    rango = maximo - minimo
    media = valores.mean()
    mediana = valores.median()
    
    # Cálculo de la moda
    try:
        moda = stats.mode(valores, keepdims=True)[0][0]
    except:
        moda = valores.value_counts().idxmax()
    
    varianza = valores.var()
    desviacion_estandar = valores.std()
    coef_variacion = (desviacion_estandar / media) * 100 if media != 0 else 0
    
    # Cálculo de número de clases (Sturges)
    if n > 0:
        num_clases = int(1 + 3.322 * np.log10(n))
        ancho_clase = rango / num_clases if num_clases > 0 else 0
    else:
        num_clases = 0
        ancho_clase = 0
    
    return {
        'n': n,
        'minimo': minimo,
        'maximo': maximo,
        'rango': rango,
        'media': media,
        'mediana': mediana,
        'moda': moda,
        'varianza': varianza,
        'desviacion_estandar': desviacion_estandar,
        'coef_variacion': coef_variacion,
        'num_clases': num_clases,
        'ancho_clase': ancho_clase
    }

def crear_tabla_estadisticas(estadisticas, titulo, ruta_guardado):
    """
    Crea una imagen con una tabla de estadísticas descriptivas.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    ax.axis('tight')
    
    # Preparar datos para la tabla
    datos = [
        ['N', f"{estadisticas['n']}"],
        ['Mínimo', f"{estadisticas['minimo']:.3f}"],
        ['Máximo', f"{estadisticas['maximo']:.3f}"],
        ['Rango', f"{estadisticas['rango']:.3f}"],
        ['Media', f"{estadisticas['media']:.3f}"],
        ['Mediana', f"{estadisticas['mediana']:.3f}"],
        ['Moda', f"{estadisticas['moda']:.3f}"],
        ['Varianza', f"{estadisticas['varianza']:.3f}"],
        ['Desviación Estándar', f"{estadisticas['desviacion_estandar']:.3f}"],
        ['Coeficiente de Variación (%)', f"{estadisticas['coef_variacion']:.2f}"],
        ['Número de Clases', f"{estadisticas['num_clases']}"],
        ['Ancho de Clase', f"{estadisticas['ancho_clase']:.3f}"]
    ]
    
    tabla = ax.table(
        cellText=datos,
        colLabels=['Estadística', 'Valor'],
        loc='center',
        cellLoc='center'
    )
    
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1.2, 1.8)
    
    # Personalizar la tabla
    for (i, j), cell in tabla.get_celld().items():
        if i == 0:  # Encabezados
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4472C4')
        elif i % 2 == 1:  # Filas impares
            cell.set_facecolor('#D9E1F2')
        else:  # Filas pares
            cell.set_facecolor('#E9EDF4')
    
    plt.title(titulo, fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    plt.close()

def calcular_intervalos_clase(df, valor_col, num_clases=None):
    """
    Calcula los intervalos de clase y estadísticas de frecuencia.
    """
    valores = df[valor_col].dropna()
    
    if num_clases is None:
        num_clases = int(1 + 3.322 * np.log10(len(valores)))  # Regla de Sturges
    
    # Crear los intervalos
    minimo = valores.min()
    maximo = valores.max()
    ancho = (maximo - minimo) / num_clases
    
    intervalos = []
    for i in range(num_clases):
        limite_inferior = minimo + i * ancho
        limite_superior = limite_inferior + ancho
        # Para el último intervalo, asegurarse de incluir el valor máximo
        if i == num_clases - 1:
            limite_superior = maximo * 1.0001  # Pequeño margen para incluir el máximo
        
        # Etiqueta del intervalo
        etiqueta = f"[{limite_inferior:.2f}, {limite_superior:.2f})"
        
        # Contar valores en este intervalo
        if i == num_clases - 1:  # Último intervalo
            mascara = (valores >= limite_inferior) & (valores <= limite_superior)
        else:
            mascara = (valores >= limite_inferior) & (valores < limite_superior)
        
        frec_absoluta = mascara.sum()
        
        # Marca de clase (punto medio del intervalo)
        marca_clase = (limite_inferior + limite_superior) / 2
        
        intervalos.append({
            'intervalo': etiqueta,
            'limite_inferior': limite_inferior,
            'limite_superior': limite_superior,
            'marca_clase': marca_clase,
            'frec_absoluta': frec_absoluta
        })
    
    # Crear DataFrame con los resultados
    df_intervalos = pd.DataFrame(intervalos)
    
    # Calcular frecuencias relativas y acumuladas
    n_total = len(valores)
    df_intervalos['frec_relativa'] = df_intervalos['frec_absoluta'] / n_total if n_total > 0 else 0
    df_intervalos['frec_abs_acum'] = df_intervalos['frec_absoluta'].cumsum()
    df_intervalos['frec_rel_acum'] = df_intervalos['frec_relativa'].cumsum()
    
    return df_intervalos

def crear_tabla_intervalos(df_intervalos, titulo, ruta_guardado):
    """
    Crea una imagen con la tabla de intervalos de clase y frecuencias.
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    ax.axis('tight')
    
    # Preparar datos para la tabla
    datos = []
    for _, row in df_intervalos.iterrows():
        datos.append([
            row['intervalo'],
            f"{row['marca_clase']:.2f}",
            f"{int(row['frec_absoluta'])}",
            f"{row['frec_relativa']:.3f}",
            f"{int(row['frec_abs_acum'])}",
            f"{row['frec_rel_acum']:.3f}"
        ])
    
    tabla = ax.table(
        cellText=datos,
        colLabels=['Intervalo de Clase', 'Marca de Clase', 'Frec. Absoluta', 
                   'Frec. Relativa', 'Frec. Abs. Acum.', 'Frec. Rel. Acum.'],
        loc='center',
        cellLoc='center'
    )
    
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1.2, 1.5)
    
    # Personalizar la tabla
    for (i, j), cell in tabla.get_celld().items():
        if i == 0:  # Encabezados
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4472C4')
        elif i % 2 == 1:  # Filas impares
            cell.set_facecolor('#D9E1F2')
        else:  # Filas pares
            cell.set_facecolor('#E9EDF4')
    
    plt.title(titulo, fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    plt.close()

def crear_diagrama_cajas(df, fecha_col, valor_col, titulo, xlabel, ylabel, ruta_guardado, color='#4472C4'):
    """
    Crea un diagrama de cajas y bigotes para los datos mensuales multianuales.
    """
    # Preparar los datos
    df = df.copy()
    if isinstance(df[fecha_col].iloc[0], str):
        df[fecha_col] = pd.to_datetime(df[fecha_col])
    
    df['mes'] = df[fecha_col].dt.month
    df['año'] = df[fecha_col].dt.year
    
    plt.figure(figsize=(14, 8))
    
    # Crear el diagrama de cajas
    ax = sns.boxplot(x='mes', y=valor_col, data=df, palette='Blues')
    
    # Ajustar etiquetas del eje x
    plt.xticks(range(len(meses)), meses)
    
    # Calcular y mostrar la media para cada mes
    medias_mensuales = df.groupby('mes')[valor_col].mean()
    plt.plot(range(len(medias_mensuales)), medias_mensuales.values, 'ro-', linewidth=2, 
             label=f'Media: {medias_mensuales.mean():.2f}')
    
    # Añadir leyenda
    plt.legend()
    
    # Añadir etiquetas y título
    plt.title(titulo, fontsize=18, pad=20)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    
    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    plt.close()

def crear_graficos_frecuencia(df, fecha_col, valor_col, titulo_base, ylabel, ruta_base, color='#4472C4'):
    """
    Crea gráficos de frecuencias mensuales multianuales.
    """
    # Preparar los datos
    df = df.copy()
    if isinstance(df[fecha_col].iloc[0], str):
        df[fecha_col] = pd.to_datetime(df[fecha_col])
    
    df['mes'] = df[fecha_col].dt.month
    df['año'] = df[fecha_col].dt.year
    
    # 1. Frecuencia absoluta mensual multianual
    frec_abs_mensual = df.groupby('mes').size().reset_index(name='frecuencia')
    crear_grafico(frec_abs_mensual, 'mes', 'frecuencia', 
                 f'Frecuencia Absoluta Mensual Multianual - {titulo_base}', 
                 'Mes', 'Frecuencia Absoluta', 
                 f'{ruta_base}_frec_abs_mensual.png', 'barras', color)
    
    # 2. Frecuencia absoluta acumulada
    frec_abs_mensual['frec_acumulada'] = frec_abs_mensual['frecuencia'].cumsum()
    crear_grafico(frec_abs_mensual, 'mes', 'frec_acumulada', 
                 f'Frecuencia Absoluta Acumulada - {titulo_base}', 
                 'Mes', 'Frecuencia Absoluta Acumulada', 
                 f'{ruta_base}_frec_abs_acum.png', 'lineas', color)
    
    # 3. Frecuencia relativa mensual multianual
    total = frec_abs_mensual['frecuencia'].sum()
    frec_abs_mensual['frec_relativa'] = frec_abs_mensual['frecuencia'] / total if total > 0 else 0
    crear_grafico(frec_abs_mensual, 'mes', 'frec_relativa', 
                 f'Frecuencia Relativa Mensual Multianual - {titulo_base}', 
                 'Mes', 'Frecuencia Relativa', 
                 f'{ruta_base}_frec_rel_mensual.png', 'barras', color)
    
    # 4. Frecuencia relativa acumulada
    frec_abs_mensual['frec_rel_acumulada'] = frec_abs_mensual['frec_relativa'].cumsum()
    crear_grafico(frec_abs_mensual, 'mes', 'frec_rel_acumulada', 
                 f'Frecuencia Relativa Acumulada - {titulo_base}', 
                 'Mes', 'Frecuencia Relativa Acumulada', 
                 f'{ruta_base}_frec_rel_acum.png', 'lineas', color)

def analizar_estadisticas_caudal():
    """
    Realiza un análisis estadístico completo de los datos de caudal.
    """
    print("Analizando estadísticas de caudal...")
    try:
        print("  Cargando datos de caudal...")
        caudal_df = pd.read_csv('Caudal medio mensual/Caudal medio mensual.csv')
        caudal_df['Fecha'] = pd.to_datetime(caudal_df['Fecha'])
        print(f"  Datos cargados: {len(caudal_df)} registros")
        
        # 1. Calcular estadísticas descriptivas
        print("  Calculando estadísticas descriptivas...")
        stats_caudal = calcular_estadisticas(caudal_df, 'Valor')
        print(f"  Media: {stats_caudal['media']:.2f}, Mediana: {stats_caudal['mediana']:.2f}, Moda: {stats_caudal['moda']:.2f}")
        crear_tabla_estadisticas(stats_caudal, 'Estadísticas Descriptivas - Caudal Medio Mensual', 
                               'figuras/caudal_estadisticas.png')
        print("  Tabla de estadísticas generada")
        
        # 2. Calcular tabla de intervalos de clase
        print("  Calculando intervalos de clase...")
        intervalos_caudal = calcular_intervalos_clase(caudal_df, 'Valor')
        print(f"  Se generaron {len(intervalos_caudal)} intervalos")
        crear_tabla_intervalos(intervalos_caudal, 'Intervalos de Clase - Caudal Medio Mensual', 
                             'figuras/caudal_intervalos.png')
        print("  Tabla de intervalos generada")
        
        # 3. Crear diagrama de cajas y bigotes
        print("  Creando diagrama de cajas y bigotes...")
        crear_diagrama_cajas(caudal_df, 'Fecha', 'Valor', 
                           'Diagrama de Cajas y Bigotes - Caudal Medio Mensual', 
                           'Mes', 'Caudal (m³/s)', 
                           'figuras/caudal_boxplot.png', '#4472C4')
        print("  Diagrama de cajas y bigotes generado")
        
        # 4. Crear gráficos de frecuencia
        print("  Creando gráficos de frecuencia...")
        crear_graficos_frecuencia(caudal_df, 'Fecha', 'Valor', 
                                'Caudal Medio Mensual', 'Caudal (m³/s)', 
                                'figuras/caudal', '#4472C4')
        print("  Gráficos de frecuencia generados")
        
        # 5. Estadísticas específicas para el diagrama de cajas y bigotes
        print("  Calculando estadísticas por mes para el boxplot...")
        df_mensual = caudal_df.copy()
        df_mensual['mes'] = df_mensual['Fecha'].dt.month
        stats_boxplot = {}
        for mes in range(1, 13):
            valores_mes = df_mensual[df_mensual['mes'] == mes]['Valor']
            if not valores_mes.empty:
                stats_mes = calcular_estadisticas(pd.DataFrame({'Valor': valores_mes}), 'Valor')
                stats_boxplot[meses[mes-1]] = stats_mes
        
        print("  Creando tabla de estadísticas del boxplot...")
        # Crear tabla con estadísticas del boxplot
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.axis('off')
        ax.axis('tight')
        
        # Preparar datos para la tabla
        headers = ['Estadística'] + meses
        filas = [
            ['Media'],
            ['Mediana'],
            ['Moda'],
            ['Rango'],
            ['Varianza'],
            ['Desv. Est.'],
            ['Coef. Var. (%)'],
            ['Mínimo'],
            ['Máximo'],
            ['n']
        ]
        
        # Llenar los valores
        for mes in meses:
            if mes in stats_boxplot:
                s = stats_boxplot[mes]
                filas[0].append(f"{s['media']:.2f}")
                filas[1].append(f"{s['mediana']:.2f}")
                filas[2].append(f"{s['moda']:.2f}")
                filas[3].append(f"{s['rango']:.2f}")
                filas[4].append(f"{s['varianza']:.2f}")
                filas[5].append(f"{s['desviacion_estandar']:.2f}")
                filas[6].append(f"{s['coef_variacion']:.2f}")
                filas[7].append(f"{s['minimo']:.2f}")
                filas[8].append(f"{s['maximo']:.2f}")
                filas[9].append(f"{s['n']}")
            else:
                for i in range(10):
                    filas[i].append("N/A")
        
        tabla = ax.table(
            cellText=[f for f in filas],
            colLabels=headers,
            loc='center',
            cellLoc='center'
        )
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1.2, 1.5)
        
        # Personalizar la tabla
        for (i, j), cell in tabla.get_celld().items():
            if i == 0:  # Encabezados
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#4472C4')
            elif j == 0:  # Primera columna
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#D9E1F2')
            elif i % 2 == 1:  # Filas impares
                cell.set_facecolor('#E9EDF4')
            else:  # Filas pares
                cell.set_facecolor('#D9E1F2')
        
        plt.title('Estadísticas por Mes - Caudal Medio Mensual', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('figuras/caudal_boxplot_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Tabla de estadísticas del boxplot generada")
        
        print("Análisis estadístico de caudal completado.")
    except Exception as e:
        print(f"Error en el análisis estadístico de caudal: {e}")
        import traceback
        print(traceback.format_exc())

# Función para analizar estadísticas de temperatura
def analizar_estadisticas_temperatura():
    """
    Realiza un análisis estadístico completo de los datos de temperatura.
    """
    print("Analizando estadísticas de temperatura...")
    try:
        print("  Cargando datos de temperatura...")
        
        # El archivo tiene un formato diferente, con filas iniciales de metadatos
        # Vamos a leer el archivo como texto y procesarlo manualmente
        temp_file = 'Temperatura Mensual/Temperatura Minima Mensual/Temperatura Minima Mensual.csv'
        
        # Leer y parsear manualmente el archivo
        temp_data = []
        with open(temp_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Encontrar dónde comienzan los datos reales
            data_start = 0
            for i, line in enumerate(lines):
                if line.startswith('Fecha'):
                    data_start = i + 2  # Saltar la fila de encabezado y la siguiente línea en blanco
                    break
            
            # Extraer datos
            for i in range(data_start, len(lines)):
                line = lines[i].strip()
                if line and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 3 and parts[0] and parts[2]:
                        fecha = parts[0].strip()
                        # El valor está en la 3ra columna (índice 2)
                        valor_str = parts[2].strip()
                        if valor_str:
                            try:
                                valor = float(valor_str)
                                temp_data.append({'Fecha': fecha, 'Valor': valor})
                            except ValueError:
                                pass  # Ignorar valores no convertibles
        
        # Convertir a DataFrame
        if not temp_data:
            raise ValueError("No se pudieron extraer datos de temperatura del archivo")
        
        temp_min_df = pd.DataFrame(temp_data)
        temp_min_df['Fecha'] = pd.to_datetime(temp_min_df['Fecha'])
        print(f"  Datos cargados: {len(temp_min_df)} registros")
        
        # 1. Calcular estadísticas descriptivas
        print("  Calculando estadísticas descriptivas...")
        stats_temperatura = calcular_estadisticas(temp_min_df, 'Valor')
        print(f"  Media: {stats_temperatura['media']:.2f}, Mediana: {stats_temperatura['mediana']:.2f}, Moda: {stats_temperatura['moda']:.2f}")
        crear_tabla_estadisticas(stats_temperatura, 'Estadísticas Descriptivas - Temperatura Mínima Mensual', 
                               'figuras/temperatura_estadisticas.png')
        print("  Tabla de estadísticas generada")
        
        # 2. Calcular tabla de intervalos de clase
        print("  Calculando intervalos de clase...")
        intervalos_temperatura = calcular_intervalos_clase(temp_min_df, 'Valor')
        print(f"  Se generaron {len(intervalos_temperatura)} intervalos")
        crear_tabla_intervalos(intervalos_temperatura, 'Intervalos de Clase - Temperatura Mínima Mensual', 
                             'figuras/temperatura_intervalos.png')
        print("  Tabla de intervalos generada")
        
        # 3. Crear diagrama de cajas y bigotes
        print("  Creando diagrama de cajas y bigotes...")
        crear_diagrama_cajas(temp_min_df, 'Fecha', 'Valor', 
                           'Diagrama de Cajas y Bigotes - Temperatura Mínima Mensual', 
                           'Mes', 'Temperatura (°C)', 
                           'figuras/temperatura_boxplot.png', '#ED7D31')
        print("  Diagrama de cajas y bigotes generado")
        
        # 4. Crear gráficos de frecuencia
        print("  Creando gráficos de frecuencia...")
        crear_graficos_frecuencia(temp_min_df, 'Fecha', 'Valor', 
                                'Temperatura Mínima Mensual', 'Temperatura (°C)', 
                                'figuras/temperatura', '#ED7D31')
        print("  Gráficos de frecuencia generados")
        
        # 5. Estadísticas específicas para el diagrama de cajas y bigotes
        print("  Calculando estadísticas por mes para el boxplot...")
        df_mensual = temp_min_df.copy()
        df_mensual['mes'] = df_mensual['Fecha'].dt.month
        stats_boxplot = {}
        for mes in range(1, 13):
            valores_mes = df_mensual[df_mensual['mes'] == mes]['Valor']
            if not valores_mes.empty:
                stats_mes = calcular_estadisticas(pd.DataFrame({'Valor': valores_mes}), 'Valor')
                stats_boxplot[meses[mes-1]] = stats_mes
        
        print("  Creando tabla de estadísticas del boxplot...")
        # Crear tabla con estadísticas del boxplot
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.axis('off')
        ax.axis('tight')
        
        # Preparar datos para la tabla
        headers = ['Estadística'] + meses
        filas = [
            ['Media'],
            ['Mediana'],
            ['Moda'],
            ['Rango'],
            ['Varianza'],
            ['Desv. Est.'],
            ['Coef. Var. (%)'],
            ['Mínimo'],
            ['Máximo'],
            ['n']
        ]
        
        # Llenar los valores
        for mes in meses:
            if mes in stats_boxplot:
                s = stats_boxplot[mes]
                filas[0].append(f"{s['media']:.2f}")
                filas[1].append(f"{s['mediana']:.2f}")
                filas[2].append(f"{s['moda']:.2f}")
                filas[3].append(f"{s['rango']:.2f}")
                filas[4].append(f"{s['varianza']:.2f}")
                filas[5].append(f"{s['desviacion_estandar']:.2f}")
                filas[6].append(f"{s['coef_variacion']:.2f}")
                filas[7].append(f"{s['minimo']:.2f}")
                filas[8].append(f"{s['maximo']:.2f}")
                filas[9].append(f"{s['n']}")
            else:
                for i in range(10):
                    filas[i].append("N/A")
        
        tabla = ax.table(
            cellText=[f for f in filas],
            colLabels=headers,
            loc='center',
            cellLoc='center'
        )
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1.2, 1.5)
        
        # Personalizar la tabla
        for (i, j), cell in tabla.get_celld().items():
            if i == 0:  # Encabezados
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#ED7D31')
            elif j == 0:  # Primera columna
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#FBE5D6')
            elif i % 2 == 1:  # Filas impares
                cell.set_facecolor('#FDF1E9')
            else:  # Filas pares
                cell.set_facecolor('#FBE5D6')
        
        plt.title('Estadísticas por Mes - Temperatura Mínima Mensual', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('figuras/temperatura_boxplot_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Tabla de estadísticas del boxplot generada")
        
        print("Análisis estadístico de temperatura completado.")
    except Exception as e:
        print(f"Error en el análisis estadístico de temperatura: {e}")
        import traceback
        print(traceback.format_exc())

# Función para analizar estadísticas de humedad
def analizar_estadisticas_humedad():
    """
    Realiza un análisis estadístico completo de los datos de humedad relativa.
    """
    print("Analizando estadísticas de humedad...")
    try:
        print("  Cargando datos de humedad...")
        humedad_df = pd.read_csv('Húmeda relativa calculada máxima diaria/Húmeda relativa calculada máxima diaria.csv')
        humedad_df['Fecha'] = pd.to_datetime(humedad_df['Fecha'])
        print(f"  Datos cargados: {len(humedad_df)} registros")
        
        # 1. Calcular estadísticas descriptivas
        print("  Calculando estadísticas descriptivas...")
        stats_humedad = calcular_estadisticas(humedad_df, 'Valor')
        print(f"  Media: {stats_humedad['media']:.2f}, Mediana: {stats_humedad['mediana']:.2f}, Moda: {stats_humedad['moda']:.2f}")
        crear_tabla_estadisticas(stats_humedad, 'Estadísticas Descriptivas - Humedad Relativa Máxima Diaria', 
                               'figuras/humedad_estadisticas.png')
        print("  Tabla de estadísticas generada")
        
        # 2. Calcular tabla de intervalos de clase
        print("  Calculando intervalos de clase...")
        intervalos_humedad = calcular_intervalos_clase(humedad_df, 'Valor')
        print(f"  Se generaron {len(intervalos_humedad)} intervalos")
        crear_tabla_intervalos(intervalos_humedad, 'Intervalos de Clase - Humedad Relativa Máxima Diaria', 
                             'figuras/humedad_intervalos.png')
        print("  Tabla de intervalos generada")
        
        # 3. Crear diagrama de cajas y bigotes
        print("  Creando diagrama de cajas y bigotes...")
        crear_diagrama_cajas(humedad_df, 'Fecha', 'Valor', 
                           'Diagrama de Cajas y Bigotes - Humedad Relativa Máxima Diaria', 
                           'Mes', 'Humedad Relativa (%)', 
                           'figuras/humedad_boxplot.png', '#70AD47')
        print("  Diagrama de cajas y bigotes generado")
        
        # 4. Crear gráficos de frecuencia
        print("  Creando gráficos de frecuencia...")
        crear_graficos_frecuencia(humedad_df, 'Fecha', 'Valor', 
                                'Humedad Relativa Máxima Diaria', 'Humedad Relativa (%)', 
                                'figuras/humedad', '#70AD47')
        print("  Gráficos de frecuencia generados")
        
        # 5. Estadísticas específicas para el diagrama de cajas y bigotes
        print("  Calculando estadísticas por mes para el boxplot...")
        df_mensual = humedad_df.copy()
        df_mensual['mes'] = df_mensual['Fecha'].dt.month
        stats_boxplot = {}
        for mes in range(1, 13):
            valores_mes = df_mensual[df_mensual['mes'] == mes]['Valor']
            if not valores_mes.empty:
                stats_mes = calcular_estadisticas(pd.DataFrame({'Valor': valores_mes}), 'Valor')
                stats_boxplot[meses[mes-1]] = stats_mes
        
        print("  Creando tabla de estadísticas del boxplot...")
        # Crear tabla con estadísticas del boxplot
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.axis('off')
        ax.axis('tight')
        
        # Preparar datos para la tabla
        headers = ['Estadística'] + meses
        filas = [
            ['Media'],
            ['Mediana'],
            ['Moda'],
            ['Rango'],
            ['Varianza'],
            ['Desv. Est.'],
            ['Coef. Var. (%)'],
            ['Mínimo'],
            ['Máximo'],
            ['n']
        ]
        
        # Llenar los valores
        for mes in meses:
            if mes in stats_boxplot:
                s = stats_boxplot[mes]
                filas[0].append(f"{s['media']:.2f}")
                filas[1].append(f"{s['mediana']:.2f}")
                filas[2].append(f"{s['moda']:.2f}")
                filas[3].append(f"{s['rango']:.2f}")
                filas[4].append(f"{s['varianza']:.2f}")
                filas[5].append(f"{s['desviacion_estandar']:.2f}")
                filas[6].append(f"{s['coef_variacion']:.2f}")
                filas[7].append(f"{s['minimo']:.2f}")
                filas[8].append(f"{s['maximo']:.2f}")
                filas[9].append(f"{s['n']}")
            else:
                for i in range(10):
                    filas[i].append("N/A")
        
        tabla = ax.table(
            cellText=[f for f in filas],
            colLabels=headers,
            loc='center',
            cellLoc='center'
        )
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1.2, 1.5)
        
        # Personalizar la tabla
        for (i, j), cell in tabla.get_celld().items():
            if i == 0:  # Encabezados
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#70AD47')
            elif j == 0:  # Primera columna
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#E2F0D9')
            elif i % 2 == 1:  # Filas impares
                cell.set_facecolor('#F0F7EC')
            else:  # Filas pares
                cell.set_facecolor('#E2F0D9')
        
        plt.title('Estadísticas por Mes - Humedad Relativa Máxima Diaria', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('figuras/humedad_boxplot_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Tabla de estadísticas del boxplot generada")
        
        print("Análisis estadístico de humedad completado.")
    except Exception as e:
        print(f"Error en el análisis estadístico de humedad: {e}")
        import traceback
        print(traceback.format_exc())

# Función para analizar estadísticas de evaporación
def analizar_estadisticas_evaporacion():
    """
    Realiza un análisis estadístico completo de los datos de evaporación.
    """
    print("Analizando estadísticas de evaporación...")
    try:
        print("  Cargando datos de evaporación...")
        evaporacion_df = pd.read_csv('Evaporación total diaria SUM [EVTE_CON]/Evaporación total diaria SUM.csv')
        evaporacion_df['Fecha'] = pd.to_datetime(evaporacion_df['Fecha'])
        print(f"  Datos cargados: {len(evaporacion_df)} registros")
        
        # 1. Calcular estadísticas descriptivas
        print("  Calculando estadísticas descriptivas...")
        stats_evaporacion = calcular_estadisticas(evaporacion_df, 'Valor')
        print(f"  Media: {stats_evaporacion['media']:.2f}, Mediana: {stats_evaporacion['mediana']:.2f}, Moda: {stats_evaporacion['moda']:.2f}")
        crear_tabla_estadisticas(stats_evaporacion, 'Estadísticas Descriptivas - Evaporación Total Diaria', 
                               'figuras/evaporacion_estadisticas.png')
        print("  Tabla de estadísticas generada")
        
        # 2. Calcular tabla de intervalos de clase
        print("  Calculando intervalos de clase...")
        intervalos_evaporacion = calcular_intervalos_clase(evaporacion_df, 'Valor')
        print(f"  Se generaron {len(intervalos_evaporacion)} intervalos")
        crear_tabla_intervalos(intervalos_evaporacion, 'Intervalos de Clase - Evaporación Total Diaria', 
                             'figuras/evaporacion_intervalos.png')
        print("  Tabla de intervalos generada")
        
        # 3. Crear diagrama de cajas y bigotes
        print("  Creando diagrama de cajas y bigotes...")
        crear_diagrama_cajas(evaporacion_df, 'Fecha', 'Valor', 
                           'Diagrama de Cajas y Bigotes - Evaporación Total Diaria', 
                           'Mes', 'Evaporación (mm)', 
                           'figuras/evaporacion_boxplot.png', '#5B9BD5')
        print("  Diagrama de cajas y bigotes generado")
        
        # 4. Crear gráficos de frecuencia
        print("  Creando gráficos de frecuencia...")
        crear_graficos_frecuencia(evaporacion_df, 'Fecha', 'Valor', 
                                'Evaporación Total Diaria', 'Evaporación (mm)', 
                                'figuras/evaporacion', '#5B9BD5')
        print("  Gráficos de frecuencia generados")
        
        # 5. Estadísticas específicas para el diagrama de cajas y bigotes
        print("  Calculando estadísticas por mes para el boxplot...")
        df_mensual = evaporacion_df.copy()
        df_mensual['mes'] = df_mensual['Fecha'].dt.month
        stats_boxplot = {}
        for mes in range(1, 13):
            valores_mes = df_mensual[df_mensual['mes'] == mes]['Valor']
            if not valores_mes.empty:
                stats_mes = calcular_estadisticas(pd.DataFrame({'Valor': valores_mes}), 'Valor')
                stats_boxplot[meses[mes-1]] = stats_mes
        
        print("  Creando tabla de estadísticas del boxplot...")
        # Crear tabla con estadísticas del boxplot
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.axis('off')
        ax.axis('tight')
        
        # Preparar datos para la tabla
        headers = ['Estadística'] + meses
        filas = [
            ['Media'],
            ['Mediana'],
            ['Moda'],
            ['Rango'],
            ['Varianza'],
            ['Desv. Est.'],
            ['Coef. Var. (%)'],
            ['Mínimo'],
            ['Máximo'],
            ['n']
        ]
        
        # Llenar los valores
        for mes in meses:
            if mes in stats_boxplot:
                s = stats_boxplot[mes]
                filas[0].append(f"{s['media']:.2f}")
                filas[1].append(f"{s['mediana']:.2f}")
                filas[2].append(f"{s['moda']:.2f}")
                filas[3].append(f"{s['rango']:.2f}")
                filas[4].append(f"{s['varianza']:.2f}")
                filas[5].append(f"{s['desviacion_estandar']:.2f}")
                filas[6].append(f"{s['coef_variacion']:.2f}")
                filas[7].append(f"{s['minimo']:.2f}")
                filas[8].append(f"{s['maximo']:.2f}")
                filas[9].append(f"{s['n']}")
            else:
                for i in range(10):
                    filas[i].append("N/A")
        
        tabla = ax.table(
            cellText=[f for f in filas],
            colLabels=headers,
            loc='center',
            cellLoc='center'
        )
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1.2, 1.5)
        
        # Personalizar la tabla
        for (i, j), cell in tabla.get_celld().items():
            if i == 0:  # Encabezados
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#5B9BD5')
            elif j == 0:  # Primera columna
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#DEEAF6')
            elif i % 2 == 1:  # Filas impares
                cell.set_facecolor('#EFF4FB')
            else:  # Filas pares
                cell.set_facecolor('#DEEAF6')
        
        plt.title('Estadísticas por Mes - Evaporación Total Diaria', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('figuras/evaporacion_boxplot_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Tabla de estadísticas del boxplot generada")
        
        print("Análisis estadístico de evaporación completado.")
    except Exception as e:
        print(f"Error en el análisis estadístico de evaporación: {e}")
        import traceback
        print(traceback.format_exc())

# Función para analizar estadísticas de precipitación
def analizar_estadisticas_precipitacion():
    """
    Realiza un análisis estadístico completo de los datos de precipitación.
    """
    print("Analizando estadísticas de precipitación...")
    try:
        print("  Cargando datos de precipitación...")
        precipitacion_df = pd.read_csv('Datos/Precipitacion Mensual.csv')
        precipitacion_df['Fecha'] = pd.to_datetime(precipitacion_df['system:time_start'])
        precipitacion_df = precipitacion_df.rename(columns={'precipitation': 'Valor'})
        print(f"  Datos cargados: {len(precipitacion_df)} registros")
        
        # 1. Calcular estadísticas descriptivas
        print("  Calculando estadísticas descriptivas...")
        stats_precipitacion = calcular_estadisticas(precipitacion_df, 'Valor')
        print(f"  Media: {stats_precipitacion['media']:.2f}, Mediana: {stats_precipitacion['mediana']:.2f}, Moda: {stats_precipitacion['moda']:.2f}")
        crear_tabla_estadisticas(stats_precipitacion, 'Estadísticas Descriptivas - Precipitación Mensual', 
                               'figuras/precipitacion_estadisticas.png')
        print("  Tabla de estadísticas generada")
        
        # 2. Calcular tabla de intervalos de clase
        print("  Calculando intervalos de clase...")
        intervalos_precipitacion = calcular_intervalos_clase(precipitacion_df, 'Valor')
        print(f"  Se generaron {len(intervalos_precipitacion)} intervalos")
        crear_tabla_intervalos(intervalos_precipitacion, 'Intervalos de Clase - Precipitación Mensual', 
                             'figuras/precipitacion_intervalos.png')
        print("  Tabla de intervalos generada")
        
        # 3. Crear diagrama de cajas y bigotes
        print("  Creando diagrama de cajas y bigotes...")
        crear_diagrama_cajas(precipitacion_df, 'Fecha', 'Valor', 
                           'Diagrama de Cajas y Bigotes - Precipitación Mensual', 
                           'Mes', 'Precipitación (mm)', 
                           'figuras/precipitacion_boxplot.png', '#9B59B6')
        print("  Diagrama de cajas y bigotes generado")
        
        # 4. Crear gráficos de frecuencia
        print("  Creando gráficos de frecuencia...")
        crear_graficos_frecuencia(precipitacion_df, 'Fecha', 'Valor', 
                                'Precipitación Mensual', 'Precipitación (mm)', 
                                'figuras/precipitacion', '#9B59B6')
        print("  Gráficos de frecuencia generados")
        
        # 5. Estadísticas específicas para el diagrama de cajas y bigotes
        print("  Calculando estadísticas por mes para el boxplot...")
        df_mensual = precipitacion_df.copy()
        df_mensual['mes'] = df_mensual['Fecha'].dt.month
        stats_boxplot = {}
        for mes in range(1, 13):
            valores_mes = df_mensual[df_mensual['mes'] == mes]['Valor']
            if not valores_mes.empty:
                stats_mes = calcular_estadisticas(pd.DataFrame({'Valor': valores_mes}), 'Valor')
                stats_boxplot[meses[mes-1]] = stats_mes
        
        print("  Creando tabla de estadísticas del boxplot...")
        # Crear tabla con estadísticas del boxplot
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.axis('off')
        ax.axis('tight')
        
        # Preparar datos para la tabla
        headers = ['Estadística'] + meses
        filas = [
            ['Media'],
            ['Mediana'],
            ['Moda'],
            ['Rango'],
            ['Varianza'],
            ['Desv. Est.'],
            ['Coef. Var. (%)'],
            ['Mínimo'],
            ['Máximo'],
            ['n']
        ]
        
        # Llenar los valores
        for mes in meses:
            if mes in stats_boxplot:
                s = stats_boxplot[mes]
                filas[0].append(f"{s['media']:.2f}")
                filas[1].append(f"{s['mediana']:.2f}")
                filas[2].append(f"{s['moda']:.2f}")
                filas[3].append(f"{s['rango']:.2f}")
                filas[4].append(f"{s['varianza']:.2f}")
                filas[5].append(f"{s['desviacion_estandar']:.2f}")
                filas[6].append(f"{s['coef_variacion']:.2f}")
                filas[7].append(f"{s['minimo']:.2f}")
                filas[8].append(f"{s['maximo']:.2f}")
                filas[9].append(f"{s['n']}")
            else:
                for i in range(10):
                    filas[i].append("N/A")
        
        tabla = ax.table(
            cellText=[f for f in filas],
            colLabels=headers,
            loc='center',
            cellLoc='center'
        )
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1.2, 1.5)
        
        # Personalizar la tabla
        for (i, j), cell in tabla.get_celld().items():
            if i == 0:  # Encabezados
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#9B59B6')
            elif j == 0:  # Primera columna
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#E8DAEF')
            elif i % 2 == 1:  # Filas impares
                cell.set_facecolor('#F4ECF7')
            else:  # Filas pares
                cell.set_facecolor('#E8DAEF')
        
        plt.title('Estadísticas por Mes - Precipitación Mensual', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('figuras/precipitacion_boxplot_stats.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Tabla de estadísticas del boxplot generada")
        
        print("Análisis estadístico de precipitación completado.")
    except Exception as e:
        print(f"Error en el análisis estadístico de precipitación: {e}")
        import traceback
        print(traceback.format_exc())

# Función principal
if __name__ == "__main__":
    # Ejecutar las funciones de análisis básico
    #analizar_caudal()
    analizar_temperatura()
    analizar_humedad()
    analizar_evaporacion()
    analizar_precipitacion()
    
    # Crear gráfico comparativo
    crear_grafico_comparativo()
    
    # Ejecutar los análisis estadísticos
    analizar_estadisticas_caudal()
    analizar_estadisticas_temperatura()
    analizar_estadisticas_humedad()
    analizar_estadisticas_evaporacion()
    analizar_estadisticas_precipitacion()
    
    print("Análisis hidrológico completado. Revise la carpeta 'figuras' para ver los resultados.") 