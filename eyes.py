
import tkinter as tk
import random
import math

WIDTH = 900
HEIGHT = 600

root = tk.Tk()
root.title("Eyes ❤️ Heart")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="black")
root.resizable(False, False)

canvas = tk.Canvas(
    root, width=WIDTH, height=HEIGHT,
    bg="#030506", highlightthickness=0
)
canvas.pack()

# Символы на заднем фоне
symbols = "01アイウエオ<>/\\{}[]#$%&*"
columns = []

for x in range(0, WIDTH, 15):
    columns.append({
        "x": x,
        "y": random.randint(-HEIGHT, HEIGHT),
        "speed": random.randint(3, 8),
        "length": random.randint(8, 22)
    })

frame = 0
start_time = 0


def draw_background():
    canvas.delete("bg")

    for col in columns:
        x = col["x"]
        y = col["y"]

        for i in range(col["length"]):
            char_y = y - i * 16
            if 0 <= char_y <= HEIGHT:
                color = "#ff5a48" if random.random() < 0.08 else "#174b38"
                if i == 0:
                    color = "#71ffb0"

                canvas.create_text(
                    x, char_y,
                    text=random.choice(symbols),
                    fill=color,
                    font=("Consolas", 11),
                    tags="bg"
                )

        col["y"] += col["speed"]

        if col["y"] - col["length"] * 16 > HEIGHT:
            col["y"] = random.randint(-250, -20)
            col["speed"] = random.randint(3, 8)


def draw_eye(cx, cy, opening, blink=1):
    # opening: 0 = закрытый глаз, 1 = открытый
    w = 145
    h = 65 * opening

    if opening < 0.08:
        # Закрытый глаз
        canvas.create_line(
            cx - w, cy,
            cx - 75, cy + 8,
            cx, cy + 14,
            cx + 75, cy + 8,
            cx + w, cy,
            fill="#f2c7b9", width=4,
            smooth=True, capstyle=tk.ROUND
        )
        return

    # Контур глаза
    points = [
        cx - w, cy,
        cx - 90, cy - h * 0.65,
        cx, cy - h,
        cx + 90, cy - h * 0.65,
        cx + w, cy,
        cx + 90, cy + h * 0.65,
        cx, cy + h,
        cx - 90, cy + h * 0.65
    ]

    canvas.create_polygon(
        points, smooth=True,
        fill="#e9b7a5", outline="#f7d9cc", width=2
    )

    # Белок глаза
    canvas.create_oval(
        cx - 105, cy - h * 0.65,
        cx + 105, cy + h * 0.65,
        fill="#fff0e7", outline=""
    )

    # Радужка и зрачок
    radius = max(3, 28 * opening)
    canvas.create_oval(
        cx - radius, cy - radius,
        cx + radius, cy + radius,
        fill="#a52c37", outline="#5e101e", width=2
    )

    canvas.create_oval(
        cx - radius * 0.48, cy - radius * 0.48,
        cx + radius * 0.48, cy + radius * 0.48,
        fill="#100c12", outline=""
    )

    # Блик
    canvas.create_oval(
        cx - 9, cy - 12,
        cx - 2, cy - 5,
        fill="white", outline=""
    )

    # Ресницы
    for side in (-1, 1):
        x1 = cx + side * 95
        canvas.create_line(
            x1, cy - h * 0.48,
            x1 + side * 13, cy - h * 0.85,
            fill="#f2c7b9", width=3
        )


def draw_heart(cx, cy, size):
    # Сердце из координат многоугольника
    points = [
        (0, -0.25), (-0.15, -0.48), (-0.42, -0.48),
        (-0.58, -0.28), (-0.55, -0.05),
        (-0.35, 0.20), (0, 0.52),
        (0.35, 0.20), (0.55, -0.05),
        (0.58, -0.28), (0.42, -0.48),
        (0.15, -0.48)
    ]

    coords = []
    for px, py in points:
        coords.extend([cx + px * size, cy + py * size])

    canvas.create_polygon(
        coords, smooth=True,
        fill="#ff174f", outline="#ff8aa6", width=2
    )

    # Блик на сердце
    canvas.create_oval(
        cx - size * 0.30, cy - size * 0.32,
        cx - size * 0.17, cy - size * 0.19,
        fill="#ffd6e0", outline=""
    )


def animate():
    global frame
    frame += 1

    draw_background()

    # Цикл: закрытие -> открытие -> сердце -> повтор
    cycle = frame % 300

    if cycle < 35:
        opening = 0
    elif cycle < 85:
        opening = (cycle - 35) / 50
    elif cycle < 245:
        opening = 1
    elif cycle < 265:
        opening = 1 - (cycle - 245) / 20
    else:
        opening = 0

    opening = max(0, min(1, opening))

    # Глаза
    draw_eye(315, 250, opening)
    draw_eye(585, 250, opening)

    # Сердце появляется после открытия глаз
    if cycle >= 65 and cycle < 245:
        pulse = 1 + 0.10 * math.sin(frame * 0.16)
        size = 105 * pulse * min(1, (cycle - 65) / 20)

        draw_heart(450, 390, size)

    # Подпись
    canvas.create_text(
        WIDTH // 2, 525,
        text="E Y E S   &   H E A R T",
        fill="#d6e6e0",
        font=("Consolas", 16, "bold")
    )

    canvas.create_text(
        WIDTH // 2, 555,
        text="♡  made with Python  ♡",
        fill="#ff6385",
        font=("Consolas", 11)
    )

    root.after(40, animate)


animate()
root.mainloop()
