import os
import json
from dotenv import load_dotenv

# LangChain es la libreria que nos simplifica hablar con modelos de IA.
# ChatBedrockConverse es la "version LangChain" de conectarse a AWS Bedrock.
from langchain_aws import ChatBedrockConverse

def crear_modelo_ia():
    """
    Creo y devuelvo una conexion con Claude Sonnet 4.6 a traves de AWS Bedrock.
    Es como encender mi "telefono" para poder llamar a la IA.
    """
    load_dotenv()
    
    import boto3
    # 1. Creo el cliente de Amazon (boto3) leyendo mis claves del .env automáticamente
    cliente_bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    # 2. Conecto LangChain usando ese cliente
    # NOTA: AWS Bedrock ahora me requiere usar "Perfiles de inferencia" (Inference Profiles) para los modelos nuevos.
    # Por eso le pongo el prefijo "us." delante del ID del modelo.
    modelo = ChatBedrockConverse(
        model="us.anthropic.claude-sonnet-4-6",
        client=cliente_bedrock,
        temperature=0.3,
        max_tokens=4096
    )
    
    return modelo

def analizar_perfil(datos_perfil: dict):
    """
    Recibo los datos del perfil de GitHub (el JSON que generé) y se los envío
    a Claude para que haga un analisis profesional.
    
    El 'prompt' es la instruccion que le doy a la IA. Cuanto mejor sea el prompt,
    mejor sera la respuesta. Esto se llama 'Prompt Engineering'.
    """
    modelo = crear_modelo_ia()
    
    # Convierto el diccionario a texto JSON para que la IA pueda leerlo
    datos_texto = json.dumps(datos_perfil, ensure_ascii=False, indent=2)
    
    # Este es el PROMPT: la instrucción detallada que le doy a Claude.
    # Fíjate en que le pido cosas muy concretas para que no se invente nada.
    prompt = f"""Eres un analista de talento tecnologico experto. 
Te voy a pasar los datos del perfil de GitHub de un desarrollador. 
Contiene sus repositorios, lenguajes usados (con bytes que indican cuanto ha programado en cada uno), 
descripciones de proyectos y el contenido de sus README.

DATOS DEL PERFIL:
{datos_texto}

Analiza todo y devuelveme un informe estructurado con estas secciones:

1. **RESUMEN PROFESIONAL**: Un parrafo describiendo el perfil del desarrollador.
2. **HABILIDADES TECNICAS CONFIRMADAS**: Lista solo las tecnologias que realmente ha usado, 
   agrupadas por categoria (Lenguajes, Frameworks, Bases de Datos, DevOps/Infra, Otros).
   Ignora tecnologias irrelevantes como 'url', 'Inno Setup' o 'Batchfile' a no ser que sean significativas.
3. **PROYECTOS DESTACADOS**: Los 3 proyectos mas impresionantes, con una breve explicacion de por que destacan.
4. **AREAS DE MEJORA**: Que habilidades le faltarian para ser un perfil mas competitivo.
5. **PUESTOS RECOMENDADOS**: 3 puestos de trabajo que encajarian con este perfil.

Se objetivo y basate unicamente en la evidencia real de los datos. No inventes habilidades que no aparezcan."""

    # Aquí es donde ocurre la magia: envío el prompt a Claude y espero su respuesta
    # .invoke() es el metodo de LangChain que "llama" a la IA
    respuesta = modelo.invoke(prompt)
    
    # La respuesta me viene dentro de .content (es un objeto, no un string directo)
    return respuesta.content

# Solo se ejecuta si lanzo este archivo directamente desde la terminal
if __name__ == "__main__":
    # 1. Busco el archivo JSON con los datos del perfil
    archivos_json = [f for f in os.listdir(".") if f.startswith("perfil_") and f.endswith(".json")]
    
    if not archivos_json:
        print("No se encontro ningun archivo perfil_*.json. Ejecuta primero github_parser.py")
    else:
        archivo = archivos_json[0]
        print(f"Leyendo datos de: {archivo}")
        
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        print(f"Se encontraron {len(datos['repositorios'])} repositorios.")
        print("Enviando datos a Claude Sonnet 4.6 para analisis... (esto puede tardar 15-30 segundos)\n")
        
        resultado = analizar_perfil(datos)
        
        print("=" * 60)
        print("INFORME DE PERFIL PROFESIONAL - GritStack AI")
        print("=" * 60)
        
        # Guardo el informe en un archivo Markdown (que soporta los emojis perfectamente)
        nombre_informe = "informe_profesional.md"
        with open(nombre_informe, "w", encoding="utf-8") as f:
            f.write(resultado)
        
        print(f"\nInforme generado con éxito!")
        print(f"Por problemas con los emojis en la consola de Windows, no lo imprimo por aqui.")
        print(f"Por favor, abre el archivo '{nombre_informe}' en tu editor para ver el resultado.")
