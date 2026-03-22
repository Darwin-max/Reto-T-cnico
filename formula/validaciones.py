from datetime import date, datetime

def validar_fecha_fin(fecha_fin: date, fecha_inicio: date) -> dict:
    """Valida que la fecha fin no sea antes que la fecha inicio."""
    if fecha_fin < fecha_inicio:
        return {"valido": False, "mensaje": "La fecha de fin no puede ser antes de la fecha de inicio."}
    return {"valido": True}

def validar_max_dias(fecha_fin: date, fecha_inicio: date) -> dict:
    """Valida que el préstamo no supere los 14 días."""
    dias_solicitados = (fecha_fin - fecha_inicio).days
    if dias_solicitados > 14:
        return {"valido": False, "mensaje": f"El préstamo no puede superar 14 días. Solicitaste {dias_solicitados} días."}
    return {"valido": True}

def validar_fecha_no_pasada(fecha_inicio: date) -> dict:
    """Valida que la fecha de inicio no sea en el pasado."""
    hoy = date.today()
    if fecha_inicio < hoy:
        return {"valido": False, "mensaje": "La fecha de inicio no puede ser en el pasado."}
    return {"valido": True}

def parsear_fecha(fecha_str: str) -> date | None:
    """Convierte un string 'YYYY-MM-DD' a objeto date. Retorna None si el formato es inválido."""
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None
