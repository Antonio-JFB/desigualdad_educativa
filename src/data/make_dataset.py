import os
import requests
from dotenv import load_dotenv

def descargar_pib_sonora():
    load_dotenv()
    INEGI_TOKEN = os.getenv("INEGI_TOKEN")
    if not INEGI_TOKEN:
        raise ValueError("No se encontró el token de INEGI. Asegúrate de definirlo en .env")

    indicador = "6207061405"  # ITAEE Actividades secundarias en Sonora
    url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicador}/es/07000026/false/BISE/2.0/{INEGI_TOKEN}?type=json"

    print(f"Descargando datos de INEGI desde: {url}\n")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error al descargar datos de INEGI: {response.status_code}")

    data = response.json()

    print("Estructura de la respuesta:")
    print(data.keys())

    if "Series" in data:
        for serie in data["Series"]:
            print(f"\nIndicador: {serie.get('INDICADOR', 'N/A')}")
            print(f"Nombre: {serie.get('TITULO', 'N/A')}")
            for obs in serie.get("OBSERVATIONS", []):
                print(f"{obs['TIME_PERIOD']} -> {obs['OBS_VALUE']}")
    else:
        print(" No se encontró la clave 'Series' en la respuesta de INEGI")

if __name__ == "__main__":
    descargar_pib_sonora()
