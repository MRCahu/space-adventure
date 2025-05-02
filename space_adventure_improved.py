#!/usr/bin/env python3
"""
space_adventure_improved.py

Jogo Space Adventure refatorado:
- Configuração via CLI (argparse)
- Tipos anotados e PEP8
- Logging para diagnóstico
- Maior modularidade e limpeza
"""
import argparse
import logging
import math
import random
import sys
from typing import List, Optional

# Tenta importar turtle; se falhar, informa ao usuário e encerra
try:
    import turtle
except ModuleNotFoundError:
    print("Erro: módulo 'turtle' não encontrado. Execute este jogo em um ambiente local com suporte gráfico (Tkinter).")
    sys.exit(1)


# ——————————————————————————————————————————————————————————————
# CONFIGURAÇÃO E LOGGING
# ——————————————————————————————————————————————————————————————
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Jogo Space Adventure - Colete estrelas e evite asteroides"
    )
    parser.add_argument("--width", type=int, default=800,
                        help="Largura da tela (px)")
    parser.add_argument("--height", type=int, default=600,
                        help="Altura da tela (px)")
    parser.add_argument("--stars", type=int, default=10,
                        help="Número de estrelas para coletar")
    parser.add_argument("--asteroids", type=int, default=5,
                        help="Número inicial de asteroides")
    parser.add_argument("--lives", type=int, default=3,
                        help="Número de vidas do jogador")
    parser.add_argument("--speed", type=float, default=20.0,
                        help="Velocidade da nave")
    parser.add_argument("--debug", action="store_true",
                        help="Habilita logging de debug")
    return parser.parse_args()


def setup_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s", level=level
    )
    logging.debug("Logging iniciado (DEBUG=%s)", debug)


# ——————————————————————————————————————————————————————————————
# CLASSE GENÉRICA PARA OBJETOS
# ——————————————————————————————————————————————————————————————
class GameObject:
    """
    Abstração para objetos Turtle (shape, cor, tamanho, visibilidade).
    """
    def __init__(
        self,
        shape: str,
        color: str,
        size: float = 1.0,
        visible: bool = True
    ) -> None:
        self.turtle = turtle.Turtle(shape=shape)
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.shapesize(stretch_wid=size, stretch_len=size)
        self.active: bool = visible
        if not visible:
            self.turtle.hideturtle()

    def show(self) -> None:
        self.active = True
        self.turtle.showturtle()

    def hide(self) -> None:
        self.active = False
        self.turtle.hideturtle()

    def goto(self, x: float, y: float) -> None:
        self.turtle.goto(x, y)

    def distance(self, other: "GameObject") -> float:
        return self.turtle.distance(other.turtle)

    def setheading(self, angle: float) -> None:
        self.turtle.setheading(angle)

    def heading(self) -> float:
        return self.turtle.heading()

    def forward(self, dist: float) -> None:
        self.turtle.forward(dist)

    def clear(self) -> None:
        self.turtle.clear()


# ——————————————————————————————————————————————————————————————
# CLASSE DO JOGO
# ——————————————————————————————————————————————————————————————
class SpaceGame:
    """
    Gerencia loop principal, detecção de colisões, pontuação e níveis.
    """
    def __init__(
        self,
        width: int,
        height: int,
        num_stars: int,
        num_asteroids: int,
        lives: int,
        ship_speed: float
    ) -> None:
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.num_asteroids = num_asteroids
        self.max_lives = lives
        self.ship_speed = ship_speed

        self.level = 1
        self.score = 0
        self.lives = lives
        self.game_over = True
        self.stars_left = num_stars
        self.asteroid_speed = 2.0

        self.bg_stars: List[GameObject] = []
        self.stars: List[GameObject] = []
        self.asteroids: List[GameObject] = []

        self.ship: Optional[GameObject] = None
        self.prop: Optional[GameObject] = None
        self.hud: Optional[GameObject] = None

        self._init_screen()
        self._show_start()

    def _init_screen(self) -> None:
        turtle.clearscreen()
        self.screen = turtle.Screen()
        self.screen.setup(self.width, self.height)
        self.screen.title(f"🚀 Space Adventure — Nível {self.level}")
        self.screen.bgcolor("black")
        self.screen.tracer(0)

        self.screen.listen()
        self.screen.onkey(self._move_forward, "Up")
        self.screen.onkey(self._turn_left, "Left")
        self.screen.onkey(self._turn_right, "Right")
        self.screen.onkey(self.start, "space")
        self.screen.onkey(self.restart, "r")
        logging.debug("Tela inicializada com largura=%d, altura=%d", self.width, self.height)

    def _show_start(self) -> None:
        msg = turtle.Turtle()
        msg.hideturtle()
        msg.color("cyan")
        msg.write(
            "Pressione ESPAÇO para começar",
            align="center",
            font=("Arial", 24, "bold"),
        )
        self.screen.update()

    def start(self) -> None:
        if not self.game_over:
            return
        self.game_over = False
        self._reset_level()
        logging.info("Iniciando nível %d", self.level)
        self._loop()

    def restart(self) -> None:
        if not self.game_over:
            return
        self.level = 1
        self.score = 0
        self.lives = self.max_lives
        self.start()

    def _reset_level(self) -> None:
        turtle.clearscreen()
        self._init_screen()
        self._draw_border()
        self._create_objects()
        self._place_items()
        self._update_hud()

    def _draw_border(self) -> None:
        b = turtle.Turtle()
        b.hideturtle()
        b.color("blue")
        b.pensize(3)
        b.penup()
        b.goto(-self.width / 2, -self.height / 2)
        b.pendown()
        for _ in range(2):
            b.forward(self.width)
            b.left(90)
            b.forward(self.height)
            b.left(90)

    def _create_objects(self) -> None:
        # Fundo com estrelas pequenas
        self.bg_stars = [
            self._make_obj("circle", "white", 0.1, (
                random.randint(-self.width // 2, self.width // 2),
                random.randint(-self.height // 2, self.height // 2),
            ))
            for _ in range(50)
        ]

        # Nave e efeito propulsor
        self.ship = self._make_obj("triangle", "white", 1.2, (0, 0))
        self.ship.setheading(90)
        self.prop = self._make_obj("triangle", "orange", 0.5, (0, 0), visible=False)

        # Estrelas colecionáveis e asteroides (escondidos inicialmente)
        self.stars = [
            self._make_obj("circle", "yellow", 0.8, (0, 0), visible=False)
            for _ in range(self.num_stars)
        ]
        self.asteroids = [
            self._make_obj("circle", "gray", 1.5, (0, 0), visible=False)
            for _ in range(self.num_asteroids)
        ]

        # HUD (placar)
        self.hud = self._make_obj(
            "classic", "white", 1.0,
            (-self.width // 2 + 20, self.height // 2 - 40),
            visible=False
        )

    def _make_obj(
        self,
        shape: str,
        color: str,
        size: float,
        position: tuple,
        visible: bool = True,
    ) -> GameObject:
        obj = GameObject(shape, color, size, visible)
        obj.goto(*position)
        return obj

    def _place_items(self) -> None:
        self.stars_left = self.num_stars
        # Coloca estrelas coletáveis
        for star in self.stars:
            star.show()
            star.goto(
                random.randint(-self.width // 2 + 20, self.width // 2 - 20),
                random.randint(-self.height // 2 + 20, self.height // 2 - 20)
            )
        # Coloca asteroides com heading aleatório
        for ast in self.asteroids:
            ast.show()
            ast.goto(
                random.randint(-self.width // 2 + 40, self.width // 2 - 40),
                random.randint(-self.height // 2 + 40, self.height // 2 - 40)
            )
            ast.setheading(random.random() * 360)

    def _move_forward(self) -> None:
        if self.game_over:
            return
        self.prop.show()
        angle = math.radians(self.ship.heading())
        dx = self.ship_speed * math.cos(angle)
        dy = self.ship_speed * math.sin(angle)
        x, y = self.ship.turtle.position()
        nx, ny = x + dx, y + dy
        if abs(nx) < self.width / 2 - 20 and abs(ny) < self.height / 2 - 20:
            self.ship.goto(nx, ny)
            back_angle = angle + math.pi
            self.prop.goto(
                nx + 20 * math.cos(back_angle),
                ny + 20 * math.sin(back_angle)
            )
            self.prop.setheading(self.ship.heading())
        self._collisions()

    def _turn_left(self) -> None:
        if not self.game_over:
            self.ship.turtle.left(30)

    def _turn_right(self) -> None:
        if not self.game_over:
            self.ship.turtle.right(30)

    def _collisions(self) -> None:
        # Verifica colisão com estrelas
        for star in self.stars:
            if star.active and self.ship.distance(star) < 20:
                star.hide()
                self.score += 10
                self.stars_left -= 1
                self._update_hud()
                if self.stars_left == 0:
                    self._level_up()
                return
        # Verifica colisão com asteroides
        for ast in self.asteroids:
            if ast.active and self.ship.distance(ast) < 25:
                ast.hide()
                self.lives -= 1
                self._update_hud()
                if self.lives <= 0:
                    self._game_over_screen(False)
                else:
                    self.ship.goto(0, 0)
                    self.ship.setheading(90)
                return

    def _update_hud(self) -> None:
        self.hud.clear()
        hearts = "❤️" * self.lives
        text = f"Nível: {self.level}  Pontos: {self.score}  Vidas: {hearts}"
        self.hud.turtle.write(text, font=("Arial", 16, "bold"))
        self.screen.update()

    def _level_up(self) -> None:
        self.score += 50
        self._game_over_screen(True)
        self.screen.ontimer(self._next_level, 2000)

    def _next_level(self) -> None:
        self.level += 1
        self.asteroid_speed += 0.5
        self.start()

    def _move_asteroids(self) -> None:
        if self.game_over:
            return
        for ast in self.asteroids:
            if ast.active:
                ast.forward(self.asteroid_speed)
                x, y = ast.turtle.position()
                if abs(x) > self.width / 2 or abs(y) > self.height / 2:
                    ast.setheading(random.random() * 360)
        self.screen.update()

    def _game_over_screen(self, victory: bool) -> None:
        self.game_over = True
        turtle.clearscreen()
        msg = turtle.Turtle()
        msg.hideturtle()
        msg.color("green" if victory else "red")
        label = "🎉 VITÓRIA! Próximo nível." if victory else "💥 GAME OVER!"
        msg.write(
            f"{label}\nPressione R para reiniciar",
            align="center",
            font=("Arial", 24, "bold"),
        )
        self.screen.update()

    def _loop(self) -> None:
        if not self.game_over:
            self._move_asteroids()
            self.screen.ontimer(self._loop, 30)

    def run(self) -> None:
        turtle.mainloop()


# ——————————————————————————————————————————————————————————————
# PONTO DE ENTRADA
# ——————————————————————————————————————————————————————————————
def main() -> None:
    args = parse_args()
    setup_logging(args.debug)
    game = SpaceGame(
        width=args.width,
        height=args.height,
        num_stars=args.stars,
        num_asteroids=args.asteroids,
        lives=args.lives,
        ship_speed=args.speed,
    )
    game.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Erro durante execução do jogo: %s", e)
        sys.exit(1)
