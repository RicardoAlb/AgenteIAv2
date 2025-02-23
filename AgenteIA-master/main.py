from pydantic_ai import Agent
import os
import API
import generadorVideo

#CONFIGURACIÓN AGENTE DE IA (DEFINIR MODELO Y PROPÓSITO)
os.environ["GEMINI_API_KEY"] = API.geminiApi
agent = Agent(
    'gemini-2.0-flash-thinking-exp-01-21',
    system_prompt='Eres un experto acerca del derecho urbanístico español y te dedicas a subir shorts a youtube',
)



result = agent.run_sync('Escribe un guión para un video de youtube sobre el derecho urbanístico español.')
imagenQuery = agent.run_sync(f"Elabora una query (máximo 3 palabras) para buscar una imagen que represente el siguiente texto: {result.data}")

print(result.data)
print(imagenQuery.data)


generadorVideo.crear_video_pexels(query=imagenQuery.data)
#TexToAudio.generar_audio(result.data, "audio.mp3")

