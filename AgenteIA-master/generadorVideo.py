import os
import requests
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import API

def crear_video_unsplash(api_key=API.unsplashApi, query="", per_page=10, duracion_imagen=2,
                         output_video="video_unsplash.mp4", imagenes_dir="imagenes_unsplash"):
    """
    Crea un video a partir de imágenes obtenidas de la API de Unsplash en formato 1080x1920.

    Parámetros:
    - api_key: Tu API Key de Unsplash.
    - query: Término de búsqueda.
    - per_page: Número de imágenes a obtener.
    - duracion_imagen: Duración en segundos de cada imagen en el video.
    - output_video: Nombre del archivo de video de salida.
    - imagenes_dir: Directorio donde se guardarán las imágenes descargadas.

    Retorna:
    - El nombre del archivo de video generado si tuvo éxito, o None en caso de error.
    """
    # Crear el directorio para guardar imágenes si no existe
    if not os.path.exists(imagenes_dir):
        os.makedirs(imagenes_dir)

    # Configuración de la petición a la API de Unsplash
    unsplash_url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "portrait"  # Para imágenes verticales
    }

    print("Realizando búsqueda en Unsplash...")
    respuesta = requests.get(unsplash_url, headers=headers, params=params)
    if respuesta.status_code != 200:
        print("Error en la petición:", respuesta.status_code, respuesta.text)
        return None

    datos = respuesta.json()
    resultados = datos.get("results", [])
    if not resultados:
        print("No se encontraron imágenes para la consulta.")
        return None

    # Descargar las imágenes
    rutas_imagenes = []
    for i, foto in enumerate(resultados):
        # Obtener la URL "raw" y forzar el tamaño deseado (1080x1920) usando parámetros
        raw_url = foto.get("urls", {}).get("raw")
        if not raw_url:
            continue

        # Agregamos parámetros para que Unsplash entregue la imagen con tamaño 1080x1920
        image_url = f"{raw_url}&w=1080&h=1920&fit=crop"
        print(f"Descargando imagen {i + 1}...")
        resp_imagen = requests.get(image_url)
        if resp_imagen.status_code != 200:
            print("Error al descargar la imagen:", resp_imagen.status_code)
            continue

        ruta_imagen = os.path.join(imagenes_dir, f"imagen_{i + 1}.jpg")
        with open(ruta_imagen, "wb") as f:
            f.write(resp_imagen.content)
        rutas_imagenes.append(ruta_imagen)

    if not rutas_imagenes:
        print("No se pudieron descargar imágenes.")
        return None

    # Crear el video a partir de las imágenes utilizando ImageSequenceClip
    print("Creando el video a partir de las imágenes...")
    fps = 1 / duracion_imagen if duracion_imagen > 0 else 1
    clip = ImageSequenceClip(rutas_imagenes, fps=fps)
    clip.write_videofile(output_video, fps=24)
    print("Video creado con éxito:", output_video)

    return output_video

