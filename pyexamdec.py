import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageSequence

is_blurred = False
button_id = None
button_photo = None

def on_button_click():
    print("Круглая кнопка нажата!")

def blur_background():
    global is_blurred
    if not is_blurred:
        canvas.itemconfig(background_id, image=blurred_photo)
        canvas.delete(button_id)
        is_blurred = True

def unblur_background(event=None):
    global is_blurred
    if is_blurred:
        canvas.itemconfig(background_id, image=original_photo)
        create_or_restore_button(800, 750, on_button_click)
        is_blurred = False

def create_or_restore_button(new_x, new_y, action):
    global button_id, button_photo
    button_radius = 50

    if button_photo is None:
        button_image = Image.new("RGBA", (button_radius * 4, button_radius * 4), (0, 0, 0, 0))
        draw = ImageDraw.Draw(button_image)
        draw.ellipse(
            (0, 0, button_radius * 4 - 1, button_radius * 4 - 1),
            fill=(211, 211, 211, 77),
            outline=(80, 80, 80, 100),
            width=4
        )
        button_image = button_image.resize((button_radius * 2, button_radius * 2), Image.LANCZOS)
        button_photo = ImageTk.PhotoImage(button_image)

    if button_id is None:
        button_id = canvas.create_image(new_x, new_y, image=button_photo, anchor=tk.CENTER)

        def on_circle_click(event):
            if (event.x - new_x) ** 2 + (event.y - new_y) ** 2 <= button_radius ** 2:
                action()

        canvas.tag_bind(button_id, "<Button-1>", on_circle_click)

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
    create_or_restore_button(800, 750, on_button_click)

def show_photo():
    print("Фото будет показано!")

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

create_start_screen()
root.bind("<Escape>", unblur_background)
root.mainloop()