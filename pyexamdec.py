import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageSequence

def blur_background():
    global is_blured
    if not is_blurred:
        canvas.itemconfig(background_id, image=blurred_photo)
        canvas.delete(button_id)  # Удаляем кнопку после нажатия
        add_computer_image()  # Добавляем новое изображение
        is_blurred = True

def unblur_background(event=None):
    """Функция для снятия размытия с фона и возврата кнопки."""
    global is_blurred, button_id
    if is_blurred:  # Проверяем, если фон размыт
        canvas.itemconfig(background_id, image=original_photo)
        restore_button()  # Восстанавливаем кнопку
        is_blurred = False

root = tk.Tk()
root.geometry("1500x1000")

image1 = Image.open("/Users/andriiprykhno/Desktop/photo/ill1.png")  # Основной фон
computer_image = Image.open("/Users/andriiprykhno/Desktop/photo/ill3.png")
gif_path = "/Users/andriiprykhno/Desktop/photo/firstanimaation.gif"  # Анимация GIF

gif = Image.open(gif_path)
gif_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

photo_paths = [
    "/Users/andriiprykhno/Desktop/photo/animpho1.png",
    "/Users/andriiprykhno/Desktop/photo/animpho2.png",
    "/Users/andriiprykhno/Desktop/photo/animpho3.png",
    "/Users/andriiprykhno/Desktop/photo/animpho4.png",
]

photo_images = [ImageTk.PhotoImage(Image.open(path)) for path in photo_paths]
current_photo_index = 0