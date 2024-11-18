import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageSequence

is_blurred = False
button_id = None
button_photo = None

def on_button_click():
    print("Круглая кнопка нажата!")
    blur_background()

def blur_background():
    global is_blurred, button_id
    print("Размытие фона...")
    if not is_blurred:
        canvas.itemconfig(background_id, image=blurred_photo)
        if button_id is not None:
            canvas.delete(button_id)
            button_id = None
        is_blurred = True

def unblur_background(event=None):
    global is_blurred, button_id
    print("Снятие размытия...")
    if is_blurred:
        canvas.itemconfig(background_id, image=original_photo)
        create_button(750, 500, on_button_click)
        is_blurred = False

def create_button(new_x, new_y, action):
    global button_id, button_photo
    button_radius = 50

    if button_photo is None:
        button_image = Image.new("RGBA", (button_radius * 4, button_radius * 4), (0, 0, 0, 0))
        draw = ImageDraw.Draw(button_image)
        draw.ellipse(
            (0, 0, button_radius * 4 - 1, button_radius * 4 - 1),
            fill=(211, 211, 211, 178),
            outline=(80, 80, 80, 178),
            width=4
        )
        button_image = button_image.resize((button_radius * 2, button_radius * 2), Image.LANCZOS)
        button_photo = ImageTk.PhotoImage(button_image)

    if button_id is None:
        print("Создание кнопки...")
        button_id = canvas.create_image(new_x, new_y, image=button_photo, anchor=tk.CENTER)

        def on_circle_click(event):
            if (event.x - new_x) ** 2 + (event.y - new_y) ** 2 <= button_radius ** 2:
                action()

        canvas.tag_bind(button_id, "<Button-1>", on_circle_click)

def start_photo_sequence():
    print("Показ фотографий...")
    animation_label.pack_forget()
    canvas.pack(fill="both", expand=True)
    root.bind("<Key>", show_next_photo)
    root.bind("<Button-1>", show_next_photo)
    show_next_photo()

def show_next_photo(event=None):
    global current_photo_index
    canvas.delete("all")
    if current_photo_index < len(photo_images):
        print(f"Показ фото: {current_photo_index}")
        next_photo = photo_images[current_photo_index]
        canvas.create_image(0, 0, anchor=tk.NW, image=next_photo)
        current_photo_index += 1
    else:
        show_main_screen()

def show_main_screen():
    print("Переход на основной экран...")
    global button_id
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=original_photo)
    button_id = None
    create_button(750, 500, on_button_click)

def start_animation():
    menu_frame.pack_forget()  # Скрываем начальный экран
    animation_label.pack(fill="both", expand=True)  # Показываем анимацию
    play_animation()

def play_animation():
    def update(index):
        frame = gif_frames[index]
        animation_label.configure(image=frame)
        index += 1
        if index == len(gif_frames):
            start_photo_sequence()  # Переход к последовательности фотографий
        else:
            root.after(500, update, index)  # Задержка между кадрами (200 мс)

    update(0)

root = tk.Tk()
root.geometry("1500x1000")

image1 = Image.open("/Users/andriiprykhno/Desktop/PyCodeExam/photo/ill1.png")
computer_image = Image.open("/Users/andriiprykhno/Desktop/PyCodeExam/photo/ill3.png")
gif_path = "/Users/andriiprykhno/Desktop/PyCodeExam/photo/firstanimaation.gif"

blurred_image = image1.filter(ImageFilter.GaussianBlur(10))
original_photo = ImageTk.PhotoImage(image1)
blurred_photo = ImageTk.PhotoImage(blurred_image)

canvas = tk.Canvas(root, width=1500, height=1000)
background_id = canvas.create_image(0, 0, anchor=tk.NW, image=original_photo)

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

menu_frame = tk.Frame(root, bg="#d3d3d3")
menu_frame.pack(fill="both", expand=True)

start_button = tk.Button(menu_frame, text="Начать играть", command=start_animation)
start_button.pack(pady=20)

exit_button = tk.Button(menu_frame, text="Выход", command=root.quit)
exit_button.pack(pady=20)

animation_label = tk.Label(root)
root.bind("<Escape>", unblur_background)
root.mainloop()