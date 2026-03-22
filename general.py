from design.empleado import formularioLogin


def iniciar():
    print(" ╔══════════════════════════════════════════════╗")
    print(" ║     Bienvenido al Sistema de Préstamos TI    ║")
    print(" ╚══════════════════════════════════════════════╝")

    usuario = formularioLogin()
    if not usuario:
        print("Acceso denegado. Cerrando sistema.")
        return
