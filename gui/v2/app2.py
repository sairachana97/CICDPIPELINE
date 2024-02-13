

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/SER517-FALL23-TEAM4/gui/v2/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("2880x1800")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1800,
    width = 2880,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    2880.0,
    1800.0,
    fill="#0D1D3D",
    outline="")

canvas.create_text(
    77.0,
    462.0,
    anchor="nw",
    text="Model Training",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 55 * -1)
)

canvas.create_rectangle(
    520.0,
    20.0,
    2880.0,
    1800.0,
    fill="#F4F7FC",
    outline="")

canvas.create_text(
    610.0,
    513.0,
    anchor="nw",
    text="Preview",
    fill="#000000",
    font=("RobotoRoman Regular", 36 * -1)
)

canvas.create_rectangle(
    913.0,
    298.0,
    2133.0,
    408.0,
    fill="#000000",
    outline="")

canvas.create_text(
    57.0,
    96.0,
    anchor="nw",
    text="Vinci",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 90 * -1)
)

canvas.create_text(
    610.0,
    337.0,
    anchor="nw",
    text="Dataset:",
    fill="#000000",
    font=("RobotoRoman Regular", 36 * -1)
)

canvas.create_rectangle(
    554.0,
    591.0,
    2838.0,
    1746.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    77.0,
    344.0,
    anchor="nw",
    text="Datasets",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 55 * -1)
)

canvas.create_text(
    77.0,
    580.0,
    anchor="nw",
    text="Risk",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 55 * -1)
)

canvas.create_text(
    77.0,
    698.0,
    anchor="nw",
    text="Predictions",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 55 * -1)
)

canvas.create_text(
    77.0,
    816.0,
    anchor="nw",
    text="Help",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 55 * -1)
)
window.resizable(False, False)
window.mainloop()
