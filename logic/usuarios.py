import json

def findAll() -> list:
    with open("data/usuarios.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())

def findByEmail(email: str) -> dict | None:
    usuarios = findAll()
    resultado = list(filter(lambda u: u.get("email") == email, usuarios))
    return resultado[0] if resultado else None

def findById(id_usuario: str) -> dict | None:
    usuarios = findAll()
    resultado = list(filter(lambda u: u.get("id_usuario") == id_usuario, usuarios))
    return resultado[0] if resultado else None
