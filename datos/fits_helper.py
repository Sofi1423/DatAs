from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np


def generar_info_guardar_csv(nombre_archivo_fits):
    # Colocar archivo FITS indicando el nombre
    with fits.open(nombre_archivo_fits) as archivo_fits:
        # Extraer los datos de la primera extensión (extensión 0) de la imagen FITS
        datos_imagen = archivo_fits[0].data
        archivo_fits.close()

    print(datos_imagen)


def visualizar_y_dividir_imagen(datos_imagen, divisiones):
    # Obtener el tamaño de la imagen
    height, width = datos_imagen.shape

    # Calcular el tamaño de las celdas
    cell_size_y = height // divisiones
    cell_size_x = width // divisiones

    # Lista para almacenar la información de las celdas
    celdas_info = []

    # Visualizar la imagen con divisiones y etiquetas
    plt.imshow(datos_imagen, cmap='gray')

    # Deshabilitar los ejes del gráfico
    plt.axis('off')

    # Dividir la imagen en celdas y asignar nombres siguiendo el patrón de cuadrados de ajedrez para mejor orientación
    for y in range(0, height, cell_size_y):
        for x in range(0, width, cell_size_x):
            cell_data = datos_imagen[y:y + cell_size_y, x:x + cell_size_x]
            cell_name = f"{chr(x // cell_size_x + 97)}{y // cell_size_y + 1}"  # Usamos las letras a, b, c, ... y los números 1, 2, 3, ... como nombres
            celdas_info.append((cell_name, x, y, x + cell_size_x, y + cell_size_y))

            # Dibujamos las líneas de los bordes de las celdas
            plt.plot([x, x + cell_size_x, x + cell_size_x, x, x], [y, y, y + cell_size_y, y + cell_size_y, y], color='red')

            # Mostrar el nombre de la celda en el centro
            plt.text(x + cell_size_x // 2, y + cell_size_y // 2, cell_name, color='red', fontsize=6, ha='center', va='center')

    plt.show()
    return celdas_info

def visualizar_y_dividir_reduccion(datos_imagen, divisiones):
    # Reducir la imagen
    reduced_image_data = datos_imagen[::2, ::2]

    # Tamaño de celda para la imagen reducida
    cell_size = min(reduced_image_data.shape) // divisiones

    # Obtener las dimensiones de la imagen reducida
    height, width = reduced_image_data.shape

    # Calcular el número de celdas en filas y columnas
    num_cells_x = width // cell_size
    num_cells_y = height // cell_size

    # Ajustar num_cells_x y num_cells_y si no están completamente llenos
    if width % cell_size != 0:
        num_cells_x += 1
    if height % cell_size != 0:
        num_cells_y += 1

    # Configurar la figura principal para ocupar toda la pantalla sin bordes blancos
    fig = plt.figure(figsize=(num_cells_x, num_cells_y + 1), dpi=100)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

    # Visualizar la imagen completa sin los números y ejes de tipo gráfico
    ax_image = plt.subplot(1, 1, 1)
    ax_image.imshow(reduced_image_data, cmap='gray', extent=[0, width, 0, height])
    ax_image.axis('off')

    # Lista para almacenar la información de las celdas
    celdas_info = []

    # Dividir la imagen en celdas y asignar nombres siguiendo el patrón de cuadrados de ajedrez
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cell_data = reduced_image_data[y:y + cell_size, x:x + cell_size]
            cell_name = f"{chr(x // cell_size + 97)}{y // cell_size + 1}"  # Usamos las letras a, b, c, ... y los números 1, 2, 3, ... como nombres
            celdas_info.append((cell_name, x, y, x + cell_size, y + cell_size))

            ax_cell = plt.subplot(num_cells_y, num_cells_x, (y // cell_size) * num_cells_x + (x // cell_size) + 1)
            ax_cell.imshow(cell_data, cmap='gray', extent=[x, x + cell_size, y, y + cell_size])
            ax_cell.text(x + cell_size // 2, y + cell_size // 2, cell_name, color='red', fontsize=6, ha='center', va='center')
            ax_cell.axis('off')

    plt.show()
    return celdas_info, reduced_image_data