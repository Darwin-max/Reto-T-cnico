import json

def findAll() -> list:
    with open("data/equipos.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())

def saveAll(data: list) -> str:

    with open("data/equipos.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))
    return "Equipos actualizados correctamente."

def findById(id_equipo: str) -> dict | None:
    equipos = findAll()
    resultado = list(filter(lambda e: e.get("id_equipo") == id_equipo, equipos))
    return resultado[0] if resultado else None

def findDisponiblesByTipo(tipo: str) -> list:
    equipos = findAll()
    return list(filter(lambda e: e.get("tipo") == tipo and e.get("estado") == "disponible", equipos))

def actualizarEstado(id_equipo: str, nuevo_estado: str) -> str:

    equipos = findAll()
    for equipo in equipos:
        if equipo.get("id_equipo") == id_equipo:
            equipo["estado"] = nuevo_estado
    return saveAll(equipos)
