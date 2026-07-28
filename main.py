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

# Estados del juego: "INICIO", "JUGANDO", "FIN_VICTORIA", "FIN_DERROTA"
estado_juego = "INICIO"

# ==========================================
# BALANCE DE BATALLA (~5 MINUTOS)
# ==========================================
MAX_SALUD_HEROE = 1500
MAX_SALUD_DEMONIO = 12000

salud_heroe = MAX_SALUD_HEROE
salud_demonio = MAX_SALUD_DEMONIO

tiempo_ultimo_ataque_t = time.time()
tiempo_ultima_frase = time.time()
tiempo_ultimo_ataque_demonio = time.time()

frases_demonio = [
    "¡Siente la desesperación, mortal!",
    "¡No podrás huir de mi sombra!",
    "¡Cada paso que das me acerca a tu fin!",
    "¡Tus ataques son insignificantes!",
    "¡Esta arena será tu tumba!",
]

# ==========================================
# DIBUJO DEL ESCENARIO (SUELO DESDE ARRIBA)
# ==========================================
fondo = turtle.Turtle()
fondo.speed(0)
fondo.penup()
fondo.hideturtle()


def dibujar_escenario_topdown():
    fondo.clear()

    # 1. Marco exterior de la arena
    fondo.goto(-390, 290)
    fondo.color("#2a1836")
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(780)
        fondo.right(90)
        fondo.forward(580)
        fondo.right(90)
    fondo.end_fill()

    # 2. Suelo principal de piedra
    fondo.goto(-370, 270)
    fondo.color("#181524")
    fondo.begin_fill()
    for _ in range(2):
        fondo.forward(740)
        fondo.right(90)
        fondo.forward(540)
        fondo.right(90)
    fondo.end_fill()

    # 3. Cuadrícula de baldosas
    fondo.color("#252033")
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
    fondo.color("#3d1d52")
    fondo.pensize(4)
    fondo.pendown()
    fondo.circle(90)
    fondo.penup()

    # Antorchas en las esquinas
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
# PERSONAJES CON CAPA Y CUERNOS
# ==========================================
titulo_txt = turtle.Turtle()
titulo_txt.speed(0)
titulo_txt.penup()
titulo_txt.hideturtle()


class PersonajeTopDown:

    def __init__(self, es_heroe=True):
        self.es_heroe = es_heroe

        # Elemento 1: Capa (Héroe) / Aura (Demonio)
        self.base = turtle.Turtle()
        self.base.speed(0)
        self.base.penup()

        # Elemento 2: Cuerpo / Armadura
        self.cuerpo = turtle.Turtle()
        self.cuerpo.speed(0)
        self.cuerpo.penup()

        # Elemento 3: Cabeza (Héroe) / Corona (Demonio)
        self.cabeza = turtle.Turtle()
        self.cabeza.speed(0)
        self.cabeza.penup()

        # Elementos Extra: Cuernos del Rey Demonio
        self.cuerno_izq = turtle.Turtle()
        self.cuerno_izq.speed(0)
        self.cuerno_izq.penup()

        self.cuerno_der = turtle.Turtle()
        self.cuerno_der.speed(0)
        self.cuerno_der.penup()

        if es_heroe:
            # CAPA ROJA DE FLAMEADO
            self.base.shape("triangle")
            self.base.color("firebrick")
            self.base.shapesize(stretch_wid=1.8, stretch_len=2.2)
            self.base.setheading(180)  # Apunta hacia atrás

            # ARMADURA Y HOMBRERAS AZULES
            self.cuerpo.shape("circle")
            self.cuerpo.color("dodgerblue")
            self.cuerpo.shapesize(stretch_wid=1.5, stretch_len=1.5)

            # CASCO DORADO
            self.cabeza.shape("circle")
            self.cabeza.color("gold")
            self.cabeza.shapesize(stretch_wid=0.8, stretch_len=0.8)

        else:
            # AURA OSCURA
            self.base.shape("circle")
            self.base.color("#3d000c")
            self.base.shapesize(stretch_wid=4.5, stretch_len=4.5)

            # CUERPO DEL DEMONIO
            self.cuerpo.shape("square")
            self.cuerpo.color("crimson")
            self.cuerpo.shapesize(stretch_wid=3.2, stretch_len=3.2)

            # CORONA DORADA
            self.cabeza.shape("triangle")
            self.cabeza.color("gold")
            self.cabeza.shapesize(stretch_wid=1.6, stretch_len=2.0)

            # CUERNOS DEMONIACOS GRANDES
            self.cuerno_izq.shape("triangle")
            self.cuerno_izq.color("black")
            self.cuerno_izq.shapesize(stretch_wid=0.8, stretch_len=2.5)
            self.cuerno_izq.setheading(135)

            self.cuerno_der.shape("triangle")
            self.cuerno_der.color("black")
            self.cuerno_der.shapesize(stretch_wid=0.8, stretch_len=2.5)
            self.cuerno_der.setheading(45)

        self.ocultar()

    def ir_a(self, x, y):
        self.cuerpo.goto(x, y)

        if self.es_heroe:
            self.base.goto(x - 15, y)  # Capa roja extendida hacia atrás
            self.cabeza.goto(x, y)
        else:
            self.base.goto(x, y)
            self.cabeza.goto(x, y + 10)
            # Posición de los Cuernos
            self.cuerno_izq.goto(x - 25, y + 25)
            self.cuerno_der.goto(x + 25, y + 25)

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

# Espada Gigante Vistas desde Arriba
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


def crear_proyectil(x, y, dx, dy, color, tamano):
    p = turtle.Turtle()
    p.speed(0)
    p.shape("circle")
    p.color(color)
    p.shapesize(stretch_wid=tamano, stretch_len=tamano)
    p.penup()
    p.goto(x, y)
    p.dx = dx
    p.dy = dy
    proyectiles.append(p)


def limpiar_proyectiles():
    for p in proyectiles:
        p.hideturtle()
    proyectiles.clear()


# ==========================================
# CONTROLES Y MOVIMIENTO
# ==========================================
def mover_arriba():
    if estado_juego == "JUGANDO" and heroe.ycor() < 240:
        heroe.ir_a(heroe.xcor(), heroe.ycor() + 20)


def mover_abajo():
    if estado_juego == "JUGANDO" and heroe.ycor() > -240:
        heroe.ir_a(heroe.xcor(), heroe.ycor() - 20)


def mover_izquierda():
    if estado_juego == "JUGANDO" and heroe.xcor() > -340:
        heroe.ir_a(heroe.xcor() - 20, heroe.ycor())


def mover_derecha():
    if estado_juego == "JUGANDO" and heroe.xcor() < 340:
        heroe.ir_a(heroe.xcor() + 20, heroe.ycor())


def realizar_ataque():
    global atacando
    if estado_juego == "JUGANDO" and not atacando:
        atacando = True


def procesar_enter():
    global estado_juego, salud_heroe, salud_demonio

    if estado_juego == "INICIO":
        estado_juego = "JUGANDO"
        titulo_txt.clear()

        salud_heroe = MAX_SALUD_HEROE
        salud_demonio = MAX_SALUD_DEMONIO

        heroe.ir_a(-220, 0)
        heroe.mostrar()

        demonio.ir_a(220, 0)
        demonio.mostrar()

    elif estado_juego in ["FIN_VICTORIA", "FIN_DERROTA"]:
        limpiar_proyectiles()
        hud.clear()
        dialogo.clear()

        heroe.ocultar()
        demonio.ocultar()
        espada.hideturtle()

        estado_juego = "INICIO"
        mostrar_menu()


ventana.listen()
ventana.onkeypress(mover_arriba, "Up")
ventana.onkeypress(mover_abajo, "Down")
ventana.onkeypress(mover_izquierda, "Left")
ventana.onkeypress(mover_derecha, "Right")
ventana.onkeypress(realizar_ataque, "space")
ventana.onkeypress(procesar_enter, "Return")


# ==========================================
# PANTALLA DE INICIO
# ==========================================
def mostrar_menu():
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
        "BATALLA EN LA ARENA DE PIEDRA",
        align="center",
        font=("Courier", 15, "bold"),
    )

    titulo_txt.goto(0, -60)
    titulo_txt.color("yellow")
    titulo_txt.write(
        "[ Presiona ENTER para Comenzar ]",
        align="center",
        font=("Arial", 18, "bold"),
    )

    titulo_txt.goto(0, -140)
    titulo_txt.color("lightgray")
    titulo_txt.write(
        "Controles:\nFlechas: Moverte  |  Espacio: Ataque de Espada",
        align="center",
        font=("Courier", 12, "normal"),
    )


mostrar_menu()

# ==========================================
# BUCLE PRINCIPAL DEL JUEGO
# ==========================================
while True:
    ventana.update()
    time.sleep(0.02)

    if estado_juego == "JUGANDO":
        tiempo_actual = time.time()

        # --- 1. HUD Y FRASES ---
        hud.clear()
        hud.goto(0, 250)
        hud.write(
            f"Héroe: {salud_heroe} HP   |   Rey Demonio: {salud_demonio} HP\n[ESPACIO]: Atacar con Espada",
            align="center",
            font=("Courier", 12, "bold"),
        )

        if tiempo_actual - tiempo_ultima_frase > 6.0:
            dialogo.clear()
            dialogo.goto(demonio.xcor(), demonio.ycor() + 50)
            dialogo.write(
                random.choice(frases_demonio),
                align="center",
                font=("Arial", 11, "italic"),
            )
            tiempo_ultima_frase = tiempo_actual

        # --- 2. MOVIMIENTO DEL REY DEMONIO ---
        dx_d = heroe.xcor() - demonio.xcor()
        dy_d = heroe.ycor() - demonio.ycor()
        ang_demonio = math.atan2(dy_d, dx_d)

        velocidad_intimidante = 0.45
        nuevo_x_d = demonio.xcor() + math.cos(ang_demonio) * velocidad_intimidante
        nuevo_y_d = demonio.ycor() + math.sin(ang_demonio) * velocidad_intimidante
        demonio.ir_a(nuevo_x_d, nuevo_y_d)

        # --- 3. ESPADA MÁGICA DEL HÉROE ---
        dx_e = demonio.xcor() - heroe.xcor()
        dy_e = demonio.ycor() - heroe.ycor()
        angulo_grad = math.degrees(math.atan2(dy_e, dx_e))
        espada.setheading(angulo_grad)

        if atacando:
            espada.showturtle()
            espada.setx(heroe.xcor() + math.cos(math.radians(angulo_grad)) * 55)
            espada.sety(heroe.ycor() + math.sin(math.radians(angulo_grad)) * 55)

            dist_espada = math.hypot(
                espada.xcor() - demonio.xcor(), espada.ycor() - demonio.ycor()
            )
            if dist_espada < 65:
                salud_demonio -= 40
            atacando = False
        else:
            espada.hideturtle()
            espada.goto(heroe.xcor(), heroe.ycor())

        # --- 4. ATAQUES Y PROYECTILES ---
        if tiempo_actual - tiempo_ultimo_ataque_demonio > 2.0:
            tipo = random.choice(["corto", "largo"])
            vel = 7.5 if tipo == "corto" else 4.0
            tam = 1.0 if tipo == "corto" else 2.0

            crear_proyectil(
                demonio.xcor(),
                demonio.ycor(),
                math.cos(ang_demonio) * vel,
                math.sin(ang_demonio) * vel,
                "red",
                tam,
            )
            tiempo_ultimo_ataque_demonio = tiempo_actual

        # Ataque Especial en T
        if tiempo_actual - tiempo_ultimo_ataque_t > 6.5:
            crear_proyectil(
                demonio.xcor(),
                demonio.ycor(),
                math.cos(ang_demonio) * 6.5,
                math.sin(ang_demonio) * 6.5,
                "magenta",
                1.5,
            )

            rad_izq = ang_demonio + math.pi / 2
            rad_der = ang_demonio - math.pi / 2
            crear_proyectil(
                demonio.xcor(),
                demonio.ycor(),
                math.cos(rad_izq) * 5.5,
                math.sin(rad_izq) * 5.5,
                "magenta",
                1.3,
            )
            crear_proyectil(
                demonio.xcor(),
                demonio.ycor(),
                math.cos(rad_der) * 5.5,
                math.sin(rad_der) * 5.5,
                "magenta",
                1.3,
            )

            tiempo_ultimo_ataque_t = tiempo_actual

        # --- 5. COLISIONES ---
        for p in proyectiles[:]:
            p.setx(p.xcor() + p.dx)
            p.sety(p.ycor() + p.dy)

            dist_p = math.hypot(
                p.xcor() - heroe.xcor(), p.ycor() - heroe.ycor()
            )
            if dist_p < 25:
                salud_heroe -= 15
                p.hideturtle()
                proyectiles.remove(p)
            elif abs(p.xcor()) > 370 or abs(p.ycor()) > 270:
                p.hideturtle()
                proyectiles.remove(p)

        dist_contacto = math.hypot(
            demonio.xcor() - heroe.xcor(), demonio.ycor() - heroe.ycor()
        )
        if dist_contacto < 45:
            salud_heroe -= 1.5

        # --- 6. CONDICIONES DE FIN DE JUEGO ---
        if salud_demonio <= 0:
            salud_demonio = 0
            estado_juego = "FIN_VICTORIA"
            limpiar_proyectiles()

        elif salud_heroe <= 0:
            salud_heroe = 0
            estado_juego = "FIN_DERROTA"
            limpiar_proyectiles()

    # --- PANTALLA DE VICTORIA CON DIÁLOGO FINAL ---
    elif estado_juego == "FIN_VICTORIA":
        hud.clear()
        dialogo.clear()
        dialogo.goto(demonio.xcor(), demonio.ycor() + 50)
        dialogo.write(
            "¡No... esto no puede ser mi fin...!",
            align="center",
            font=("Arial", 12, "bold"),
        )

        hud.goto(0, 30)
        hud.write("¡TÚ GANASTE!", align="center", font=("Courier", 28, "bold"))
        hud.goto(0, -30)
        hud.write(
            "[ Presiona ENTER para volver al título ]",
            align="center",
            font=("Arial", 14, "bold"),
        )

    # --- PANTALLA DE DERROTA ---
    elif estado_juego == "FIN_DERROTA":
        hud.clear()
        dialogo.clear()

        hud.goto(0, 30)
        hud.write("FIN DEL JUEGO", align="center", font=("Courier", 28, "bold"))
        hud.goto(0, -30)
        hud.write(
            "[ Presiona ENTER para volver al título ]",
            align="center",
            font=("Arial", 14, "bold"),
        )