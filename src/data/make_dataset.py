import json
import os
import requests
import pandas as pd
import numpy as np
import time
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta base del proyecto (dos niveles arriba del script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


# ============================================================================
# SECCIÓN 1: DESCARGA DE DATOS DE LA SEP
# ============================================================================

def descargar_formato_911():
    """
    Descarga los archivos del Formato 911 de la SEP para educación básica.
    El Formato 911 es el principal instrumento de recolección de datos del 
    sistema educativo en México.
    """
    print("=" * 70)
    print("INICIANDO DESCARGA DE DATOS DE LA SEP")
    print("=" * 70)
    
    # Diccionario con los ciclos escolares y sus URLs
    archivos_a_descargar = {
        '2019-2020': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2019-2020.csv',
        '2020-2021': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2020-2021.csv',
        '2021-2022': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2021-2022.csv',
        '2022-2023': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2022-2023.csv',
        '2023-2024': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/ESTANDAR_BASICA_I2324.csv'
    }
    
    ruta = PROJECT_ROOT / 'data' / 'raw' / 'formato_911'
    ruta.mkdir(parents=True, exist_ok=True)
    
    print("\n--- Descargando archivos del Formato 911 ---")
    
    for ciclo, url in archivos_a_descargar.items():
        nombre_archivo = f'formato_911_basica_{ciclo}.csv'
        ruta_guardado = ruta / nombre_archivo
        
        if not ruta_guardado.exists():
            print(f"\nDescargando datos para el ciclo {ciclo}...")
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(ruta_guardado, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f" -> ✅ Archivo guardado en: {ruta_guardado}")
            
            except requests.exceptions.RequestException as e:
                print(f" -> ❌ Error al descargar el archivo para el ciclo {ciclo}: {e}")
        else:
            print(f"\n✓ El archivo para el ciclo {ciclo} ya existe. Se omite.")
    
    print("\n✅ Descarga del Formato 911 finalizada.")


def descargar_catalogo_escuelas():
    """
    Descarga el catálogo de centros de trabajo (escuelas) del estado de Sonora.
    """
    print("\n--- Descargando Catálogo de Centros de Trabajo (Escuelas) de Sonora ---")
    
    url_catalogo = 'https://www.datos.gob.mx/dataset/2a1d047c-546b-4293-971a-c835689a37a5/resource/4f013342-5028-447f-b39d-1c08f09f47f3/download/catalogo_centro_trabajo_26_csv.csv'
    ruta_raw = PROJECT_ROOT / 'data' / 'raw'
    nombre_archivo = 'catalogo_escuelas_sonora.csv'
    ruta_guardado = ruta_raw / nombre_archivo
    
    ruta_raw.mkdir(parents=True, exist_ok=True)
    
    if not ruta_guardado.exists():
        try:
            df_catalogo = pd.read_csv(url_catalogo, encoding='latin1', low_memory=False)
            df_catalogo.to_csv(ruta_guardado, index=False, encoding='utf-8')
            
            print(f"✅ Catálogo de escuelas guardado exitosamente en: {ruta_guardado}")
            print(f"   Total de registros: {len(df_catalogo)}")
        
        except Exception as e:
            print(f"❌ Ocurrió un error al descargar o procesar el archivo: {e}")
    else:
        print(f"✓ El archivo '{nombre_archivo}' ya existe. Se omite.")


# ============================================================================
# SECCIÓN 2: DESCARGA DE DATOS DEL INEGI
# ============================================================================

def cargar_configuracion():
    """
    Carga todas las configuraciones necesarias desde la carpeta /references.
    """
    print("\n" + "=" * 70)
    print("INICIANDO DESCARGA DE DATOS DEL INEGI")
    print("=" * 70)
    print("\n--- 1. Cargando configuración ---")
    
    # Cargar el .env desde la raíz del proyecto
    dotenv_path = PROJECT_ROOT / '.env'
    load_dotenv(dotenv_path)
    
    token = os.getenv("INEGI_TOKEN")
    if not token:
        raise ValueError("No se encontró el token de INEGI en el archivo .env")
    
    ruta_referencias = PROJECT_ROOT / 'references'
    
    # Verificar que la carpeta references existe
    if not ruta_referencias.exists():
        raise Exception(f"Error: La carpeta 'references' no existe en {ruta_referencias}")
    
    print(f"Buscando archivos de configuración en: {ruta_referencias}")
    
    try:
        ruta_municipales = ruta_referencias / 'diccionario_inegi_municipio.json'
        ruta_contexto = ruta_referencias / 'diccionario_inegi_contexto.json'
        ruta_dict_municipios = ruta_referencias / 'diccionario_municipios_sonora.json'
        
        # Verificar que los archivos existen
        archivos_requeridos = [
            ('diccionario_inegi_municipio.json', ruta_municipales),
            ('diccionario_inegi_contexto.json', ruta_contexto),
            ('diccionario_municipios_sonora.json', ruta_dict_municipios)
        ]
        
        archivos_faltantes = []
        for nombre, ruta in archivos_requeridos:
            if not ruta.exists():
                archivos_faltantes.append(nombre)
        
        if archivos_faltantes:
            raise Exception(f"Faltan los siguientes archivos en {ruta_referencias}:\n" + 
                          "\n".join(f"  - {archivo}" for archivo in archivos_faltantes))
        
        with open(ruta_municipales, 'r', encoding='utf-8') as f:
            config_municipales = json.load(f)
        with open(ruta_contexto, 'r', encoding='utf-8') as f:
            config_contexto = json.load(f)
        with open(ruta_dict_municipios, 'r', encoding='utf-8') as f:
            municipios = json.load(f)
    
    except FileNotFoundError as e:
        raise Exception(f"Error: No se encontró un archivo de configuración. Detalle: {e}")
    
    print("✅ Configuración cargada exitosamente.")
    return token, config_municipales, config_contexto, municipios


def descargar_datos_municipales(token, config_municipales, municipios):
    """
    Descarga y procesa la serie histórica completa para todos 
    los indicadores a nivel municipal.
    """
    print("\n--- 2. Descargando datos municipales (serie histórica completa) ---")
    
    CLAVE_SONORA = '07000026'
    ruta_external = PROJECT_ROOT / 'data' / 'external'
    ruta_external.mkdir(parents=True, exist_ok=True)
    
    for indicador in config_municipales['indicadores_municipales']:
        nombre_indicador = indicador['nombre']
        id_indicador = indicador['id_inegi']
        
        ruta_csv = ruta_external / f"{nombre_indicador}.csv"
        
        if ruta_csv.exists():
            print(f"\n✓ El archivo '{nombre_indicador}.csv' ya existe. Se omite.")
            continue
        
        print(f"\nProcesando indicador: {nombre_indicador}...")
        
        datos_de_este_indicador = []
        for nombre_mun, codigo_mun in municipios.items():
            ubicacion = CLAVE_SONORA + codigo_mun
            url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{id_indicador}/es/{ubicacion}/false/BISE/2.0/{token}?type=json"
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                observaciones = data['Series'][0]['OBSERVATIONS']
                
                if observaciones:
                    for obs in observaciones:
                        valor = obs['OBS_VALUE']
                        periodo = obs['TIME_PERIOD']
                        
                        if valor is not None:
                            datos_de_este_indicador.append({
                                'municipio': nombre_mun,
                                'periodo': periodo,
                                'valor': float(valor)
                            })
                        else:
                            datos_de_este_indicador.append({
                                'municipio': nombre_mun,
                                'periodo': periodo,
                                'valor': np.nan
                            })
                else:
                    print(f" -> Advertencia: No se encontraron observaciones para {nombre_mun}.")
            
            except Exception as e:
                print(f" -> Error al consultar {nombre_mun}: {e}")
            
            time.sleep(0.1)
        
        if datos_de_este_indicador:
            df = pd.DataFrame(datos_de_este_indicador)
            df = df[['municipio', 'periodo', 'valor']]
            df.to_csv(ruta_csv, index=False, encoding='utf-8')
            print(f" -> ✅ Archivo '{nombre_indicador}.csv' guardado con {len(df)} registros.")


def descargar_datos_contexto(token, config_contexto):
    """
    Descarga y procesa todos los indicadores de contexto (estatales y nacionales).
    """
    print("\n--- 3. Descargando datos de contexto (Estatales/Nacionales) ---")
    
    CLAVE_GEO_SONORA = '07000026'
    CLAVE_GEO_NACIONAL = '0700'
    ruta_external = PROJECT_ROOT / 'data' / 'external'
    ruta_external.mkdir(parents=True, exist_ok=True)
    
    for indicador in config_contexto['indicadores_contexto']:
        nombre_indicador = indicador['nombre']
        id_indicador = indicador['id_inegi']
        
        ruta_csv = ruta_external / f"{nombre_indicador}.csv"
        if ruta_csv.exists():
            print(f"\n✓ El archivo '{nombre_indicador}.csv' ya existe. Se omite.")
            continue
        
        nivel_geo = indicador.get('nivel_geografico', 'estatal')
        fuente_api = indicador.get('fuente_api', 'BISE')
        
        ubicacion = CLAVE_GEO_NACIONAL if nivel_geo == 'nacional' else CLAVE_GEO_SONORA
        
        print(f"\nProcesando indicador '{nombre_indicador}' desde {fuente_api}...")
        
        url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{id_indicador}/es/{ubicacion}/false/{fuente_api}/2.0/{token}?type=json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            observaciones = data['Series'][0]['OBSERVATIONS']
            datos_limpios = [
                {'periodo': obs['TIME_PERIOD'], 'valor': float(obs['OBS_VALUE'])}
                for obs in observaciones if obs['OBS_VALUE'] is not None
            ]
            
            df = pd.DataFrame(datos_limpios)
            df.to_csv(ruta_csv, index=False, encoding='utf-8')
            print(f" -> ✅ Archivo '{nombre_indicador}.csv' guardado.")
        
        except Exception as e:
            print(f" -> ❌ Error al procesar el indicador {nombre_indicador}: {e}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta todas las descargas.
    """
    print("\n" + "=" * 70)
    print("SCRIPT DE DESCARGA UNIFICADO - SEP E INEGI")
    print("=" * 70)
    print(f"\nDirectorio del script: {SCRIPT_DIR}")
    print(f"Raíz del proyecto: {PROJECT_ROOT}")
    
    try:
        # Parte 1: Descargas de la SEP
        descargar_formato_911()
        descargar_catalogo_escuelas()
        
        # Parte 2: Descargas del INEGI
        api_token, conf_municipales, conf_contexto, dict_municipios = cargar_configuracion()
        descargar_datos_municipales(api_token, conf_municipales, dict_municipios)
        descargar_datos_contexto(api_token, conf_contexto)
        
        print("\n" + "=" * 70)
        print("🎉 ¡PROCESO COMPLETO FINALIZADO EXITOSAMENTE!")
        print("=" * 70)
        print(f"\nArchivos guardados en:")
        print(f"  - {PROJECT_ROOT / 'data' / 'raw' / 'formato_911'}")
        print(f"  - {PROJECT_ROOT / 'data' / 'raw' / 'catalogo_escuelas_sonora.csv'}")
        print(f"  - {PROJECT_ROOT / 'data' / 'external'}")
    
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ OCURRIÓ UN ERROR EN EL PROCESO PRINCIPAL:")
        print(f"   {e}")
        print("=" * 70)


if __name__ == "__main__":
    main()
"""
Script unificado para descargar datos de SEP e INEGI
Descarga:
1. Formato 911 (SEP) - Matrícula escolar por ciclo escolar
2. Catálogo de escuelas de Sonora
3. Indicadores municipales (INEGI)
4. Indicadores de contexto estatales y nacionales (INEGI)
"""

import json
import os
import requests
import pandas as pd
import numpy as np
import time
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta base del proyecto (dos niveles arriba del script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


# ============================================================================
# SECCIÓN 1: DESCARGA DE DATOS DE LA SEP
# ============================================================================

def descargar_formato_911():
    """
    Descarga los archivos del Formato 911 de la SEP para educación básica.
    El Formato 911 es el principal instrumento de recolección de datos del 
    sistema educativo en México.
    """
    print("=" * 70)
    print("INICIANDO DESCARGA DE DATOS DE LA SEP")
    print("=" * 70)
    
    # Diccionario con los ciclos escolares y sus URLs
    archivos_a_descargar = {
        '2019-2020': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2019-2020.csv',
        '2020-2021': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2020-2021.csv',
        '2021-2022': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2021-2022.csv',
        '2022-2023': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/BASICA_2022-2023.csv',
        '2023-2024': 'https://repodatos.atdt.gob.mx/s_educacion_publica/f911/ESTANDAR_BASICA_I2324.csv'
    }
    
    ruta = PROJECT_ROOT / 'data' / 'raw' / 'formato_911'
    ruta.mkdir(parents=True, exist_ok=True)
    
    print("\n--- Descargando archivos del Formato 911 ---")
    
    for ciclo, url in archivos_a_descargar.items():
        nombre_archivo = f'formato_911_basica_{ciclo}.csv'
        ruta_guardado = ruta / nombre_archivo
        
        if not ruta_guardado.exists():
            print(f"\nDescargando datos para el ciclo {ciclo}...")
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(ruta_guardado, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f" -> ✅ Archivo guardado en: {ruta_guardado}")
            
            except requests.exceptions.RequestException as e:
                print(f" -> ❌ Error al descargar el archivo para el ciclo {ciclo}: {e}")
        else:
            print(f"\n✓ El archivo para el ciclo {ciclo} ya existe. Se omite.")
    
    print("\n✅ Descarga del Formato 911 finalizada.")


def descargar_catalogo_escuelas():
    """
    Descarga el catálogo de centros de trabajo (escuelas) del estado de Sonora.
    """
    print("\n--- Descargando Catálogo de Centros de Trabajo (Escuelas) de Sonora ---")
    
    url_catalogo = 'https://www.datos.gob.mx/dataset/2a1d047c-546b-4293-971a-c835689a37a5/resource/4f013342-5028-447f-b39d-1c08f09f47f3/download/catalogo_centro_trabajo_26_csv.csv'
    ruta_raw = PROJECT_ROOT / 'data' / 'raw'
    nombre_archivo = 'catalogo_escuelas_sonora.csv'
    ruta_guardado = ruta_raw / nombre_archivo
    
    ruta_raw.mkdir(parents=True, exist_ok=True)
    
    if not ruta_guardado.exists():
        try:
            df_catalogo = pd.read_csv(url_catalogo, encoding='latin1', low_memory=False)
            df_catalogo.to_csv(ruta_guardado, index=False, encoding='utf-8')
            
            print(f"✅ Catálogo de escuelas guardado exitosamente en: {ruta_guardado}")
            print(f"   Total de registros: {len(df_catalogo)}")
        
        except Exception as e:
            print(f"❌ Ocurrió un error al descargar o procesar el archivo: {e}")
    else:
        print(f"✓ El archivo '{nombre_archivo}' ya existe. Se omite.")


# ============================================================================
# SECCIÓN 2: DESCARGA DE DATOS DEL INEGI
# ============================================================================

def cargar_configuracion():
    """
    Carga todas las configuraciones necesarias desde la carpeta /references.
    """
    print("\n" + "=" * 70)
    print("INICIANDO DESCARGA DE DATOS DEL INEGI")
    print("=" * 70)
    print("\n--- 1. Cargando configuración ---")
    
    # Cargar el .env desde la raíz del proyecto
    dotenv_path = PROJECT_ROOT / '.env'
    load_dotenv(dotenv_path)
    
    token = os.getenv("INEGI_TOKEN")
    if not token:
        raise ValueError("No se encontró el token de INEGI en el archivo .env")
    
    ruta_referencias = PROJECT_ROOT / 'references'
    
    # Verificar que la carpeta references existe
    if not ruta_referencias.exists():
        raise Exception(f"Error: La carpeta 'references' no existe en {ruta_referencias}")
    
    print(f"Buscando archivos de configuración en: {ruta_referencias}")
    
    try:
        ruta_municipales = ruta_referencias / 'diccionario_inegi_municipio.json'
        ruta_contexto = ruta_referencias / 'diccionario_inegi_contexto.json'
        ruta_dict_municipios = ruta_referencias / 'diccionario_municipios_sonora.json'
        
        # Verificar que los archivos existen
        archivos_requeridos = [
            ('diccionario_inegi_municipio.json', ruta_municipales),
            ('diccionario_inegi_contexto.json', ruta_contexto),
            ('diccionario_municipios_sonora.json', ruta_dict_municipios)
        ]
        
        archivos_faltantes = []
        for nombre, ruta in archivos_requeridos:
            if not ruta.exists():
                archivos_faltantes.append(nombre)
        
        if archivos_faltantes:
            raise Exception(f"Faltan los siguientes archivos en {ruta_referencias}:\n" + 
                          "\n".join(f"  - {archivo}" for archivo in archivos_faltantes))
        
        with open(ruta_municipales, 'r', encoding='utf-8') as f:
            config_municipales = json.load(f)
        with open(ruta_contexto, 'r', encoding='utf-8') as f:
            config_contexto = json.load(f)
        with open(ruta_dict_municipios, 'r', encoding='utf-8') as f:
            municipios = json.load(f)
    
    except FileNotFoundError as e:
        raise Exception(f"Error: No se encontró un archivo de configuración. Detalle: {e}")
    
    print("✅ Configuración cargada exitosamente.")
    return token, config_municipales, config_contexto, municipios


def descargar_datos_municipales(token, config_municipales, municipios):
    """
    Descarga y procesa la serie histórica completa para todos 
    los indicadores a nivel municipal.
    """
    print("\n--- 2. Descargando datos municipales (serie histórica completa) ---")
    
    CLAVE_SONORA = '07000026'
    ruta_external = PROJECT_ROOT / 'data' / 'external'
    ruta_external.mkdir(parents=True, exist_ok=True)
    
    for indicador in config_municipales['indicadores_municipales']:
        nombre_indicador = indicador['nombre']
        id_indicador = indicador['id_inegi']
        
        ruta_csv = ruta_external / f"{nombre_indicador}.csv"
        
        if ruta_csv.exists():
            print(f"\n✓ El archivo '{nombre_indicador}.csv' ya existe. Se omite.")
            continue
        
        print(f"\nProcesando indicador: {nombre_indicador}...")
        
        datos_de_este_indicador = []
        for nombre_mun, codigo_mun in municipios.items():
            ubicacion = CLAVE_SONORA + codigo_mun
            url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{id_indicador}/es/{ubicacion}/false/BISE/2.0/{token}?type=json"
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                observaciones = data['Series'][0]['OBSERVATIONS']
                
                if observaciones:
                    for obs in observaciones:
                        valor = obs['OBS_VALUE']
                        periodo = obs['TIME_PERIOD']
                        
                        if valor is not None:
                            datos_de_este_indicador.append({
                                'municipio': nombre_mun,
                                'periodo': periodo,
                                'valor': float(valor)
                            })
                        else:
                            datos_de_este_indicador.append({
                                'municipio': nombre_mun,
                                'periodo': periodo,
                                'valor': np.nan
                            })
                else:
                    print(f" -> Advertencia: No se encontraron observaciones para {nombre_mun}.")
            
            except Exception as e:
                print(f" -> Error al consultar {nombre_mun}: {e}")
            
            time.sleep(0.1)
        
        if datos_de_este_indicador:
            df = pd.DataFrame(datos_de_este_indicador)
            df = df[['municipio', 'periodo', 'valor']]
            df.to_csv(ruta_csv, index=False, encoding='utf-8')
            print(f" -> ✅ Archivo '{nombre_indicador}.csv' guardado con {len(df)} registros.")


def descargar_datos_contexto(token, config_contexto):
    """
    Descarga y procesa todos los indicadores de contexto (estatales y nacionales).
    """
    print("\n--- 3. Descargando datos de contexto (Estatales/Nacionales) ---")
    
    CLAVE_GEO_SONORA = '07000026'
    CLAVE_GEO_NACIONAL = '0700'
    ruta_external = PROJECT_ROOT / 'data' / 'external'
    ruta_external.mkdir(parents=True, exist_ok=True)
    
    for indicador in config_contexto['indicadores_contexto']:
        nombre_indicador = indicador['nombre']
        id_indicador = indicador['id_inegi']
        
        ruta_csv = ruta_external / f"{nombre_indicador}.csv"
        if ruta_csv.exists():
            print(f"\n✓ El archivo '{nombre_indicador}.csv' ya existe. Se omite.")
            continue
        
        nivel_geo = indicador.get('nivel_geografico', 'estatal')
        fuente_api = indicador.get('fuente_api', 'BISE')
        
        ubicacion = CLAVE_GEO_NACIONAL if nivel_geo == 'nacional' else CLAVE_GEO_SONORA
        
        print(f"\nProcesando indicador '{nombre_indicador}' desde {fuente_api}...")
        
        url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{id_indicador}/es/{ubicacion}/false/{fuente_api}/2.0/{token}?type=json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            observaciones = data['Series'][0]['OBSERVATIONS']
            datos_limpios = [
                {'periodo': obs['TIME_PERIOD'], 'valor': float(obs['OBS_VALUE'])}
                for obs in observaciones if obs['OBS_VALUE'] is not None
            ]
            
            df = pd.DataFrame(datos_limpios)
            df.to_csv(ruta_csv, index=False, encoding='utf-8')
            print(f" -> ✅ Archivo '{nombre_indicador}.csv' guardado.")
        
        except Exception as e:
            print(f" -> ❌ Error al procesar el indicador {nombre_indicador}: {e}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta todas las descargas.
    """
    print("\n" + "=" * 70)
    print("SCRIPT DE DESCARGA UNIFICADO - SEP E INEGI")
    print("=" * 70)
    print(f"\nDirectorio del script: {SCRIPT_DIR}")
    print(f"Raíz del proyecto: {PROJECT_ROOT}")
    
    try:
        # Parte 1: Descargas de la SEP
        descargar_formato_911()
        descargar_catalogo_escuelas()
        
        # Parte 2: Descargas del INEGI
        api_token, conf_municipales, conf_contexto, dict_municipios = cargar_configuracion()
        descargar_datos_municipales(api_token, conf_municipales, dict_municipios)
        descargar_datos_contexto(api_token, conf_contexto)
        
        print("\n" + "=" * 70)
        print("🎉 ¡PROCESO COMPLETO FINALIZADO EXITOSAMENTE!")
        print("=" * 70)
        print(f"\nArchivos guardados en:")
        print(f"  - {PROJECT_ROOT / 'data' / 'raw' / 'formato_911'}")
        print(f"  - {PROJECT_ROOT / 'data' / 'raw' / 'catalogo_escuelas_sonora.csv'}")
        print(f"  - {PROJECT_ROOT / 'data' / 'external'}")
    
    except Exception as e:
        print("\n" + "=" * 70)
        print(f" OCURRIÓ UN ERROR EN EL PROCESO PRINCIPAL:")
        print(f"   {e}")
        print("=" * 70)


if __name__ == "__main__":
    main()
