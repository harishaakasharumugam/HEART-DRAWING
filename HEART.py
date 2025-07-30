import tkinter as tk
from tkinter import colorchooser, ttk
import turtle
import threading
import time
import colorsys

def draw_heart_in_canvas(canvas, color, size, animation_type):
    canvas.delete("all")

    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("white")
    screen.tracer(0)

    t = turtle.RawTurtle(screen)
    t.shape("arrow")
    t.color(color)
    t.pensize(2)
    t.speed(0)

    def slow_forward(distance, step=2, delay=0.01):
        moved = 0
        while moved < distance:
            t.forward(min(step, distance - moved))
            moved += step
            screen.update()
            time.sleep(delay)

    def slow_circle(radius, extent, step=2, delay=0.01):
        steps = int(abs(extent) / step)
        for _ in range(steps):
            t.circle(radius, step if extent > 0 else -step)
            screen.update()
            time.sleep(delay)

    def get_heart_center(size):
        if size <= 1.5:
            return 0, -50
        else:
            return 0, -150

    def draw_heart(scale):
        x, y = get_heart_center(scale)
        t.penup()
        t.goto(x, y)
        t.setheading(140)
        t.pendown()
        t.begin_fill()

        slow_forward(1.8 * 70 * scale)
        slow_circle(-90 * scale * 0.7, 200)
        t.setheading(60)
        slow_circle(-90 * scale * 0.7, 200)
        slow_forward(1.8 * 70 * scale)

        t.end_fill()
        t.hideturtle()
        screen.update()

    def pulse_animation():
        for i in range(2):
            s = size * (1 + 0.1 * (i % 2))
            t.clear()
            draw_heart(s)
            time.sleep(0.1)

    def fade_animation():
        # Convert hex color to RGB (0-1)
        def hex_to_rgb_normalized(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))

        # Convert RGB (0-1) back to hex
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % tuple(int(max(0, min(1, c)) * 255) for c in rgb)

        base_rgb = hex_to_rgb_normalized(color)
        h, l, s = colorsys.rgb_to_hls(*base_rgb)

        # Create lightness steps from current to near white (e.g., l -> 0.9)
        steps = 3
        for i in range(steps):
            t.clear()
            # Gradually increase lightness (up to 0.9 max)
            new_l = l + (0.9 - l) * (i / (steps - 1))
            new_rgb = colorsys.hls_to_rgb(h, new_l, s)
            new_hex = rgb_to_hex(new_rgb)
            t.color(new_hex)
            draw_heart(size)
            time.sleep(0.5)


    if animation_type == "Pulse":
        pulse_animation()
    elif animation_type == "Fade":
        fade_animation()
    else:
        draw_heart(size)

def start_drawing():
    color = selected_color.get()
    size = size_var.get()
    animation = animation_var.get()

    threading.Thread(
        target=draw_heart_in_canvas,
        args=(turtle_canvas, color, size, animation),
        daemon=True
    ).start()

def pick_color():
    color_code = colorchooser.askcolor(title="Choose Heart Color")[1]
    if color_code:
        selected_color.set(color_code)
        color_display.config(bg=color_code)

def clear_canvas():
    turtle_canvas.delete("all")

# GUI setup
root = tk.Tk()
root.title("Turtle Heart Drawer")
root.geometry("600x400")
root.configure(bg="white")

selected_color = tk.StringVar(value="#FF0000")
size_var = tk.DoubleVar(value=1.0)
animation_var = tk.StringVar(value="None")

# Control panel
control_frame = tk.Frame(root, bg="white")
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

tk.Label(control_frame, text="HEART GENERATOR", font=("Helvetica", 16, "bold"), bg="white", fg="red").pack(pady=10)

tk.Label(control_frame, text="Choose Color:", bg="white", font=("Arial", 12)).pack(pady=5)
color_display = tk.Label(control_frame, bg=selected_color.get(), width=10, height=2)
color_display.pack(pady=5)
tk.Button(control_frame, text="Pick Color", command=pick_color).pack(pady=5)

tk.Label(control_frame, text="Size:", bg="white", font=("Arial", 12)).pack(pady=10)
tk.Scale(control_frame, from_=0.5, to=2.0, resolution=0.1, variable=size_var, orient=tk.HORIZONTAL, length=180).pack()

tk.Label(control_frame, text="Animation Type:", bg="white", font=("Arial", 12)).pack(pady=10)
ttk.Combobox(control_frame, textvariable=animation_var, values=["None", "Pulse", "Fade"], state="readonly").pack(pady=5)

tk.Button(control_frame, text="Generate", command=start_drawing, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
tk.Button(control_frame, text="Clear", command=clear_canvas, bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# Turtle canvas
canvas_frame = tk.Frame(root, bg="black", width=1000)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

turtle_canvas = tk.Canvas(canvas_frame, width=1000)
turtle_canvas.pack(fill=tk.BOTH, expand=True)

# Sync canvas height dynamically to match control_frame height
def sync_canvas_height(event=None):
    control_height = control_frame.winfo_height()
    canvas_frame.config(height=control_height)
    turtle_canvas.config(height=control_height)

root.bind("<Configure>", sync_canvas_height)

root.mainloop()
