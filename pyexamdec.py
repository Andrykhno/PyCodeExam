import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageSequence

def blur_background(): #что бы блюрить что либо когда ты открываешь что-то на первом слое
    global is_blured
    if not is_blurred:
        canvas.itemconfig(background_id, image=blurred_photo)
        canvas.delete(button_id)  # Удаляем кнопку после нажатия
        add_computer_image()  # Добавляем новое изображение
        is_blurred = True

def unblur_background(event=None): #что бы убирать блюр
    """Функция для снятия размытия с фона и возврата кнопки."""
    global is_blurred, button_id
    if is_blurred:  # Проверяем, если фон размыт
        canvas.itemconfig(background_id, image=original_photo)
        restore_button()  # Восстанавливаем кнопку
        is_blurred = False

def create_start_screen():
    # Создаем Frame для начального экрана
    start_screen = tk.Frame(root, bg="#d3d3d3")
    start_screen.pack(fill="both", expand=True)

    # Кнопка "Start Game"
    start_button = tk.Button(
        start_screen, 
        text="Start Game", 
        font=("Arial", 16), 
        bg="#404040", 
        fg="white", 
        width=20, 
        command=lambda: start_game(start_screen)
    )
    start_button.pack(pady=20)
    quit_button = tk.Button(
        start_screen, 
        text="Quit", 
        font=("Arial", 16), 
        bg="#404040", 
        fg="white", 
        width=20, 
        
    )



root = tk.Tk()
root.geometry("1500x1000")

image1 = Image.open("/Users/andriiprykhno/Desktop/photo/ill1.png")  # Основной фон
computer_image = Image.open("/Users/andriiprykhno/Desktop/photo/ill3.png") # картинка экрана компьютера 
gif_path = "/Users/andriiprykhno/Desktop/photo/firstanimaation.gif"  # Анимация GIF

gif = Image.open(gif_path)
gif_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

photo_paths_boscall = [ #путь к фото после гифки
    "/Users/andriiprykhno/Desktop/photo/animpho1.png",
    "/Users/andriiprykhno/Desktop/photo/animpho2.png",
    "/Users/andriiprykhno/Desktop/photo/animpho3.png",
    "/Users/andriiprykhno/Desktop/photo/animpho4.png",
]

photo_images = [ImageTk.PhotoImage(Image.open(path)) for path in photo_paths]
current_photo_index = 0

root.mainloop()