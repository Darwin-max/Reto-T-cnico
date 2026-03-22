def mostrarMenuPrincipal() -> str:
    print("""
    ╔══════════════════════════════════════════════╗
    ║     Sistema de Préstamo de Equipos TI        ║
    ╠══════════════════════════════════════════════╣
    ║  1. Solicitar préstamo                       ║
    ║  2. Ver mis préstamos activos                ║
    ║  3. Devolver equipo                          ║
    ║  4. Ver equipos disponibles                  ║
    ║  0. Cerrar sesión                            ║
    ╚══════════════════════════════════════════════╝
    """)
    return input("Selecciona una opción: ").strip()
