from logic.usuarios import findByEmail
from logic.prestamos import solicitarPrestamo, findActivosByUsuario, devolverEquipo
from logic.equipos import findAll as findAllEquipos
from datetime import date
from tabulate import tabulate
from formula.validaciones import parsear_fecha
from logic.espera import agregarAEspera

def formularioLogin() -> dict | None:
    print("── Inicio de Sesión ──")
    email    = input("Email: ").strip()
    password = input("Contraseña: ").strip()

    usuario = findByEmail(email)
    if usuario and usuario.get("password") == password:
        print(f"Bienvenido, {usuario['nombre']} ({usuario['cargo']})")
        return usuario

    print(" Email o contraseña incorrectos.")
    return None



# prestamooooo

def formularioSolicitarPrestamo(usuario: dict):
    equipos = findAllEquipos()
    disponibles = list(filter(lambda e: e.get("estado") == "disponible", equipos))

    print("── Equipos disponibles ──")
    if not disponibles:
        print("No hay equipos disponibles en este momento.")
        return

    print(tabulate(disponibles, headers="keys", tablefmt="grid", numalign="center", showindex="always"))

    id_equipo = input("Ingresa el ID del equipo que deseas (ej. EQ-001): ").strip().upper()
    fecha_fin_str = input("¿Hasta qué fecha lo necesitas? (YYYY-MM-DD): ").strip()

    fecha_fin = parsear_fecha(fecha_fin_str)
    if not fecha_fin:
        print("Formato de fecha inválido. Usa YYYY-MM-DD.")
        return

    resultado = solicitarPrestamo(usuario["id_usuario"], id_equipo, fecha_fin)

    if resultado["exito"]:
        print(f"{resultado['mensaje']}")
        print(tabulate([resultado["detalle"]], headers="keys", tablefmt="grid"))
    else:
        print(f"{resultado['mensaje']}")

        # Si el equipo no está disponible, mostrar opciones
        if not resultado.get("disponible", True):
            opciones = resultado.get("opciones", {})
            print(f"Opción 1 → {opciones.get('espera')}")
            alternativas = opciones.get("alternativas")
            if isinstance(alternativas, list) and alternativas:
                print("Opción 2 → Equipos alternativos disponibles del mismo tipo:")
                print(tabulate(alternativas, headers="keys", tablefmt="grid"))

            eleccion = input("¿Qué deseas hacer? (1 = Lista de espera / 2 = Ver alternativa / 0 = Cancelar): ").strip()

            if eleccion == "1":
                fecha_fin = parsear_fecha(fecha_fin_str)
                agregarAEspera(usuario["id_usuario"], id_equipo, fecha_fin)
                print("Fuiste agregado a la lista de espera.")

            elif eleccion == "2" and isinstance(alternativas, list) and alternativas:
                id_alt = input("Ingresa el ID del equipo alternativo: ").strip().upper()
                resultado_alt = solicitarPrestamo(usuario["id_usuario"], id_alt, fecha_fin)
                if resultado_alt["exito"]:
                    print(f"{resultado_alt['mensaje']}")
                    print(tabulate([resultado_alt["detalle"]], headers="keys", tablefmt="grid"))
                else:
                    print(f"{resultado_alt['mensaje']}")
            else:
                print("Solicitud cancelada.")


# ver prestamos activos que el empleado a solicitado   


def tablaPrestamosActivos(usuario: dict):
    """Muestra los préstamos activos del usuario."""
    prestamos = findActivosByUsuario(usuario["id_usuario"])
    print("── Tus préstamos activos ──")
    if not prestamos:
        print("No tienes préstamos activos.")
        return
    print(tabulate(prestamos, headers="keys", tablefmt="grid"))


# ──────────────────────────────────────────────
#  DEVOLVER EQUIPO
# ──────────────────────────────────────────────

def formularioDevolucion(usuario: dict):
    """Flujo para devolver un equipo."""
    prestamos = findActivosByUsuario(usuario["id_usuario"])
    if not prestamos:
        print("No tienes préstamos activos para devolver.")
        return
    print("── Tus préstamos activos ──")
    print(tabulate(prestamos, headers="keys", tablefmt="grid"))
    id_prestamo = input("\nIngresa el ID del préstamo a devolver (ej. PR-001): ").strip().upper()
    mensaje = devolverEquipo(id_prestamo)
    print(f"{mensaje}")
