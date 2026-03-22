from logic.usuarios import findByEmail


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