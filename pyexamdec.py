import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageSequence

is_blurred = False
button_id = None

def on_button_click():
    print("Круглая кнопка нажата!")

def blur_background():
    global is_blurred
    if not is_blurred:
        canvas.itemconfig(background_id, image=blurred_photo)
        canvas.delete(button_id)
        is_blurred = True

def unblur_background(event=None):
    global is_blurred, button_id
    if is_blurred:
        canvas.itemconfig(background_id, image=original_photo)
        restore_button()
        is_blurred = False

def restore_button():
    global button_id
    if button_id is None:
        button_id = canvas.create_image(800, 750, image=button_photo, anchor=tk.CENTER)

def create_start_screen():
    start_screen = tk.Frame(root, bg="#d3d3d3")
    start_screen.pack(fill="both", expand=True)

    start_button = tk.Button(
        start_screen, 
        text="Start Game", 
        font=("Arial", 20), 
        bg="#404040", 
        fg="white", 
        width=20, 
        command=lambda: start_game(start_screen)
    )
    start_button.pack(pady=20)

    quit_button = tk.Button(
        start_screen, 
        text="Quit", 
        font=("Arial", 20), 
        bg="#404040", 
        fg="white", 
        width=20, 
        command=root.quit
    )
    quit_button.pack(pady=20)

def start_game(start_screen):
    print("Нажата кнопка: Start Game")
    start_screen.pack_forget()
    canvas.pack(fill="both", expand=True)
    restore_button()

def button_create(new_x, new_y, action):
    """Создает полупрозрачную круглую кнопку с полупрозрачной обводкой."""
    button_radius = 50
    # Рисуем круг с полупрозрачной заливкой и обводкой
    button_id = canvas.create_oval(
        new_x - button_radius,
        new_y - button_radius,
        new_x + button_radius,
        new_y + button_radius,
        fill="#a0a0a0", 
        outline="#505050",  
        width=3  
    )

def show_photo():
    print("Фото будет показано")

def on_circle_click(event):
    if (event.x - new_x) ** 2 + (event.y - new_y) ** 2 <= button_radius ** 2:
        action()
    canvas.tag_bind(button_id, "<Button-1>", on_circle_click)

root = tk.Tk()
root.geometry("1500x1000")

image1 = Image.open("/Users/andriiprykhno/Desktop/PyCodeExam/photo/ill1.png")
computer_image = Image.open("/Users/andriiprykhno/Desktop/PyCodeExam/photo/ill3.png")
gif_path = "/Users/andriiprykhno/Desktop/PyCodeExam/photo/firstanimaation.gif"

gif = Image.open(gif_path)
gif_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

photo_paths = [
    "/Users/andriiprykhno/Desktop/PyCodeExam/photo/animpho1.png",
    "/Users/andriiprykhno/Desktop/PyCodeExam/photo/animpho2.png",
    "/Users/andriiprykhno/Desktop/PyCodeExam/photo/animpho3.png",
    "/Users/andriiprykhno/Desktop/PyCodeExam/photo/animpho4.png",
]

photo_images = [ImageTk.PhotoImage(Image.open(path)) for path in photo_paths]
current_photo_index = 0

blurred_image = image1.filter(ImageFilter.GaussianBlur(10))
original_photo = ImageTk.PhotoImage(image1)
blurred_photo = ImageTk.PhotoImage(blurred_image)

canvas = tk.Canvas(root, width=1500, height=1000)
background_id = canvas.create_image(0, 0, anchor=tk.NW, image=original_photo)


button_create(750, 500, show_photo)

create_start_screen()
root.mainloop()