from PIL import Image
import cv2
import random
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os


def augment_image(image):
    augmented_images = []

    for i in range(2):
        # Rotación
        angle = random.randint(-45, 45)
        rotated_image = image.rotate(angle)

        # Cambio de tamaño
        scale = random.uniform(0.5, 2)
        width, height = image.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = image.resize((new_width, new_height))

        # Cambio de iluminación
        brightness = random.randint(-50, 50)
        contrast = random.uniform(0.5, 1.5)
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        adjusted_image = cv2.convertScaleAbs(
            img_array, beta=brightness, alpha=contrast)
        adjusted_image = Image.fromarray(
            cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB))

        # Recorte
        crop_x1 = random.randint(0, int(width/6))
        crop_y1 = random.randint(0, int(height/6))
        crop_x2 = random.randint(int(width/2), width)
        crop_y2 = random.randint(int(height/2), height)
        cropped_image = image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

        # Espejo
        mirrored_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
        image = mirrored_image

        # Agregar cada imagen resultante a la lista de imágenes aumentadas
        augmented_images.extend(
            [rotated_image, resized_image, adjusted_image, mirrored_image, cropped_image])

    # Devolver la lista con todas las imágenes aumentadas
    return augmented_images


# Seleccionar las imágenes a procesar
root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title='Seleccionar imágenes', filetypes=[
                                         ('Imágenes', '*.jpg;*.jpeg;*.png')])

# Procesar cada imagen seleccionada
for file_path in file_paths:
    # Cargar la imagen original
    img = Image.open(file_path)

    # Pedir al usuario la base del nombre de las imágenes resultantes
    name_base = input(
        "Introduce el nombre base para las imágenes aumentadas: ")

    # Obtener la ruta y extensión de la imagen original
    file_dir, file_name = os.path.split(file_path)
    file_base, file_extension = os.path.splitext(file_name)

    # Aumentar la imagen y guardar todas las imágenes resultantes
    augmented_images = augment_image(img)
    for i, image in enumerate(augmented_images):
        file_name = f'{name_base}_{i}{file_extension}'
        file_path_out = os.path.join(file_dir, file_name)
        image.save(file_path_out)
