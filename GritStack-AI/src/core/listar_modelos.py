import os
import json
from dotenv import load_dotenv

# boto3 es la libreria oficial de Amazon para Python.
# Es como un "mando a distancia" que te permite controlar todos los servicios de AWS desde tu codigo.
import boto3

def listar_modelos_disponibles():
    """
    Me conecto a AWS Bedrock y veo qué modelos de IA tengo disponibles.
    Es como preguntar: "Oye Amazon, ¿qué IAs puedo usar?"
    """
    load_dotenv()
    
    # Creo la conexion con Bedrock usando mis credenciales del .env
    cliente_bedrock = boto3.client(
        service_name="bedrock",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    # Pido la lista de modelos disponibles
    respuesta = cliente_bedrock.list_foundation_models()
    
    # Filtro solo los modelos de Anthropic (Claude)
    modelos_claude = []
    for modelo in respuesta["modelSummaries"]:
        if "anthropic" in modelo["modelId"].lower():
            modelos_claude.append({
                "id": modelo["modelId"],
                "nombre": modelo.get("modelName", "Sin nombre"),
                "estado": modelo.get("modelLifecycle", {}).get("status", "desconocido")
            })
    
    return modelos_claude

if __name__ == "__main__":
    print("Buscando modelos de Claude disponibles en tu cuenta de AWS Bedrock...\n")
    
    modelos = listar_modelos_disponibles()
    
    if modelos:
        print(f"Se encontraron {len(modelos)} modelos de Claude:\n")
        for m in modelos:
            print(f"  Modelo: {m['nombre']}")
            print(f"  ID:     {m['id']}")
            print(f"  Estado: {m['estado']}")
            print("-" * 50)
    else:
        print("No se encontraron modelos de Claude. Revisa tu region y permisos.")
