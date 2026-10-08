# Pydroid run tkinter
# CHRONICLES OF THE FALLEN KING
# Versión adaptada para Pydroid 3 / Android con controles táctiles mejorados, más grandes y decorados.
import math
import random
import time
import turtle

# Configuración de la ventana principal
ventana = turtle.Screen()
ventana.title("CHRONICLES OF THE FALLEN KING - ARENA TOP-DOWN")
ventana.bgcolor("#0a0510")
ventana.setup(width=900, height=650)
ventana.tracer(0)

es_pantalla_completa = False


# ============================================================
# COMPATIBILIDAD Pydroid 3 / ANDROID
# ============================================================
MODO_MOBILE = True
mobile_flechas = {"up": False, "down": False, "left": False, "right": False}
joystick_activo = False
joystick_x = 0.0
joystick_y = 0.0
mobile_canvas = None
mobile_ui = None


def _mobile_coord(event):
    """Convierte coordenadas del Canvas de Tk a coordenadas de turtle."""
    canvas = ventana.getcanvas()
    try:
        w = int(canvas.winfo_width())
        h = int(canvas.winfo_height())
    except Exception:
        w, h = 800, 600
    return event.x - w / 2, h / 2 - event.y


def _mobile_en_circulo(x, y, cx, cy, radio):
    return math.hypot(x - cx, y - cy) <= radio


def dibujar_controles_mobile():
    """Interfaz táctil de Pydroid 3: flechas, espada y menú de pausa decorados y más grandes."""
    global mobile_ui
    if not MODO_MOBILE:
        return
    if mobile_ui is None:
        mobile_ui = turtle.Turtle(visible=False)
        mobile_ui.speed(0)
        mobile_ui.penup()
    mobile_ui.clear()

    if estado_juego == "INICIO":
        titulo_txt.clear()
        cuadro_ui.clear()
        mobile_ui.goto(0, 190)
        mobile_ui.color("gold")
        mobile_ui.write(
            "CHRONICLES OF THE FALLEN KING",
            align="center",
            font=("Arial", 18, "bold"),
        )
        mobile_ui.goto(0, 160)
        mobile_ui.color("#ff5522")
        mobile_ui.write(
            "SUPERA 10 PASILLOS PARA DESBLOQUEAR LOS JEFES",
            align="center",
            font=("Arial", 8, "bold"),
        )
        opciones = [
            (110, "PASILLOS NORMAL", True),
            (60, "JEFE NORMAL", boss_normal_desbloqueado),
            (10, "PASILLOS DEMON", demon_mode_desbloqueado),
            (-40, "JEFE DEMON", boss_demon_desbloqueado),
            (-90, "PASILLOS INFERNO", inferno_mode_desbloqueado),
            (-140, "JEFE INFERNO", boss_inferno_desbloqueado),
        ]
        for y, texto, activo in opciones:
            mobile_ui.goto(0, y)
            mobile_ui.color("#164d32" if activo else "#292934")
            mobile_ui.dot(40)
            mobile_ui.color("white" if activo else "#777777")
            mobile_ui.write(texto, align="center", font=("Arial", 8, "bold"))
        mobile_ui.goto(0, -195)
        mobile_ui.color("#00ffff")
        mobile_ui.write(
            "TOCA UNA OPCION PARA JUGAR",
            align="center",
            font=("Arial", 9, "bold"),
        )
        return

    if estado_juego in ("JUGANDO", "PAUSA"):
        # Flechas de control decoradas y más grandes
        for cx, cy, simbolo in [
            (-385, -135, "▲"),
            (-435, -195, "◀"),
            (-385, -255, "▼"),
            (-335, -195, "▶"),
        ]:
            # Anillo decorativo exterior dorado
            mobile_ui.goto(cx, cy)
            mobile_ui.color("#ffd700")
            mobile_ui.dot(68)
            # Fondo principal oscuro del botón
            mobile_ui.color("#111828")
            mobile_ui.dot(60)
            # Centro decorativo
            mobile_ui.color("#1e2942")
            mobile_ui.dot(48)
            # Simbolo de dirección
            mobile_ui.color("#00ffff")
            mobile_ui.write(
                simbolo, align="center", font=("Arial", 22, "bold")
            )

        # Botón Espada Decorado y más grande (Extrema derecha)
        # Resplandor dorado / borde ornamental exterior
        mobile_ui.goto(375, -195)
        mobile_ui.color("gold")
        mobile_ui.dot(115)
        # Capa roja externa
        mobile_ui.color("#7a0e19")
        mobile_ui.dot(105)
        # Capa roja interna vibrante
        mobile_ui.color("#e22b3d")
        mobile_ui.dot(92)
        # Núcleo oscuro brillante
        mobile_ui.color("#3b050c")
        mobile_ui.dot(70)
        # Texto con estilo
        mobile_ui.color("gold")
        mobile_ui.write("⚔ ESPADA ⚔", align="center", font=("Arial", 10, "bold"))

        # Menús superiores (Desplazados a la derecha superior extrema)
        for x, texto_boton in ((310, "SKIN"), (360, "MENU"), (410, "II")):
            mobile_ui.goto(x, 220)
            mobile_ui.color("gold")
            mobile_ui.dot(48)
            mobile_ui.color("#1c273e")
            mobile_ui.dot(42)
            mobile_ui.color("white")
            mobile_ui.write(
                texto_boton,
                align="center",
                font=("Arial", 8 if texto_boton != "II" else 12, "bold"),
            )

        if estado_juego == "PAUSA":
            mobile_ui.goto(0, 25)
            mobile_ui.color("#080611")
            mobile_ui.dot(420)
            mobile_ui.goto(0, 110)
            mobile_ui.color("yellow")
            mobile_ui.write(
                "JUEGO EN PAUSA", align="center", font=("Arial", 22, "bold")
            )
            mobile_ui.goto(0, 30)
            mobile_ui.color("#164d32")
            mobile_ui.dot(125)
            mobile_ui.color("white")
            mobile_ui.write(
                "REANUDAR", align="center", font=("Arial", 11, "bold")
            )
            mobile_ui.goto(0, -65)
            mobile_ui.color("#6b1720")
            mobile_ui.dot(125)
            mobile_ui.color("white")
            mobile_ui.write(
                "SALIR", align="center", font=("Arial", 11, "bold")
            )


def mobile_touch_down(event):
    """Maneja el inicio de los toques táctiles con posiciones ajustadas."""
    global estado_juego
    x, y = _mobile_coord(event)

    if estado_juego == "INICIO":
        if 85 <= y <= 135:
            procesar_v()
        elif 35 <= y < 85:
            procesar_enter()
        elif -15 <= y < 35:
            procesar_b()
        elif -65 <= y < -15:
            procesar_w()
        elif -115 <= y < -65:
            procesar_m()
        elif -165 <= y < -115:
            procesar_n()
        dibujar_controles_mobile()
        return

    if estado_juego in ("FIN_VICTORIA", "FIN_DERROTA", "FIN_PASILLO_VICTORIA"):
        procesar_enter()
        return

    if estado_juego == "PAUSA":
        if _mobile_en_circulo(x, y, 0, 30, 63):
            estado_juego = "JUGANDO"
        elif _mobile_en_circulo(x, y, 0, -65, 63):
            salir_al_titulo()
        dibujar_controles_mobile()
        return

    if estado_juego == "JUGANDO":
        # Flechas de movimiento (Ajustadas a tamaños mayores)
        for nombre, cx, cy in [
            ("up", -385, -135),
            ("left", -435, -195),
            ("down", -385, -255),
            ("right", -335, -195),
        ]:
            if _mobile_en_circulo(x, y, cx, cy, 55):
                mobile_flechas[nombre] = True

        # Ataque con Espada (Hitbox ampliada para botón más grande)
        if _mobile_en_circulo(x, y, 375, -195, 70):
            realizar_ataque()
            return

        # Botones UI superiores
        if _mobile_en_circulo(x, y, 310, 220, 28):
            cambiar_skin_heroe()
            dibujar_controles_mobile()
            return
        if _mobile_en_circulo(x, y, 360, 220, 28) or _mobile_en_circulo(
            x, y, 410, 220, 28
        ):
            estado_juego = "PAUSA"
            dibujar_controles_mobile()


def mobile_touch_move(event):
    """Permite mantener o cambiar la dirección deslizando el dedo."""
    if estado_juego != "JUGANDO":
        return
    x, y = _mobile_coord(event)
    for nombre, cx, cy in [
        ("up", -385, -135),
        ("left", -435, -195),
        ("down", -385, -255),
        ("right", -335, -195),
    ]:
        mobile_flechas[nombre] = _mobile_en_circulo(x, y, cx, cy, 55)


def mobile_touch_up(event):
    """Resetea las direcciones cuando se levanta el dedo."""
    for k in mobile_flechas:
        mobile_flechas[k] = False


def instalar_controles_pydroid():
    try:
        canvas = ventana.getcanvas()
        canvas.bind("<ButtonPress-1>", mobile_touch_down, add="+")
        canvas.bind("<B1-Motion>", mobile_touch_move, add="+")
        canvas.bind("<ButtonRelease-1>", mobile_touch_up, add="+")
        return True
    except Exception as e:
        print("Controles táctiles no disponibles:", e)
        return False


def alternar_pantalla_completa(event=None):
    """Permite cambiar a pantalla completa o regresar a ventana con F11 o F."""
    global es_pantalla_completa
    es_pantalla_completa = not es_pantalla_completa
    try:
        canvas = ventana.getcanvas()
        root = canvas.winfo_toplevel()
        root.attributes("-fullscreen", es_pantalla_completa)

        if es_pantalla_completa:
            ancho_pantalla = root.winfo_screenwidth()
            alto_pantalla = root.winfo_screenheight()
            ventana.setup(width=ancho_pantalla, height=alto_pantalla)
        else:
            ventana.setup(width=900, height=650)

        canvas.config(width=root.winfo_width(), height=root.winfo_height())
    except Exception as e:
        print("Error al cambiar modo de pantalla:", e)


# Estados y Modos de Juego
estado_juego = "INICIO"
demon_mode_desbloqueado = False
inferno_mode_desbloqueado = False
modo_actual = "NORMAL"

# Sistema de Pasillos (10 pasillos obligatorios antes de cada jefe)
pasillo_objetivo = "NORMAL"
pasillo_actual_num = 1
TOTAL_PASILLOS = 10

boss_normal_desbloqueado = False
boss_demon_desbloqueado = False
boss_inferno_desbloqueado = False

# Constantes de Salud y Combate
MAX_SALUD_HEROE_PASILLO = 1500
MAX_SALUD_HEROE_NORMAL = 8000
MAX_SALUD_HEROE_DEMON = 12000
MAX_SALUD_HEROE_INFERNO = 18000

MAX_SALUD_DEMONIO_NORMAL = 250000
MAX_SALUD_DEMONIO_DEMON = 500000
MAX_SALUD_DEMONIO_INFERNO = 1000000

DANO_HEROE = 450

max_salud_heroe_actual = MAX_SALUD_HEROE_NORMAL
max_salud_demonio_actual = MAX_SALUD_DEMONIO_NORMAL

salud_heroe = max_salud_heroe_actual
salud_demonio = max_salud_demonio_actual

# Temporizadores del juego
tiempo_ultimo_ataque_t = time.time()
tiempo_ultima_frase = time.time()
tiempo_ultima_frase_secuas = time.time()
tiempo_ultimo_ataque_demonio = time.time()
tiempo_ultimo_secuas = time.time()
tiempo_inicio_pasillo = 0
DURACION_PASILLO = 30.0

tiempo_inicio_animacion = 0
frame_brillo = 0
frame_alarma = 0
frame_fuego = 0

# Skins/Pieles del héroe
skins_heroe = [
    {"capa": "firebrick", "cuerpo": "dodgerblue", "cabeza": "gold"},
    {"capa": "#8a2be2", "cuerpo": "#00ffff", "cabeza": "white"},
    {"capa": "#2e8b57", "cuerpo": "#3cb371", "cabeza": "#e0ffff"},
    {"capa": "#ff1493", "cuerpo": "#ff69b4", "cabeza": "#ffe4e1"},
    {"capa": "#ff8c00", "cuerpo": "#ffd700", "cabeza": "#ffffff"},
]
skin_actual_idx = 0

# Variables del Botiquín (Medkit)
botiquin_activo = False
botiquin_pos = (0, 0)
tiempo_spawn_botiquin = time.time() + random.uniform(8, 12)
tiempo_expiracion_botiquin = 0
DURACION_BOTIQUIN = 5.0
CURACION_BOTIQUIN = 2500

# Control suave de teclado
teclas = {
    "Up": False,
    "Down": False,
    "Left": False,
    "Right": False,
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "m": False,
}

# Frases de Enemigos
frases_secuaces = [
    "¡No dejaré que advances más!",
    "¡El Rey Caído devorará tu alma!",
    "¡Nunca llegarás con el Jefe!",
    "¡Tu viaje termina en este pasillo!",
    "¡Caerás ante las sombras!",
    "¡Somos legión, no puedes vencernos!",
]

frases_demonio_normal = [
    "¡Siente la desesperación, mortal!",
    "¡No podrás huir de mi sombra!",
    "¡Cada paso que das me acerca a tu fin!",
    "¡Tus ataques son insignificantes!",
    "¡Esta arena será tu tumba!",
    "¡Arrodíllate ante el verdadero Rey!",
]

frases_demonio_demon = [
    "¡MI PODER DEMONÍACO ABSORBERÁ TU ESPÍRITU!",
    "¡NADA EN ESTE MUNDO SALVARÁ TU MISERABLE ALMA!",
    "¡SIENTE EL VERDADERO TERROR DE LAS TINIEBLAS!",
    "¡TU FEBLE ESPADA SE ROMPERÁ EN PEDAZOS!",
    "¡VOY A CONSUMIR HASTA EL ÚLTIMO SOPLO DE TU VIDA!",
    "¡EL ABISMO SE ALIMENTARÁ CON TU SANGRE!",
]

frases_demonio_inferno = [
    "¡BIENVENIDO AL INFIERNO, MISERABLE MORTAL!",
    "¡TODA ESPERANZA SE HA CONSUMIDO EN LAS LLAMAS!",
    "¡ESTE REINO HA SIDO COMPLETAMENTE DESTRUIDO!",
    "¡SOY EL FIN DE ESTE MUNDO Y DE TU EXISTENCIA!",
    "¡ARDE EN LAS LLAMAS ETERNAS DE LA PERDICIÓN!",
    "¡NADA SOBREVIVIRÁ A MI PODER ABSOLUTO!",
]

fondo = turtle.Turtle()
fondo.speed(0)
fondo.penup()
fondo.hideturtle()


def obtener_dano_proyectil_jefe():
    if modo_actual == "INFERNO":
        return 1500
    elif modo_actual == "DEMON":
        return 750
    return 350


def obtener_dano_contacto_jefe():
    if modo_actual == "INFERNO":
        return 180.0
    elif modo_actual == "DEMON":
        return 90.0
    return 40.0


def verificar_modo_moderador():
    global demon_mode_desbloqueado, inferno_mode_desbloqueado
    global boss_normal_desbloqueado, boss_demon_desbloqueado, boss_inferno_desbloqueado

    if estado_juego == "INICIO" and teclas["a"]:
        demon_mode_desbloqueado = True
        inferno_mode_desbloqueado = True
        boss_normal_desbloqueado = True
        boss_demon_desbloqueado = True
        boss_inferno_desbloqueado = True
        mostrar_menu(modo_moderador_activado=True)


def dibujar_escenario_topdown():
    fondo.clear()

    if modo_actual == "PASILLO":
        color_pared = "#140e1f"
        color_piso = "#0a0712"
        color_grid = "#1d152c"

        fondo.goto(-260, 290)
        fondo.color(color_pared)
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(520)
            fondo.right(90)
            fondo.forward(580)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-240, 270)
        fondo.color(color_piso)
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(480)
            fondo.right(90)
            fondo.forward(540)
            fondo.right(90)
        fondo.end_fill()

        fondo.color(color_grid)
        fondo.pensize(2)
        for y in range(-270, 280, 45):
            fondo.goto(-240, y)
            fondo.pendown()
            fondo.goto(240, y)
            fondo.penup()

        fondo.goto(-80, 260)
        fondo.color("#3d1d0c")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(160)
            fondo.right(90)
            fondo.forward(30)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-75, 255)
        fondo.color("gold")
        fondo.pensize(3)
        fondo.pendown()
        fondo.forward(150)
        fondo.right(90)
        fondo.forward(20)
        fondo.right(90)
        fondo.forward(150)
        fondo.right(90)
        fondo.forward(20)
        fondo.penup()

        for ty in [-180, -60, 60, 180]:
            for tx in [-220, 220]:
                fondo.goto(tx, ty)
                fondo.color("#000000")
                fondo.dot(18)
                fondo.color("crimson")
                fondo.dot(12)
                fondo.color("gold")
                fondo.dot(6)
        return

    elif modo_actual == "INFERNO":
        color_pared = "#220000"
        color_piso = "#0d0203"
        color_grid = "#33080c"
    elif modo_actual == "DEMON":
        color_pared = "#3a0505"
        color_piso = "#1f050a"
        color_grid = "#420d18"
    else:
        color_pared = "#2a1836"
        color_piso = "#181524"
        color_grid = "#252033"

    fondo.goto(-390, 290)
    fondo.color(color_pared)
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(780)
        fondo.right(90)
        fondo.forward(580)
        fondo.right(90)
    fondo.end_fill()

    fondo.goto(-370, 270)
    fondo.color(color_piso)
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(740)
        fondo.right(90)
        fondo.forward(540)
        fondo.right(90)
    fondo.end_fill()

    if modo_actual == "INFERNO":
        fondo.pensize(5)
        fondo.color("#ff2200")
        grietas = [
            [(-300, 200), (-150, 80), (-50, 120), (100, -20)],
            [(200, 220), (80, 100), (180, -100), (320, -180)],
            [(-250, -180), (-100, -80), (50, -200), (220, -220)],
            [(-100, 180), (0, 40), (120, 60), (250, -40)],
        ]
        for grieta in grietas:
            fondo.penup()
            fondo.goto(grieta[0])
            fondo.pendown()
            for pt in grieta[1:]:
                fondo.goto(pt)
            fondo.penup()

    fondo.color(color_grid)
    fondo.pensize(2)

    for y in range(-270, 280, 60):
        fondo.goto(-370, y)
        fondo.pendown()
        fondo.goto(370, y)
        fondo.penup()

    for x in range(-370, 380, 60):
        fondo.goto(x, -270)
        fondo.pendown()
        fondo.goto(x, 270)
        fondo.penup()

    fondo.goto(0, -90)
    fondo.color(
        "#770000"
        if modo_actual == "INFERNO"
        else ("#521d1d" if modo_actual == "DEMON" else "#3d1d52")
    )
    fondo.pensize(4)
    fondo.pendown()
    fondo.circle(90)
    fondo.penup()

    if modo_actual == "INFERNO":
        escombros = [
            (-50, 210, 45),
            (20, 220, 40),
            (-10, 190, 55),
            (40, 195, 35),
            (-80, 200, 30),
            (70, 215, 38),
        ]
        for ex, ey, tam in escombros:
            fondo.goto(ex, ey)
            fondo.color("#331111")
            fondo.dot(tam)
            fondo.color("#ff3300")
            fondo.dot(tam // 3)
    else:
        fondo.goto(-80, 250)
        fondo.color("#120718")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(160)
            fondo.right(90)
            fondo.forward(110)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-65, 240)
        fondo.color("#251433")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(130)
            fondo.right(90)
            fondo.forward(90)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-25, 240)
        fondo.color("#800c1e")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(50)
            fondo.right(90)
            fondo.forward(140)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-45, 235)
        fondo.color("#3d0b1a")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(90)
            fondo.right(90)
            fondo.forward(35)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-35, 218)
        fondo.color("#9e1329")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(70)
            fondo.right(90)
            fondo.forward(40)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-52, 222)
        fondo.color("#d4af37")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(12)
            fondo.right(90)
            fondo.forward(30)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(40, 222)
        fondo.color("#d4af37")
        fondo.begin_fill()
        for _ in range(2):
            fondo.forward(12)
            fondo.right(90)
            fondo.forward(30)
            fondo.right(90)
        fondo.end_fill()

        fondo.goto(-42, 235)
        fondo.color("gold")
        fondo.dot(14)
        fondo.goto(42, 235)
        fondo.dot(14)
        fondo.goto(0, 238)
        fondo.color("crimson")
        fondo.dot(16)
        fondo.color("gold")
        fondo.dot(8)

    for esq_x, esq_y in [(-340, 240), (340, 240), (-340, -240), (340, -240)]:
        fondo.goto(esq_x, esq_y)
        fondo.color("#000000")
        fondo.dot(28)
        fondo.color("crimson" if modo_actual != "INFERNO" else "orangered")
        fondo.dot(18)
        fondo.color("orange" if modo_actual != "INFERNO" else "yellow")
        fondo.dot(8)


secuaces = []


def calcular_golpes_secuas():
    es_segunda_mitad = pasillo_actual_num > 5

    if pasillo_objetivo == "NORMAL":
        return 2 if es_segunda_mitad else 1
    elif pasillo_objetivo == "DEMON":
        return 3 if es_segunda_mitad else 2
    elif pasillo_objetivo == "INFERNO":
        return 4 if es_segunda_mitad else 3
    return 1


def crear_secuas(x, y):
    s = turtle.Turtle()
    s.speed(0)
    s.shape("square")
    s.color("#ff1100" if modo_actual == "INFERNO" else "#aa00ff")
    s.shapesize(stretch_wid=0.9, stretch_len=0.9)
    s.penup()
    s.goto(x, y)

    s.golpes_restantes = (
        calcular_golpes_secuas() if modo_actual == "PASILLO" else 1
    )
    secuaces.append(s)


def limpiar_secuaces():
    for s in secuaces:
        s.hideturtle()
    secuaces.clear()


def actualizar_secuaces():
    global salud_heroe, tiempo_ultima_frase_secuas
    if estado_juego != "JUGANDO":
        return

    tiempo_actual = time.time()
    if (
        modo_actual == "PASILLO"
        and secuaces
        and tiempo_actual - tiempo_ultima_frase_secuas > 3.0
    ):
        secuas_hablador = random.choice(secuaces)
        dialogo.clear()
        dialogo.goto(secuas_hablador.xcor(), secuas_hablador.ycor() + 25)
        dialogo.color("#ff5555")
        dialogo.write(
            random.choice(frases_secuaces),
            align="center",
            font=("Arial", 9, "bold"),
        )
        tiempo_ultima_frase_secuas = tiempo_actual

    for s in secuaces[:]:
        dx = heroe.xcor() - s.xcor()
        dy = heroe.ycor() - s.ycor()
        ang = math.atan2(dy, dx)

        multiplicador_dificultad = (
            1.3 if (modo_actual == "PASILLO" and pasillo_actual_num > 5) else 1.0
        )
        vel_secuas = (
            (2.4 if modo_actual == "INFERNO" else 1.8)
            * multiplicador_dificultad
        )

        s.setx(s.xcor() + math.cos(ang) * vel_secuas)
        s.sety(s.ycor() + math.sin(ang) * vel_secuas)

        dist_heroe = math.hypot(
            s.xcor() - heroe.xcor(), s.ycor() - heroe.ycor()
        )
        if dist_heroe < 28:
            dano_base = 250 if modo_actual == "PASILLO" else 180
            if modo_actual == "PASILLO" and pasillo_actual_num > 5:
                dano_base = int(dano_base * 1.5)

            salud_heroe -= dano_base

            s.hideturtle()
            if s in secuaces:
                secuaces.remove(s)
            continue

        dist_a_heroe = math.hypot(
            s.xcor() - heroe.xcor(), s.ycor() - heroe.ycor()
        )
        dist_a_espada = math.hypot(
            s.xcor() - espada.xcor(), s.ycor() - espada.ycor()
        )

        if (atacando and dist_a_heroe < 85) or (
            espada.isvisible() and dist_a_espada < 55
        ):
            s.setx(s.xcor() - math.cos(ang) * 60)
            s.sety(s.ycor() - math.sin(ang) * 60)

            s.golpes_restantes -= 1

            if s.golpes_restantes <= 0:
                s.hideturtle()
                if s in secuaces:
                    secuaces.remove(s)


muro_fuego = turtle.Turtle()
muro_fuego.speed(0)
muro_fuego.penup()
muro_fuego.hideturtle()


def dibujar_muro_fuego_completo():
    global frame_alarma, frame_fuego
    frame_fuego += 1

    if frame_fuego % 4 != 0 and modo_actual != "DEMON":
        return

    muro_fuego.clear()

    if modo_actual == "PASILLO":
        for y in range(-250, 260, 35):
            muro_fuego.goto(-245, y)
            muro_fuego.color("#4a0e17")
            muro_fuego.dot(18)

            muro_fuego.goto(245, y)
            muro_fuego.color("#4a0e17")
            muro_fuego.dot(18)
        return

    if modo_actual == "DEMON":
        frame_alarma += 1
        es_rojo_intenso = (frame_alarma // 5) % 2 == 0
        colores_fuego = (
            ["#ff0000", "#990000", "#ff3333", "#ff0055"]
            if es_rojo_intenso
            else ["#660000", "#330000", "#990000", "#ff0000"]
        )
        ventana.bgcolor("#240204" if es_rojo_intenso else "#0a0510")
    elif modo_actual == "INFERNO":
        colores_fuego = ["#ff1100", "#ff5500", "#ffaa00", "#660000"]
        ventana.bgcolor("#1a0002")
    else:
        colores_fuego = ["#ff2200", "#ff6600", "#ffcc00", "#d40000", "#ff8800"]
        ventana.bgcolor("#0d0514")

    for x in range(-360, 370, 35):
        muro_fuego.goto(x, 260)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 26))

        muro_fuego.goto(x, -260)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 26))

    for y in range(-250, 260, 35):
        muro_fuego.goto(-360, y)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 26))

        muro_fuego.goto(360, y)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 26))


titulo_txt = turtle.Turtle()
titulo_txt.speed(0)
titulo_txt.penup()
titulo_txt.hideturtle()


class PersonajeTopDown:

    def __init__(self, es_heroe=True):
        self.es_heroe = es_heroe

        self.base = turtle.Turtle()
        self.base.speed(0)
        self.base.penup()

        self.cuerpo = turtle.Turtle()
        self.cuerpo.speed(0)
        self.cuerpo.penup()

        self.cabeza = turtle.Turtle()
        self.cabeza.speed(0)
        self.cabeza.penup()

        self.cuerno_izq = turtle.Turtle()
        self.cuerno_izq.speed(0)
        self.cuerno_izq.penup()

        self.cuerno_der = turtle.Turtle()
        self.cuerno_der.speed(0)
        self.cuerno_der.penup()

        if es_heroe:
            self.base.shape("triangle")
            self.base.shapesize(stretch_wid=1.8, stretch_len=2.2)
            self.orientacion_capa = 180

            self.cuerpo.shape("circle")
            self.cuerpo.shapesize(stretch_wid=1.5, stretch_len=1.5)

            self.cabeza.shape("circle")
            self.cabeza.shapesize(stretch_wid=0.8, stretch_len=0.8)

            self.aplicar_skin(skins_heroe[skin_actual_idx])
        else:
            self.base.shape("circle")
            self.base.color("#3d000c")
            self.base.shapesize(stretch_wid=4.5, stretch_len=4.5)

            self.cuerpo.shape("square")
            self.cuerpo.color("crimson")
            self.cuerpo.shapesize(stretch_wid=3.2, stretch_len=3.2)

            self.cabeza.shape("triangle")
            self.cabeza.color("gold")
            self.cabeza.shapesize(stretch_wid=1.6, stretch_len=2.0)

            self.cuerno_izq.shape("triangle")
            self.cuerno_izq.color("black")
            self.cuerno_izq.shapesize(stretch_wid=0.8, stretch_len=2.5)
            self.cuerno_izq.setheading(135)

            self.cuerno_der.shape("triangle")
            self.cuerno_der.color("black")
            self.cuerno_der.shapesize(stretch_wid=0.8, stretch_len=2.5)
            self.cuerno_der.setheading(45)

        self.ocultar()

    def aplicar_skin(self, skin):
        if self.es_heroe:
            self.base.color(skin["capa"])
            self.cuerpo.color(skin["cuerpo"])
            self.cabeza.color(skin["cabeza"])

    def ir_a(self, x, y, angulo_capa=None):
        limite_x = 220 if modo_actual == "PASILLO" else 340
        x = max(-limite_x, min(limite_x, x))
        y = max(-220, min(220, y))

        self.cuerpo.goto(x, y)

        if self.es_heroe:
            if angulo_capa is not None:
                self.orientacion_capa = angulo_capa

            rad = math.radians(self.orientacion_capa)
            offset_x = math.cos(rad) * 15
            offset_y = math.sin(rad) * 15

            self.base.goto(x + offset_x, y + offset_y)
            self.base.setheading(self.orientacion_capa)
            self.cabeza.goto(x, y)
        else:
            self.base.goto(x, y)
            self.cabeza.goto(x, y + 10)
            self.cuerno_izq.goto(x - 25, y + 25)
            self.cuerno_der.goto(x + 25, y + 25)

    def cambiar_color(
        self, color_base, color_cuerpo, color_cabeza, color_cuernos
    ):
        if not self.es_heroe:
            self.base.color(color_base)
            self.cuerpo.color(color_cuerpo)
            self.cabeza.color(color_cabeza)
            self.cuerno_izq.color(color_cuernos)
            self.cuerno_der.color(color_cuernos)

    def restaurar_colores_demonio(self):
        if not self.es_heroe:
            self.base.color("#3d000c")
            self.cuerpo.color("crimson")
            self.cabeza.color("gold")
            self.cuerno_izq.color("black")
            self.cuerno_der.color("black")

    def mostrar(self):
        self.base.showturtle()
        self.cuerpo.showturtle()
        self.cabeza.showturtle()
        if not self.es_heroe:
            self.cuerno_izq.showturtle()
            self.cuerno_der.showturtle()

    def ocultar(self):
        self.base.hideturtle()
        self.cuerpo.hideturtle()
        self.cabeza.hideturtle()
        if not self.es_heroe:
            self.cuerno_izq.hideturtle()
            self.cuerno_der.hideturtle()

    def xcor(self):
        return self.cuerpo.xcor()

    def ycor(self):
        return self.cuerpo.ycor()


heroe = PersonajeTopDown(es_heroe=True)
demonio = PersonajeTopDown(es_heroe=False)

espada = turtle.Turtle()
espada.speed(0)
espada.shape("triangle")
espada.color("cyan")
espada.shapesize(stretch_wid=1.8, stretch_len=5.0)
espada.penup()
espada.hideturtle()
atacando = False

hud = turtle.Turtle()
hud.speed(0)
hud.penup()
hud.hideturtle()

cuadro_ui = turtle.Turtle()
cuadro_ui.speed(0)
cuadro_ui.penup()
cuadro_ui.hideturtle()

dialogo = turtle.Turtle()
dialogo.speed(0)
dialogo.color("yellow")
dialogo.penup()
dialogo.hideturtle()

botiquin_gfx = turtle.Turtle()
botiquin_gfx.speed(0)
botiquin_gfx.penup()
botiquin_gfx.hideturtle()

proyectiles = []


def cambiar_skin_heroe():
    global skin_actual_idx
    skin_actual_idx = (skin_actual_idx + 1) % len(skins_heroe)
    heroe.aplicar_skin(skins_heroe[skin_actual_idx])


def crear_proyectil(
    x, y, dx, dy, color, tamano, tiempo_congelar=0, color_fuego=None
):
    p = turtle.Turtle()
    p.speed(0)
    p.shape("circle")
    p.color(color)
    p.shapesize(stretch_wid=tamano, stretch_len=tamano)
    p.penup()
    p.goto(x, y)
    p.dx = dx
    p.dy = dy
    p.tamano = tamano
    p.tiempo_congelar = tiempo_congelar
    p.tiempo_creacion = time.time()
    p.color_fuego = color_fuego
    proyectiles.append(p)


def limpiar_proyectiles():
    for p in proyectiles:
        p.hideturtle()
    proyectiles.clear()


def dibujar_cuadros_ui():
    cuadro_ui.clear()
    hud.clear()

    cuadro_ui.goto(-370, 280)
    cuadro_ui.color("#110a1c" if modo_actual == "NORMAL" else "#2b050b")
    cuadro_ui.begin_fill()
    for _ in range(2):
        cuadro_ui.forward(740)
        cuadro_ui.right(90)
        cuadro_ui.forward(52)
        cuadro_ui.right(90)
    cuadro_ui.end_fill()

    cuadro_ui.pensize(3)
    cuadro_ui.color(
        "#ff1100"
        if modo_actual == "INFERNO"
        else ("#ff1a40" if modo_actual == "DEMON" else "#d4af37")
    )
    cuadro_ui.goto(-370, 280)
    cuadro_ui.pendown()
    for _ in range(2):
        cuadro_ui.forward(740)
        cuadro_ui.right(90)
        cuadro_ui.forward(52)
        cuadro_ui.right(90)
    cuadro_ui.penup()

    pct_heroe = max(0.0, salud_heroe / max_salud_heroe_actual)
    cuadro_ui.goto(-350, 243)
    cuadro_ui.color("#333333")
    cuadro_ui.begin_fill()
    for _ in range(2):
        cuadro_ui.forward(220)
        cuadro_ui.right(90)
        cuadro_ui.forward(10)
        cuadro_ui.right(90)
    cuadro_ui.end_fill()

    cuadro_ui.goto(-350, 243)
    cuadro_ui.color("#00e676" if pct_heroe > 0.3 else "#ff1744")
    cuadro_ui.begin_fill()
    for _ in range(2):
        cuadro_ui.forward(220 * pct_heroe)
        cuadro_ui.right(90)
        cuadro_ui.forward(10)
        cuadro_ui.right(90)
    cuadro_ui.end_fill()

    hud.goto(-240, 255)
    hud.color("white")
    hud.write(
        f"Héroe: {int(salud_heroe)} / {int(max_salud_heroe_actual)} HP",
        align="center",
        font=("Consolas", 10, "bold"),
    )

    if modo_actual == "PASILLO":
        tiempo_restante_pasillo = max(
            0.0, DURACION_PASILLO - (time.time() - tiempo_inicio_pasillo)
        )
        mins = int(tiempo_restante_pasillo // 60)
        secs = int(tiempo_restante_pasillo % 60)
        hud.goto(150 if MODO_MOBILE else 240, 255)
        hud.color("gold")
        hud.write(
            f"PASILLO {pasillo_actual_num}/{TOTAL_PASILLOS} ({pasillo_objetivo}): {mins:02d}:{secs:02d}",
            align="center",
            font=("Consolas", 10 if MODO_MOBILE else 11, "bold"),
        )
    else:
        pct_demonio = max(0.0, salud_demonio / max_salud_demonio_actual)
        cuadro_ui.goto(130, 243)
        cuadro_ui.color("#333333")
        cuadro_ui.begin_fill()
        for _ in range(2):
            cuadro_ui.forward(220)
            cuadro_ui.right(90)
            cuadro_ui.forward(10)
            cuadro_ui.right(90)
        cuadro_ui.end_fill()

        cuadro_ui.goto(130, 243)
        cuadro_ui.color("#ff0055" if modo_actual != "INFERNO" else "#ff3300")
        cuadro_ui.begin_fill()
        for _ in range(2):
            cuadro_ui.forward(220 * pct_demonio)
            cuadro_ui.right(90)
            cuadro_ui.forward(10)
            cuadro_ui.right(90)
        cuadro_ui.end_fill()

        etiqueta_boss = (
            "REY DEMONIO [INFERNO]"
            if modo_actual == "INFERNO"
            else (
                "REY DEMONIO [DEMON]"
                if modo_actual == "DEMON"
                else "REY DEMONIO"
            )
        )
        hud.goto(240, 255)
        hud.color("white")
        hud.write(
            f"{etiqueta_boss}: {int(salud_demonio)} / {int(max_salud_demonio_actual)} HP",
            align="center",
            font=("Consolas", 10, "bold"),
        )

    if not MODO_MOBILE:
        cuadro_ui.goto(-370, -235)
        cuadro_ui.color("#0e0817" if modo_actual == "NORMAL" else "#240307")
        cuadro_ui.begin_fill()
        for _ in range(2):
            cuadro_ui.forward(740)
            cuadro_ui.right(90)
            cuadro_ui.forward(30)
            cuadro_ui.right(90)
        cuadro_ui.end_fill()

        cuadro_ui.pensize(2)
        cuadro_ui.color("#8a2be2" if modo_actual == "NORMAL" else "#ff3300")
        cuadro_ui.goto(-370, -235)
        cuadro_ui.pendown()
        for _ in range(2):
            cuadro_ui.forward(740)
            cuadro_ui.right(90)
            cuadro_ui.forward(30)
            cuadro_ui.right(90)
        cuadro_ui.penup()

        hud.goto(0, -258)
        hud.color("#00ffff" if modo_actual == "NORMAL" else "#ffea00")
        hud.write(
            "CONTROLES: [WASD]: Mover | [ESPACIO]: Atacar | [P]: Pieles | [Z]: Pausa | [X]: Menú | [F11]: Pantalla Completa",
            align="center",
            font=("Courier", 8, "bold"),
        )


def actualizar_botiquin(tiempo_actual):
    global botiquin_activo, botiquin_pos, tiempo_spawn_botiquin, tiempo_expiracion_botiquin, salud_heroe

    if modo_actual not in ["DEMON", "INFERNO"] or estado_juego != "JUGANDO":
        botiquin_gfx.clear()
        botiquin_activo = False
        return

    if not botiquin_activo:
        if tiempo_actual >= tiempo_spawn_botiquin:
            botiquin_activo = True
            botiquin_pos = (
                random.randint(-280, 280),
                random.randint(-180, 180),
            )
            tiempo_expiracion_botiquin = tiempo_actual + DURACION_BOTIQUIN
    else:
        tiempo_restante = tiempo_expiracion_botiquin - tiempo_actual

        if tiempo_restante <= 0:
            botiquin_activo = False
            botiquin_gfx.clear()
            tiempo_spawn_botiquin = tiempo_actual + random.uniform(8, 14)
            return

        bx, by = botiquin_pos
        botiquin_gfx.clear()

        botiquin_gfx.goto(bx - 15, by + 15)
        botiquin_gfx.color("#00e676")
        botiquin_gfx.begin_fill()
        for _ in range(4):
            botiquin_gfx.forward(30)
            botiquin_gfx.right(90)
        botiquin_gfx.end_fill()

        botiquin_gfx.goto(bx - 4, by + 10)
        botiquin_gfx.color("white")
        botiquin_gfx.begin_fill()
        for _ in range(4):
            botiquin_gfx.forward(8)
            botiquin_gfx.right(90)
        botiquin_gfx.end_fill()

        botiquin_gfx.goto(bx - 10, by + 4)
        botiquin_gfx.begin_fill()
        for _ in range(4):
            botiquin_gfx.forward(20)
            botiquin_gfx.right(90)
        botiquin_gfx.end_fill()

        botiquin_gfx.goto(bx, by + 20)
        botiquin_gfx.color("yellow")
        botiquin_gfx.write(
            f"¡BOTIQUÍN! {tiempo_restante:.1f}s",
            align="center",
            font=("Arial", 9, "bold"),
        )

        dist_botiquin = math.hypot(heroe.xcor() - bx, heroe.ycor() - by)
        if dist_botiquin < 35:
            salud_heroe = min(
                max_salud_heroe_actual, salud_heroe + CURACION_BOTIQUIN
            )
            botiquin_activo = False
            botiquin_gfx.clear()

            dialogo.clear()
            dialogo.goto(heroe.xcor(), heroe.ycor() + 40)
            dialogo.color("#00ffcc")
            dialogo.write(
                f"+{CURACION_BOTIQUIN} HP!",
                align="center",
                font=("Impact", 14, "bold"),
            )

            tiempo_spawn_botiquin = tiempo_actual + random.uniform(10, 16)


def mostrar_menu(modo_moderador_activado=False):
    if MODO_MOBILE:
        ventana.bgcolor("#080510")
        muro_fuego.clear()
        hud.clear()
        cuadro_ui.clear()
        dialogo.clear()
        titulo_txt.clear()
        botiquin_gfx.clear()
        limpiar_secuaces()
        heroe.ocultar()
        demonio.ocultar()
        espada.hideturtle()
        dibujar_controles_mobile()
        return

    ventana.bgcolor("#0a0510")
    muro_fuego.clear()
    hud.clear()
    cuadro_ui.clear()
    dialogo.clear()
    titulo_txt.clear()
    botiquin_gfx.clear()
    limpiar_secuaces()

    heroe.ocultar()
    demonio.ocultar()
    espada.hideturtle()

    cuadro_ui.goto(-360, 250)
    cuadro_ui.color("#2d0c3e")
    cuadro_ui.begin_fill()
    for _ in range(2):
        cuadro_ui.forward(720)
        cuadro_ui.right(90)
        cuadro_ui.forward(500)
        cuadro_ui.right(90)
    cuadro_ui.end_fill()

    cuadro_ui.goto(-350, 240)
    cuadro_ui.color("#12061c")
    cuadro_ui.begin_fill()
    for _ in range(2):
        cuadro_ui.forward(700)
        cuadro_ui.right(90)
        cuadro_ui.forward(480)
        cuadro_ui.right(90)
    cuadro_ui.end_fill()

    cuadro_ui.pensize(3)
    cuadro_ui.color("gold")
    cuadro_ui.goto(-350, 240)
    cuadro_ui.pendown()
    for _ in range(2):
        cuadro_ui.forward(700)
        cuadro_ui.right(90)
        cuadro_ui.forward(480)
        cuadro_ui.right(90)
    cuadro_ui.penup()

    titulo_txt.goto(0, 185)
    titulo_txt.color("gold")
    titulo_txt.write(
        "❖ CHRONICLES OF THE FALLEN KING ❖",
        align="center",
        font=("Impact", 22, "bold"),
    )

    if modo_moderador_activado:
        titulo_txt.goto(0, 155)
        titulo_txt.color("#00ffcc")
        titulo_txt.write(
            "⚡ MODO ADMIN ACTIVADO CON LA TECLA A ⚡",
            align="center",
            font=("Courier", 10, "bold"),
        )
    else:
        titulo_txt.goto(0, 155)
        titulo_txt.color("#ff3300")
        titulo_txt.write(
            "― SURVIVE 10 PASILLOS (30 SEG C/U) PARA CADA JEFE ―",
            align="center",
            font=("Courier", 11, "bold"),
        )

    titulo_txt.goto(0, 105)
    titulo_txt.color("#00ffff")
    titulo_txt.write(
        "🛡 [ V ]: PASILLOS MODO NORMAL (DISPONIBLE) 🛡",
        align="center",
        font=("Arial", 10, "bold"),
    )

    if boss_normal_desbloqueado:
        titulo_txt.goto(0, 65)
        titulo_txt.color("#00ffcc")
        titulo_txt.write(
            "⚔️ [ ENTER ]: JEFE REY DEMONIO NORMAL (DESBLOQUEADO) ⚔️",
            align="center",
            font=("Arial", 10, "bold"),
        )
    else:
        prog = pasillo_actual_num - 1 if pasillo_objetivo == "NORMAL" else 0
        titulo_txt.goto(0, 65)
        titulo_txt.color("#666666")
        titulo_txt.write(
            f"🔒 JEFE NORMAL: BLOQUEADO (Supera 10 Pasillos Normales - Progreso: {prog}/10)",
            align="center",
            font=("Arial", 9, "italic"),
        )

    if demon_mode_desbloqueado:
        titulo_txt.goto(0, 20)
        titulo_txt.color("#ffaa00")
        titulo_txt.write(
            "👿 [ B ]: PASILLOS DEMON (DESBLOQUEADOS) 👿",
            align="center",
            font=("Arial", 10, "bold"),
        )
        if boss_demon_desbloqueado:
            titulo_txt.goto(0, -5)
            titulo_txt.color("#ffea00")
            titulo_txt.write(
                "⚔️ [ W ]: JEFE REY DEMONIO DEMON (DESBLOQUEADO) ⚔️",
                align="center",
                font=("Arial", 10, "bold"),
            )
        else:
            prog = pasillo_actual_num - 1 if pasillo_objetivo == "DEMON" else 0
            titulo_txt.goto(0, -5)
            titulo_txt.color("#775522")
            titulo_txt.write(
                f"🔒 JEFE DEMON: BLOQUEADO (Supera 10 Pasillos Demon - Progreso: {prog}/10)",
                align="center",
                font=("Arial", 9, "italic"),
            )
    else:
        titulo_txt.goto(0, 10)
        titulo_txt.color("#443322")
        titulo_txt.write(
            "🔒 MODO DEMON COMPLETO: Derrota al Jefe Rey Demonio Normal para desbloquear",
            align="center",
            font=("Arial", 9, "italic"),
        )

    if inferno_mode_desbloqueado:
        titulo_txt.goto(0, -50)
        titulo_txt.color("#ff3300")
        titulo_txt.write(
            "🔥 [ M ]: PASILLOS INFERNO (DESBLOQUEADOS) 🔥",
            align="center",
            font=("Arial", 10, "bold"),
        )
        if boss_inferno_desbloqueado:
            titulo_txt.goto(0, -75)
            titulo_txt.color("#ff0000")
            titulo_txt.write(
                "⚔ [ N ]: JEFE REY DEMONIO INFERNO (DESBLOQUEADO) ⚔️",
                align="center",
                font=("Arial", 10, "bold"),
            )
        else:
            prog = (
                pasillo_actual_num - 1 if pasillo_objetivo == "INFERNO" else 0
            )
            titulo_txt.goto(0, -75)
            titulo_txt.color("#772222")
            titulo_txt.write(
                f"🔒 JEFE INFERNO: BLOQUEADO (Supera 10 Pasillos Inferno - Progreso: {prog}/10)",
                align="center",
                font=("Arial", 9, "italic"),
            )
    else:
        titulo_txt.goto(0, -60)
        titulo_txt.color("#442222")
        titulo_txt.write(
            "🔒 MODO INFERNO COMPLETO: Derrota al Jefe Rey Demonio Demon para desbloquear",
            align="center",
            font=("Arial", 9, "italic"),
        )

    titulo_txt.goto(0, -115)
    titulo_txt.color("white")
    titulo_txt.write(
        "═════════════════ CONTROLES DEL JUEGO ═════════════════",
        align="center",
        font=("Courier", 10, "bold"),
    )

    titulo_txt.goto(0, -170)
    titulo_txt.color("lightgray")
    titulo_txt.write(
        " [FLECHAS / WASD] Mover | [ESPACIO] Atacar Dirigido | [P] Cambiar Piel/Skin\n"
        " [Z] Pausar Juego | [X] Salir al Menú | [F11 / F] Pantalla Completa | [A] Modo Admin (Desbloquear Todo)",
        align="center",
        font=("Consolas", 9, "normal"),
    )


def iniciar_modo_juego(modo):
    global estado_juego, salud_heroe, salud_demonio, modo_actual
    global max_salud_heroe_actual, max_salud_demonio_actual
    global botiquin_activo, tiempo_spawn_botiquin, tiempo_inicio_pasillo

    modo_actual = modo
    estado_juego = "JUGANDO"

    titulo_txt.clear()
    hud.clear()
    dialogo.clear()
    limpiar_secuaces()
    limpiar_proyectiles()

    if modo_actual == "PASILLO":
        max_salud_heroe_actual = MAX_SALUD_HEROE_PASILLO
        max_salud_demonio_actual = 1
        tiempo_inicio_pasillo = time.time()
    elif modo_actual == "INFERNO":
        max_salud_heroe_actual = MAX_SALUD_HEROE_INFERNO
        max_salud_demonio_actual = MAX_SALUD_DEMONIO_INFERNO
    elif modo_actual == "DEMON":
        max_salud_heroe_actual = MAX_SALUD_HEROE_DEMON
        max_salud_demonio_actual = MAX_SALUD_DEMONIO_DEMON
    else:
        max_salud_heroe_actual = MAX_SALUD_HEROE_NORMAL
        max_salud_demonio_actual = MAX_SALUD_DEMONIO_NORMAL

    salud_heroe = max_salud_heroe_actual
    salud_demonio = max_salud_demonio_actual

    botiquin_activo = False
    tiempo_spawn_botiquin = time.time() + random.uniform(6, 10)

    dibujar_escenario_topdown()
    demonio.restaurar_colores_demonio()

    if modo_actual == "PASILLO":
        heroe.ir_a(0, -200, angulo_capa=90)
        heroe.mostrar()
        demonio.ocultar()
    else:
        heroe.ir_a(-220, 0, angulo_capa=180)
        heroe.mostrar()
        demonio.ir_a(220, 0)
        demonio.mostrar()


def presionar_tecla(k):
    if k in teclas:
        teclas[k] = True
    verificar_modo_moderador()


def soltar_tecla(k):
    if k in teclas:
        teclas[k] = False


def realizar_ataque():
    global atacando
    if estado_juego == "JUGANDO" and not atacando:
        atacando = True


def alternar_pausa():
    global estado_juego
    if estado_juego == "JUGANDO":
        estado_juego = "PAUSA"
    elif estado_juego == "PAUSA":
        estado_juego = "JUGANDO"


def salir_al_titulo():
    global estado_juego, botiquin_activo
    if estado_juego in ["JUGANDO", "PAUSA", "FIN_PASILLO_VICTORIA"]:
        limpiar_proyectiles()
        botiquin_activo = False
        botiquin_gfx.clear()
        estado_juego = "INICIO"
        mostrar_menu()


def procesar_enter():
    global estado_juego
    if estado_juego == "INICIO" and boss_normal_desbloqueado:
        iniciar_modo_juego("NORMAL")
    elif estado_juego in ["FIN_VICTORIA", "FIN_DERROTA", "FIN_PASILLO_VICTORIA"]:
        limpiar_proyectiles()
        estado_juego = "INICIO"
        mostrar_menu()


def procesar_w():
    global estado_juego
    if estado_juego == "INICIO" and boss_demon_desbloqueado:
        iniciar_modo_juego("DEMON")


def procesar_n():
    global estado_juego
    if estado_juego == "INICIO" and boss_inferno_desbloqueado:
        iniciar_modo_juego("INFERNO")


def iniciar_pasillos(objetivo):
    global pasillo_objetivo, pasillo_actual_num
    pasillo_objetivo = objetivo
    pasillo_actual_num = 1
    iniciar_modo_juego("PASILLO")


def procesar_v():
    if estado_juego == "INICIO":
        iniciar_pasillos("NORMAL")


def procesar_b():
    if estado_juego == "INICIO" and demon_mode_desbloqueado:
        iniciar_pasillos("DEMON")


def procesar_m():
    if estado_juego == "INICIO" and inferno_mode_desbloqueado:
        iniciar_pasillos("INFERNO")


ventana.listen()

for t in ["Up", "Down", "Left", "Right", "w", "s", "a", "d", "m"]:
    ventana.onkeypress(lambda k=t: presionar_tecla(k), t)
    ventana.onkeyrelease(lambda k=t: soltar_tecla(k), t)

ventana.onkeypress(lambda: presionar_tecla("a"), "a")
ventana.onkeypress(lambda: presionar_tecla("a"), "A")
ventana.onkeyrelease(lambda: soltar_tecla("a"), "a")
ventana.onkeyrelease(lambda: soltar_tecla("a"), "A")

ventana.onkeypress(lambda: presionar_tecla("m"), "M")
ventana.onkeyrelease(lambda: soltar_tecla("m"), "M")

ventana.onkeypress(realizar_ataque, "space")
ventana.onkeypress(cambiar_skin_heroe, "p")
ventana.onkeypress(cambiar_skin_heroe, "P")
ventana.onkeypress(alternar_pausa, "z")
ventana.onkeypress(alternar_pausa, "Z")
ventana.onkeypress(salir_al_titulo, "x")
ventana.onkeypress(salir_al_titulo, "X")
ventana.onkeypress(procesar_enter, "Return")
ventana.onkeypress(procesar_w, "w")
ventana.onkeypress(procesar_w, "W")
ventana.onkeypress(procesar_n, "n")
ventana.onkeypress(procesar_n, "N")
ventana.onkeypress(procesar_v, "v")
ventana.onkeypress(procesar_v, "V")
ventana.onkeypress(procesar_b, "b")
ventana.onkeypress(procesar_b, "B")
ventana.onkeypress(procesar_m, "m")
ventana.onkeypress(procesar_m, "M")
ventana.onkeypress(alternar_pantalla_completa, "F11")
ventana.onkeypress(alternar_pantalla_completa, "f")

mostrar_menu()
instalar_controles_pydroid()
dibujar_controles_mobile()


def actualizar_movimiento_heroe():
    if estado_juego != "JUGANDO":
        return

    dx, dy = 0, 0
    ang = None

    # Flechas táctiles de Pydroid 3
    if mobile_flechas["up"]:
        dy += 12
        ang = 270
    if mobile_flechas["down"]:
        dy -= 12
        ang = 90
    if mobile_flechas["left"]:
        dx -= 12
        ang = 180
    if mobile_flechas["right"]:
        dx += 12
        ang = 0

    if teclas["Up"] or teclas["w"]:
        dy += 16
        ang = 270
    if teclas["Down"] or teclas["s"]:
        dy -= 16
        ang = 90
    if teclas["Left"] or teclas["a"]:
        dx -= 16
        ang = 0
    if teclas["Right"] or teclas["d"]:
        dx += 16
        ang = 180

    if dx != 0 or dy != 0:
        heroe.ir_a(heroe.xcor() + dx, heroe.ycor() + dy, angulo_capa=ang)


def bucle_principal():
    global estado_juego, salud_demonio, salud_heroe, demon_mode_desbloqueado, inferno_mode_desbloqueado
    global tiempo_ultima_frase, tiempo_ultimo_ataque_demonio, tiempo_ultimo_ataque_t, tiempo_ultimo_secuas
    global atacando, frame_brillo, tiempo_inicio_animacion
    global pasillo_actual_num, boss_normal_desbloqueado, boss_demon_desbloqueado, boss_inferno_desbloqueado

    if estado_juego == "PAUSA":
        hud.clear()
        if not MODO_MOBILE:
            hud.goto(0, 30)
            hud.color("yellow")
            hud.write(
                "=== JUEGO EN PAUSA ===",
                align="center",
                font=("Impact", 22, "bold"),
            )
            hud.goto(0, -20)
            hud.color("white")
            hud.write(
                "[ Z: Reanudar | X: Salir al Título ]",
                align="center",
                font=("Arial", 11, "bold"),
            )

    elif estado_juego == "JUGANDO":
        tiempo_actual = time.time()

        actualizar_movimiento_heroe()
        dibujar_muro_fuego_completo()
        dibujar_cuadros_ui()
        dibujar_controles_mobile()

        if modo_actual == "PASILLO":
            tiempo_transcurrido = tiempo_actual - tiempo_inicio_pasillo

            if tiempo_actual - tiempo_ultimo_secuas > 0.8:
                spawn_x = random.randint(-180, 180)
                crear_secuas(spawn_x, 230)
                tiempo_ultimo_secuas = tiempo_actual

            actualizar_secuaces()

            objetivo_x, objetivo_y = heroe.xcor(), heroe.ycor() + 100
            min_dist = 999999

            for s in secuaces:
                dist = math.hypot(
                    s.xcor() - heroe.xcor(), s.ycor() - heroe.ycor()
                )
                if dist < min_dist:
                    min_dist = dist
                    objetivo_x, objetivo_y = s.xcor(), s.ycor()

            ang_ataque = math.degrees(
                math.atan2(
                    objetivo_y - heroe.ycor(), objetivo_x - heroe.xcor()
                )
            )
            espada.setheading(ang_ataque)

            if atacando:
                espada.showturtle()
                espada.setx(
                    heroe.xcor() + math.cos(math.radians(ang_ataque)) * 45
                )
                espada.sety(
                    heroe.ycor() + math.sin(math.radians(ang_ataque)) * 45
                )
                atacando = False
            else:
                espada.hideturtle()
                espada.goto(heroe.xcor(), heroe.ycor())

            if tiempo_transcurrido >= DURACION_PASILLO:
                limpiar_secuaces()
                limpiar_proyectiles()
                if pasillo_actual_num < TOTAL_PASILLOS:
                    pasillo_actual_num += 1
                    iniciar_modo_juego("PASILLO")
                else:
                    if pasillo_objetivo == "NORMAL":
                        boss_normal_desbloqueado = True
                    elif pasillo_objetivo == "DEMON":
                        boss_demon_desbloqueado = True
                    elif pasillo_objetivo == "INFERNO":
                        boss_inferno_desbloqueado = True

                    estado_juego = "FIN_PASILLO_VICTORIA"

            if salud_heroe <= 0:
                salud_heroe = 0
                estado_juego = "FIN_DERROTA"
                limpiar_secuaces()

        else:
            actualizar_botiquin(tiempo_actual)
            actualizar_secuaces()

            if tiempo_actual - tiempo_ultima_frase > 4.5:
                dialogo.clear()
                dialogo.goto(demonio.xcor(), demonio.ycor() + 55)
                dialogo.color(
                    "orangered"
                    if modo_actual == "INFERNO"
                    else ("crimson" if modo_actual == "DEMON" else "yellow")
                )

                if modo_actual == "INFERNO":
                    frase = random.choice(frases_demonio_inferno)
                elif modo_actual == "DEMON":
                    frase = random.choice(frases_demonio_demon)
                else:
                    frase = random.choice(frases_demonio_normal)

                dialogo.write(
                    frase, align="center", font=("Arial", 11, "italic")
                )
                tiempo_ultima_frase = tiempo_actual

            if (
                modo_actual == "INFERNO"
                and tiempo_actual - tiempo_ultimo_secuas > 3.0
            ):
                crear_secuas(demonio.xcor(), demonio.ycor())
                tiempo_ultimo_secuas = tiempo_actual

            dx_d = heroe.xcor() - demonio.xcor()
            dy_d = heroe.ycor() - demonio.ycor()
            ang_demonio = math.atan2(dy_d, dx_d)

            vel_demonio = (
                0.85
                if modo_actual == "INFERNO"
                else (0.65 if modo_actual == "DEMON" else 0.45)
            )
            nuevo_x_d = demonio.xcor() + math.cos(ang_demonio) * vel_demonio
            nuevo_y_d = demonio.ycor() + math.sin(ang_demonio) * vel_demonio
            demonio.ir_a(nuevo_x_d, nuevo_y_d)

            # DIRECCIÓN DE LA ESPADA HACIA EL DEMONIO
            objetivo_x, objetivo_y = demonio.xcor(), demonio.ycor()
            angulo_hacia_objetivo = math.degrees(
                math.atan2(
                    objetivo_y - heroe.ycor(), objetivo_x - heroe.xcor()
                )
            )
            espada.setheading(angulo_hacia_objetivo)

            if atacando:
                espada.showturtle()
                espada.setx(
                    heroe.xcor()
                    + math.cos(math.radians(angulo_hacia_objetivo)) * 55
                )
                espada.sety(
                    heroe.ycor()
                    + math.sin(math.radians(angulo_hacia_objetivo)) * 55
                )

                dist_espada_demonio = math.hypot(
                    espada.xcor() - demonio.xcor(),
                    espada.ycor() - demonio.ycor(),
                )
                if dist_espada_demonio < 85:
                    salud_demonio -= DANO_HEROE
                    if modo_actual == "INFERNO":
                        crear_secuas(demonio.xcor(), demonio.ycor())

                atacando = False
            else:
                espada.hideturtle()
                espada.goto(heroe.xcor(), heroe.ycor())

            # ATAQUES DEL REY DEMONIO
            cooldown_ataque = (
                1.2
                if modo_actual == "INFERNO"
                else (1.6 if modo_actual == "DEMON" else 2.0)
            )
            if tiempo_actual - tiempo_ultimo_ataque_demonio > cooldown_ataque:
                tipo = random.choice(["corto", "largo"])
                vel = (
                    9.5
                    if modo_actual == "INFERNO"
                    else (8.8 if modo_actual == "DEMON" else 7.5)
                )
                tam = 2.2 if tipo == "largo" else 1.0

                crear_proyectil(
                    demonio.xcor(),
                    demonio.ycor(),
                    math.cos(ang_demonio) * vel,
                    math.sin(ang_demonio) * vel,
                    "red",
                    tam,
                )
                tiempo_ultimo_ataque_demonio = tiempo_actual

            cooldown_triple = (
                3.5
                if modo_actual == "INFERNO"
                else (4.0 if modo_actual == "DEMON" else 6.0)
            )
            if tiempo_actual - tiempo_ultimo_ataque_t > cooldown_triple:
                crear_proyectil(
                    demonio.xcor(),
                    demonio.ycor(),
                    math.cos(ang_demonio) * 5.0,
                    math.sin(ang_demonio) * 5.0,
                    "gold",
                    1.8,
                    tiempo_congelar=2.5,
                    color_fuego="orangered",
                )
                rad_izq = ang_demonio + math.pi / 3
                crear_proyectil(
                    demonio.xcor(),
                    demonio.ycor(),
                    math.cos(rad_izq) * 4.5,
                    math.sin(rad_izq) * 4.5,
                    "gold",
                    1.5,
                    tiempo_congelar=2.5,
                    color_fuego="orangered",
                )
                rad_der = ang_demonio - math.pi / 3
                crear_proyectil(
                    demonio.xcor(),
                    demonio.ycor(),
                    math.cos(rad_der) * 4.5,
                    math.sin(rad_der) * 4.5,
                    "gold",
                    1.5,
                    tiempo_congelar=2.5,
                    color_fuego="orangered",
                )
                tiempo_ultimo_ataque_t = tiempo_actual

            # MOVIMIENTO Y DAÑO ESCALADO DE PROYECTILES
            for p in proyectiles[:]:
                if time.time() - p.tiempo_creacion < p.tiempo_congelar:
                    p.color("gold")
                    continue
                else:
                    if p.color_fuego:
                        p.color(p.color_fuego)

                p.setx(p.xcor() + p.dx)
                p.sety(p.ycor() + p.dy)

                dist_p = math.hypot(
                    p.xcor() - heroe.xcor(), p.ycor() - heroe.ycor()
                )
                radio_impacto = 25 * p.tamano

                if dist_p < radio_impacto:
                    dano_base = obtener_dano_proyectil_jefe()
                    dano_total = int(dano_base * p.tamano)
                    salud_heroe -= dano_total

                    ang_impacto = math.atan2(
                        heroe.ycor() - p.ycor(), heroe.xcor() - p.xcor()
                    )
                    heroe.ir_a(
                        heroe.xcor() + math.cos(ang_impacto) * 25,
                        heroe.ycor() + math.sin(ang_impacto) * 25,
                    )

                    p.hideturtle()
                    if p in proyectiles:
                        proyectiles.remove(p)
                elif abs(p.xcor()) > 370 or abs(p.ycor()) > 270:
                    p.hideturtle()
                    if p in proyectiles:
                        proyectiles.remove(p)

            # DAÑO ESCALADO POR CONTACTO DIRECTO
            dist_contacto = math.hypot(
                demonio.xcor() - heroe.xcor(), demonio.ycor() - heroe.ycor()
            )
            if dist_contacto < 50:
                salud_heroe -= obtener_dano_contacto_jefe()
                heroe.ir_a(
                    heroe.xcor() + math.cos(ang_demonio) * 15,
                    heroe.ycor() + math.sin(ang_demonio) * 15,
                )

            if salud_demonio <= 0:
                salud_demonio = 0
                estado_juego = "ANIM_VICTORIA"

                if modo_actual == "NORMAL":
                    demon_mode_desbloqueado = True
                elif modo_actual == "DEMON":
                    inferno_mode_desbloqueado = True

                tiempo_inicio_animacion = time.time()
                limpiar_proyectiles()
                limpiar_secuaces()
                botiquin_gfx.clear()

            elif salud_heroe <= 0:
                salud_heroe = 0
                estado_juego = "FIN_DERROTA"
                limpiar_proyectiles()
                limpiar_secuaces()
                botiquin_gfx.clear()

    elif estado_juego == "FIN_PASILLO_VICTORIA":
        if mobile_ui is not None:
            mobile_ui.clear()
        hud.clear()
        cuadro_ui.clear()
        dialogo.clear()

        hud.goto(0, 40)
        hud.color("#00ffff")
        hud.write(
            f"¡HAS COMPLETADO LOS 10 PASILLOS ({pasillo_objetivo})!",
            align="center",
            font=("Impact", 18, "bold"),
        )
        hud.goto(0, -20)
        hud.color("gold")
        hud.write(
            f"¡La batalla contra el Jefe {pasillo_objetivo} ha sido DESBLOQUEADA!",
            align="center",
            font=("Arial", 12, "bold"),
        )
        hud.goto(0, -60)
        hud.color("white")
        hud.write(
            "[ Toca la pantalla o presiona ENTER para volver al Menú e iniciar el combate ]",
            align="center",
            font=("Arial", 10, "bold"),
        )

    elif estado_juego == "ANIM_VICTORIA":
        if mobile_ui is not None:
            mobile_ui.clear()
        hud.clear()
        dialogo.clear()
        dialogo.goto(demonio.xcor(), demonio.ycor() + 55)
        dialogo.color("crimson")
        dialogo.write(
            "¡No... esto no puede ser mi fin...!",
            align="center",
            font=("Arial", 12, "bold"),
        )

        tiempo_transcurridos = time.time() - tiempo_inicio_animacion

        if frame_brillo % 2 == 0:
            demonio.cambiar_color("white", "gold", "yellow", "white")
        else:
            demonio.cambiar_color("yellow", "white", "orange", "yellow")
        frame_brillo += 1

        if tiempo_transcurridos > 3.0:
            demonio.ocultar()
            dialogo.clear()

            dialogo.goto(heroe.xcor(), heroe.ycor() + 45)
            dialogo.color("cyan")
            dialogo.write(
                "¡Por fin el Rey Caído ha sido derrotado!",
                align="center",
                font=("Arial", 12, "bold"),
            )

            estado_juego = "FIN_VICTORIA"

    elif estado_juego == "FIN_VICTORIA":
        if mobile_ui is not None:
            mobile_ui.clear()
        hud.clear()
        cuadro_ui.clear()
        hud.goto(0, 30)
        hud.color("gold")
        hud.write(
            "¡VICTORIA ABSOLUTA!", align="center", font=("Courier", 28, "bold")
        )
        hud.goto(0, -30)
        hud.color("white")
        hud.write(
            "[ Toca la pantalla o presiona ENTER para volver al título ]",
            align="center",
            font=("Arial", 12, "bold"),
        )

    elif estado_juego == "FIN_DERROTA":
        if mobile_ui is not None:
            mobile_ui.clear()
        hud.clear()
        cuadro_ui.clear()
        dialogo.clear()

        hud.goto(0, 40)
        hud.color("crimson")
        hud.write(
            "HAS SIDO DERROTADO", align="center", font=("Courier", 26, "bold")
        )

        hud.goto(0, -10)
        hud.color("orange")
        if modo_actual == "PASILLO":
            msg_derrota = (
                "¡Qué mal! El reino ha caído en la destrucción porque has muerto..."
            )
        elif modo_actual == "INFERNO":
            msg_derrota = "¡El mundo entero se consume en las llamas infinitas! Tu muerte ha traído el Apocalipsis."
        else:
            msg_derrota = "¡Las sombras han cubierto cada rincón del reino tras tu caída!"

        hud.write(msg_derrota, align="center", font=("Arial", 11, "bold"))

        hud.goto(0, -60)
        hud.color("gold")
        hud.write(
            "¡Levántate, héroe! Toca la pantalla o presiona ENTER para reintentar",
            align="center",
            font=("Arial", 11, "bold"),
        )

    try:
        dibujar_controles_mobile()
        ventana.update()
        ventana.ontimer(bucle_principal, 20)
    except Exception:
        pass


# Iniciar bucle principal
bucle_principal()
ventana.mainloop()
