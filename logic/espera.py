import json
from datetime import date


# ──────────────────────────────────────────────
#  CRUD LISTA DE ESPERA
# ──────────────────────────────────────────────

def findAllEspera() -> list:
    with open("data/lista_espera.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())

def saveAllEspera(data: list) -> str:
    with open("data/lista_espera.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False, default=str))
    return "Lista de espera actualizada."

def agregarAEspera(id_usuario: str, id_equipo: str, fecha_fin: date) -> str:
    """Agrega un usuario a la lista de espera de un equipo."""
    lista = findAllEspera()
    lista.append({
        "id_usuario": id_usuario,
        "id_equipo": id_equipo,
        "fecha_solicitud": str(date.today()),
        "fecha_fin_deseada": str(fecha_fin),
        "estado": "esperando"
    })
    return saveAllEspera(lista)
