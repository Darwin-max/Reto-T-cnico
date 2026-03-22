import json
from datetime import date
from logic.equipos import findById as findEquipoById, findDisponiblesByTipo, actualizarEstado
from logic.usuarios import findById as findUsuarioById
from formula.validaciones import validar_fecha_fin, validar_max_dias


# ──────────────────────────────────────────────
#  CRUD PRÉSTAMOS
# ──────────────────────────────────────────────

def findAll() -> list:
   
    with open("data/prestamos.json", "r", encoding="utf-8") as file: #Recorrer todos los prestamos todos los préstamos."""
        return json.loads(file.read())

def saveAll(data: list) -> str:
    """Guarda la lista de préstamos en el JSON."""
    with open("data/prestamos.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False, default=str))
    return "Préstamos guardados correctamente."

def findActivosByUsuario(id_usuario: str) -> list:
    """Retorna los préstamos activos de un usuario."""
    prestamos = findAll()
    return list(filter(lambda p: p.get("id_usuario") == id_usuario and p.get("estado") == "activo", prestamos))


# ──────────────────────────────────────────────
#  funcion principal solicitar un prestamo 
# ──────────────────────────────────────────────

def solicitarPrestamo(id_usuario: str, id_equipo: str, fecha_fin: date) -> dict:

    fecha_inicio = date.today()
    # ── Validar que el usuario existe ──
    usuario = findUsuarioById(id_usuario)
    if not usuario:
        return {"exito": False, "mensaje": "Usuario no encontrado."}

    # ── Validar que el equipo existe ──
    equipo = findEquipoById(id_equipo)
    if not equipo:
        return {"exito": False, "mensaje": "Equipo no encontrado."}

    # ── Validar fechas ──
    resultado_fecha = validar_fecha_fin(fecha_fin, fecha_inicio)
    if not resultado_fecha["valido"]:
        return {"exito": False, "mensaje": resultado_fecha["mensaje"]}

    resultado_dias = validar_max_dias(fecha_fin, fecha_inicio)
    if not resultado_dias["valido"]:
        return {"exito": False, "mensaje": resultado_dias["mensaje"]}

    # ── Validar que el usuario no tenga ya un préstamo activo del mismo tipo ──
    prestamos_activos = findActivosByUsuario(id_usuario)
    tipos_activos = [findEquipoById(p["id_equipo"])["tipo"] for p in prestamos_activos if findEquipoById(p["id_equipo"])]
    if equipo["tipo"] in tipos_activos:
        return {
            "exito": False,
            "mensaje": f"Ya tienes un préstamo activo de tipo '{equipo['tipo']}'. Devuélvelo antes de solicitar otro."
        }

    # ── Validar disponibilidad del equipo ──
    if equipo["estado"] != "disponible":
        alternativas = findDisponiblesByTipo(equipo["tipo"])
        alternativas_sin_el = list(filter(lambda e: e["id_equipo"] != id_equipo, alternativas))
        return {
            "exito": False,
            "disponible": False,
            "mensaje": f"El equipo {equipo['marca']} {equipo['modelo']} no está disponible.",
            "opciones": {
                "espera": f"Puedes unirte a la lista de espera para este equipo.",
                "alternativas": alternativas_sin_el if alternativas_sin_el else "No hay equipos alternativos disponibles del mismo tipo."
            }
        }

    # ── Registrar el préstamo ──
    prestamos = findAll()
    nuevo_id = len(prestamos) + 1
    nuevo_prestamo = {
        "id_prestamo": f"PR-{str(nuevo_id).zfill(3)}",
        "id_usuario": id_usuario,
        "id_equipo": id_equipo,
        "fecha_inicio": str(fecha_inicio),
        "fecha_fin": str(fecha_fin),
        "estado": "activo"
    }
    prestamos.append(nuevo_prestamo)
    saveAll(prestamos)

    # ── Actualizar estado del equipo ──
    actualizarEstado(id_equipo, "prestado")

    return {
        "exito": True,
        "mensaje": f"Préstamo registrado exitosamente.",
        "detalle": nuevo_prestamo
    }


def devolverEquipo(id_prestamo: str) -> str:
    """Marca un préstamo como finalizado y libera el equipo."""
    prestamos = findAll()
    for prestamo in prestamos:
        if prestamo.get("id_prestamo") == id_prestamo and prestamo.get("estado") == "activo":
            prestamo["estado"] = "finalizado"
            actualizarEstado(prestamo["id_equipo"], "disponible")
            saveAll(prestamos)
            return f"Equipo devuelto correctamente. Préstamo {id_prestamo} finalizado."
    return "Préstamo no encontrado o ya finalizado."
