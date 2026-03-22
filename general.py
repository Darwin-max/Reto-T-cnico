from design.menu import mostrarMenuPrincipal
from design.empleado import (formularioLogin, formularioSolicitarPrestamo, tablaPrestamosActivos, formularioDevolucion, tablaEquipos)



def iniciar():
    print(" ╔══════════════════════════════════════════════╗")
    print(" ║     Bienvenido al Sistema de Préstamos TI    ║")
    print(" ╚══════════════════════════════════════════════╝")

    usuario = formularioLogin()
    if not usuario:
        print("Acceso denegado. Cerrando sistema.")
        return

    while True:
        opcion = mostrarMenuPrincipal()

        match opcion:
            case "1":
                formularioSolicitarPrestamo(usuario)
            case "2":
                tablaPrestamosActivos(usuario)
            case "3":
                formularioDevolucion(usuario)
            case "4":
                tablaEquipos()
            case "0":
                print("Sesión cerrada.")
                break
            case _:
                print("Opción no válida. Intenta de nuevo.")
