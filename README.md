# sombra-del-rey-demonio
import math
import random
import time
import turtle

# ==========================================
# CONFIGURACIÓN DE LA VENTANA
# ==========================================
ventana = turtle.Screen()
ventana.title("CHRONICLES OF THE FALLEN KING - ARENA TOP-DOWN")
ventana.bgcolor("#0a0510")
ventana.setup(width=800, height=600)
ventana.tracer(0)

estado_juego = "INICIO"
demon_mode_desbloqueado = False
modo_actual = "NORMAL"  # Puede ser "NORMAL" o "DEMON"

# ==========================================
# BALANCE DE BATALLA
# ==========================================
MAX_SALUD_HEROE = 3000
MAX_SALUD_DEMONIO = 50000
DANO_HEROE = 180

salud_heroe = MAX_SALUD_HEROE
salud_demonio = MAX_SALUD_DEMONIO

tiempo_ultimo_ataque_t = time.time()
tiempo_ultima_frase = time.time()
tiempo_ultimo_ataque_demonio = time.time()

tiempo_inicio_animacion = 0
frame_brillo = 0
frame_alarma = 0

frases_demonio = [
    "¡Siente la desesperación, mortal!",
    "¡No podrás huir de mi sombra!",
    "¡Cada paso que das me acerca a tu fin!",
    "¡Tus ataques son insignificantes!",
    "¡Esta arena será tu tumba!",
    "¡Mi poder ha gobernado eras enteras!",
    "¡Arrodíllate ante el verdadero Rey!",
    "¡Tu feble espada no me destruirá!",
    "¡Miserable... vas a pagar por tu osadía!",
    "¡Nada escapa a las llamas oscuras!",
    "¡Apenas estoy usando una fracción de mi fuerza!",
    "¡Contempla el verdadero poder absoluto!",
]

# ==========================================
# DIBUJO DEL ESCENARIO Y TRONO
# ==========================================
fondo = turtle.Turtle()
fondo.speed(0)
fondo.penup()
fondo.hideturtle()


def dibujar_escenario_topdown():
    fondo.clear()

    if modo_actual == "DEMON":
        color_pared = "#3a0505"
        color_piso = "#1f050a"
        color_grid = "#420d18"
    else:
        color_pared = "#2a1836"
        color_piso = "#181524"
        color_grid = "#252033"

    # 1. Marco exterior
    fondo.goto(-390, 290)
    fondo.color(color_pared)
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(780)
        fondo.right(90)
        fondo.forward(580)
        fondo.right(90)
    fondo.end_fill()

    # 2. Suelo principal
    fondo.goto(-370, 270)
    fondo.color(color_piso)
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(740)
        fondo.right(90)
        fondo.forward(540)
        fondo.right(90)
    fondo.end_fill()

    # 3. Cuadrícula
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

    # 4. Círculo Mágico Central
    fondo.goto(0, -90)
    fondo.color("#521d1d" if modo_actual == "DEMON" else "#3d1d52")
    fondo.pensize(4)
    fondo.pendown()
    fondo.circle(90)
    fondo.penup()

    # 5. DIBUJO DEL TRONO
    fondo.goto(-60, 230)
    fondo.color("#120718")
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(120)
        fondo.right(90)
        fondo.forward(80)
        fondo.right(90)
    fondo.end_fill()

    fondo.goto(-25, 230)
    fondo.color("#800c1e")
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(50)
        fondo.right(90)
        fondo.forward(120)
        fondo.right(90)
    fondo.end_fill()

    fondo.goto(-40, 220)
    fondo.color("#3d0b1a")
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(80)
        fondo.right(90)
        fondo.forward(25)
        fondo.right(90)
    fondo.end_fill()

    fondo.goto(-30, 205)
    fondo.color("#9e1329")
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(60)
        fondo.right(90)
        fondo.forward(30)
        fondo.right(90)
    fondo.end_fill()

    fondo.goto(-38, 205)
    fondo.color("gold")
    fondo.dot(12)
    fondo.goto(38, 205)
    fondo.dot(12)

    for esq_x, esq_y in [
        (-340, 240),
        (340, 240),
        (-340, -240),
        (340, -240),
    ]:
        fondo.goto(esq_x, esq_y)
        fondo.color("#000000")
        fondo.dot(30)
        fondo.color("crimson")
        fondo.dot(20)
        fondo.color("orange")
        fondo.dot(10)


dibujar_escenario_topdown()

# ==========================================
# MURO DE FUEGO Y LUZ ROJA DE ALARMAS
# ==========================================
muro_fuego = turtle.Turtle()
muro_fuego.speed(0)
muro_fuego.penup()
muro_fuego.hideturtle()


def dibujar_muro_fuego_completo():
    global frame_alarma
    muro_fuego.clear()

    if modo_actual == "DEMON":
        frame_alarma += 1
        es_rojo_intenso = (frame_alarma // 5) % 2 == 0
        colores_fuego = (
            ["#ff0000", "#990000", "#ff3333", "#ff0055"]
            if es_rojo_intenso
            else ["#660000", "#330000", "#990000", "#ff0000"]
        )

        if es_rojo_intenso:
            ventana.bgcolor("#240204")
        else:
            ventana.bgcolor("#0a0510")
    else:
        colores_fuego = ["#ff3300", "#ff6600", "#ffcc00", "crimson"]

    # Pared Superior e Inferior
    for x in range(-360, 370, 30):
        muro_fuego.goto(x, 260)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 30))

        muro_fuego.goto(x, -260)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 30))

    # Pared Izquierda y Derecha
    for y in range(-250, 260, 30):
        muro_fuego.goto(-360, y)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 30))

        muro_fuego.goto(360, y)
        muro_fuego.color(random.choice(colores_fuego))
        muro_fuego.dot(random.randint(18, 30))


# ==========================================
# PERSONAJES CON CAPA DINÁMICA
# ==========================================
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
            self.base.color("firebrick")
            self.base.shapesize(stretch_wid=1.8, stretch_len=2.2)
            self.orientacion_capa = 180

            self.cuerpo.shape("circle")
            self.cuerpo.color("dodgerblue")
            self.cuerpo.shapesize(stretch_wid=1.5, stretch_len=1.5)

            self.cabeza.shape("circle")
            self.cabeza.color("gold")
            self.cabeza.shapesize(stretch_wid=0.8, stretch_len=0.8)
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

    def ir_a(self, x, y, angulo_capa=None):
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
hud.color("white")
hud.penup()
hud.hideturtle()

dialogo = turtle.Turtle()
dialogo.speed(0)
dialogo.color("yellow")
dialogo.penup()
dialogo.hideturtle()

proyectiles = []


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


# ==========================================
# CONTROLES Y LÓGICA DE INICIO
# ==========================================
def mover_arriba():
    if estado_juego == "JUGANDO" and heroe.ycor() < 240:
        heroe.ir_a(heroe.xcor(), heroe.ycor() + 20, angulo_capa=270)


def mover_abajo():
    if estado_juego == "JUGANDO" and heroe.ycor() > -240:
        heroe.ir_a(heroe.xcor(), heroe.ycor() - 20, angulo_capa=90)


def mover_izquierda():
    if estado_juego == "JUGANDO" and heroe.xcor() > -340:
        heroe.ir_a(heroe.xcor() - 20, heroe.ycor(), angulo_capa=0)


def mover_derecha():
    if estado_juego == "JUGANDO" and heroe.xcor() < 340:
        heroe.ir_a(heroe.xcor() + 20, heroe.ycor(), angulo_capa=180)


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
    global estado_juego
    if estado_juego in ["JUGANDO", "PAUSA"]:
        limpiar_proyectiles()
        muro_fuego.clear()
        hud.clear()
        dialogo.clear()

        heroe.ocultar()
        demonio.ocultar()
        espada.hideturtle()

        ventana.bgcolor("#0a0510")
        estado_juego = "INICIO"
        mostrar_menu()


def iniciar_modo_juego(modo):
    global estado_juego, salud_heroe, salud_demonio, modo_actual
    modo_actual = modo
    estado_juego = "JUGANDO"
    titulo_txt.clear()

    if modo_actual == "DEMON":
        salud_heroe = 1000  # 1000 de vida en Demon Mode
        salud_demonio = 100000
    else:
        salud_heroe = MAX_SALUD_HEROE
        salud_demonio = MAX_SALUD_DEMONIO

    dibujar_escenario_topdown()
    demonio.restaurar_colores_demonio()

    heroe.ir_a(-220, 0, angulo_capa=180)
    heroe.mostrar()

    demonio.ir_a(220, 0)
    demonio.mostrar()


def procesar_enter():
    global estado_juego
    if estado_juego == "INICIO":
        iniciar_modo_juego("NORMAL")

    elif estado_juego in ["FIN_VICTORIA", "FIN_DERROTA"]:
        limpiar_proyectiles()
        muro_fuego.clear()
        hud.clear()
        dialogo.clear()

        heroe.ocultar()
        demonio.ocultar()
        espada.hideturtle()

        ventana.bgcolor("#0a0510")
        estado_juego = "INICIO"
        mostrar_menu()


def procesar_w():
    global estado_juego
    if estado_juego == "INICIO" and demon_mode_desbloqueado:
        iniciar_modo_juego("DEMON")


ventana.listen()
ventana.onkeypress(mover_arriba, "Up")
ventana.onkeypress(mover_abajo, "Down")
ventana.onkeypress(mover_izquierda, "Left")
ventana.onkeypress(mover_derecha, "Right")
ventana.onkeypress(realizar_ataque, "space")
ventana.onkeypress(alternar_pausa, "z")
ventana.onkeypress(alternar_pausa, "Z")
ventana.onkeypress(salir_al_titulo, "x")
ventana.onkeypress(salir_al_titulo, "X")
ventana.onkeypress(procesar_enter, "Return")
ventana.onkeypress(procesar_w, "w")
ventana.onkeypress(procesar_w, "W")


def mostrar_menu():
    ventana.bgcolor("#0a0510")
    titulo_txt.clear()
    titulo_txt.goto(0, 110)
    titulo_txt.color("orange")
    titulo_txt.write(
        "--- LA SOMBRA DEL REY DEMONIO ---",
        align="center",
        font=("Impact", 26, "bold"),
    )

    titulo_txt.goto(0, 50)
    titulo_txt.color("crimson")
    titulo_txt.write(
        "BATALLA EN EL SALÓN DEL TRONO",
        align="center",
        font=("Courier", 15, "bold"),
    )

    titulo_txt.goto(0, -40)
    titulo_txt.color("yellow")
    titulo_txt.write(
        "[ Presiona ENTER para Comenzar ]",
        align="center",
        font=("Arial", 16, "bold"),
    )

    if demon_mode_desbloqueado:
        titulo_txt.goto(0, -90)
        titulo_txt.color("red")
        titulo_txt.write(
            "[ PRESIONA W PARA ENTRAR AL DEMON MODE ]",
            align="center",
            font=("Impact", 16, "bold"),
        )

    titulo_txt.goto(0, -150)
    titulo_txt.color("lightgray")
    titulo_txt.write(
        "Controles:\nFlechas: Moverte  |  Espacio: Ataque\nZ: Pausa  |  X: Salir al Menú",
        align="center",
        font=("Courier", 11, "normal"),
    )


mostrar_menu()

# ==========================================
# BUCLE PRINCIPAL (OPTIMIZADO CON ONTIMER)
# ==========================================
def bucle_principal():
    global estado_juego, salud_demonio, salud_heroe, demon_mode_desbloqueado
    global tiempo_ultima_frase, tiempo_ultimo_ataque_demonio, tiempo_ultimo_ataque_t
    global atacando, frame_brillo, tiempo_inicio_animacion

    if estado_juego == "PAUSA":
        hud.clear()
        hud.goto(0, 30)
        hud.color("yellow")
        hud.write(
            "=== JUEGO EN PAUSA ===",
            align="center",
            font=("Impact", 30, "bold"),
        )
        hud.goto(0, -20)
        hud.color("white")
        hud.write(
            "[ Z: Reanudar  |  X: Salir al Título ]",
            align="center",
            font=("Arial", 14, "bold"),
        )

    elif estado_juego == "JUGANDO":
        tiempo_actual = time.time()

        dibujar_muro_fuego_completo()

        hud.clear()
        hud.color("red" if modo_actual == "DEMON" else "white")
        etiqueta_modo = " [DEMON MODE]" if modo_actual == "DEMON" else ""
        hud.goto(0, 250)
        hud.write(
            f"Héroe: {int(salud_heroe)} HP   |   Rey Demonio: {int(salud_demonio)} HP{etiqueta_modo}\n[ESPACIO]: Atacar  |  [Z]: Pausa  |  [X]: Menú",
            align="center",
            font=("Courier", 11, "bold"),
        )

        if tiempo_actual - tiempo_ultima_frase > 4.5:
            dialogo.clear()
            dialogo.goto(demonio.xcor(), demonio.ycor() + 55)
            dialogo.color("red" if modo_actual == "DEMON" else "yellow")
            dialogo.write(
                random.choice(frases_demonio),
                align="center",
                font=("Arial", 11, "italic"),
            )
            tiempo_ultima_frase = tiempo_actual

        dx_d = heroe.xcor() - demonio.xcor()
        dy_d = heroe.ycor() - demonio.ycor()
        ang_demonio = math.atan2(dy_d, dx_d)

        velocidad_intimidante = 0.6 if modo_actual == "DEMON" else 0.45
        nuevo_x_d = demonio.xcor() + math.cos(ang_demonio) * velocidad_intimidante
        nuevo_y_d = demonio.ycor() + math.sin(ang_demonio) * velocidad_intimidante
        demonio.ir_a(nuevo_x_d, nuevo_y_d)

        dx_e = demonio.xcor() - heroe.xcor()
        dy_e = demonio.ycor() - heroe.ycor()
        angulo_hacia_demonio = math.degrees(math.atan2(dy_e, dx_e))

        espada.setheading(angulo_hacia_demonio)

        if atacando:
            espada.showturtle()
            espada.setx(
                heroe.xcor()
                + math.cos(math.radians(angulo_hacia_demonio)) * 55
            )
            espada.sety(
                heroe.ycor()
                + math.sin(math.radians(angulo_hacia_demonio)) * 55
            )

            dist_espada = math.hypot(
                espada.xcor() - demonio.xcor(), espada.ycor() - demonio.ycor()
            )
            if dist_espada < 65:
                salud_demonio -= DANO_HEROE
            atacando = False
        else:
            espada.hideturtle()
            espada.goto(heroe.xcor(), heroe.ycor())

        if tiempo_actual - tiempo_ultimo_ataque_demonio > 2.0:
            tipo = random.choice(["corto", "largo"])
            vel = 8.5 if modo_actual == "DEMON" else 7.5
            tam = 2.0 if tipo == "largo" else 1.0

            crear_proyectil(
                demonio.xcor(),
                demonio.ycor(),
                math.cos(ang_demonio) * vel,
                math.sin(ang_demonio) * vel,
                "red",
                tam,
            )
            tiempo_ultimo_ataque_demonio = tiempo_actual

        if tiempo_actual - tiempo_ultimo_ataque_t > (
            4.5 if modo_actual == "DEMON" else 6.0
        ):
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

        # --- COLISIONES ---
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
            
            radio_impacto = 20 * p.tamano
            if dist_p < radio_impacto:
                salud_heroe -= 60 if modo_actual == "DEMON" else 45
                p.hideturtle()
                if p in proyectiles:
                    proyectiles.remove(p)
            elif abs(p.xcor()) > 370 or abs(p.ycor()) > 270:
                p.hideturtle()
                if p in proyectiles:
                    proyectiles.remove(p)

        dist_contacto = math.hypot(
            demonio.xcor() - heroe.xcor(), demonio.ycor() - heroe.ycor()
        )
        if dist_contacto < 45:
            salud_heroe -= 6.0 if modo_actual == "DEMON" else 4.5

        if salud_demonio <= 0:
            salud_demonio = 0
            estado_juego = "ANIM_VICTORIA"
            demon_mode_desbloqueado = True
            tiempo_inicio_animacion = time.time()
            limpiar_proyectiles()

        elif salud_heroe <= 0:
            salud_heroe = 0
            estado_juego = "FIN_DERROTA"
            limpiar_proyectiles()

    elif estado_juego == "ANIM_VICTORIA":
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
                "¡Por fin se ha ido y podremos liberar al reino!",
                align="center",
                font=("Arial", 12, "bold"),
            )

            estado_juego = "FIN_VICTORIA"

    elif estado_juego == "FIN_VICTORIA":
        hud.clear()
        hud.goto(0, 30)
        hud.color("gold")
        hud.write("¡TÚ GANASTE!", align="center", font=("Courier", 28, "bold"))
        hud.goto(0, -30)
        hud.color("white")
        hud.write(
            "[ Presiona ENTER para volver al título ]",
            align="center",
            font=("Arial", 14, "bold"),
        )

    elif estado_juego == "FIN_DERROTA":
        hud.clear()
        dialogo.clear()

        hud.goto(0, 30)
        hud.color("crimson")
        hud.write("FIN DEL JUEGO", align="center", font=("Courier", 28, "bold"))
        hud.goto(0, -30)
        hud.color("white")
        hud.write(
            "[ Presiona ENTER para volver al título ]",
            align="center",
            font=("Arial", 14, "bold"),
        )

    ventana.update()
    ventana.ontimer(bucle_principal, 20)

# Arrancar el bucle principal
bucle_principal()
ventana.mainloop()
