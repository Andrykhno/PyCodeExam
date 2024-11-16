def button_create(new_x, new_y, action):
    """Создает круглую кнопку на холсте по координатам и задает действие."""
    button_radius = 50
    # Рисуем круг
    button_id = canvas.create_oval(
        new_x - button_radius, 
        new_y - button_radius, 
        new_x + button_radius, 
        new_y + button_radius, 
        fill="#d3d3d3", 
        outline="#404040", 
        width=2
    )

    # Привязываем действие к кругу
    def on_circle_click(event):
        if (event.x - new_x) ** 2 + (event.y - new_y) ** 2 <= button_radius ** 2:
            action()

    canvas.tag_bind(button_id, "<Button-1>", on_circle_click)