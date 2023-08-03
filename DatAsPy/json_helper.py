import json
import numpy as np
import matplotlib.pyplot as plt

def generar_info_guardar_json(reduced_image_data, cell_size):
    # Obtener las dimensiones de la imagen reducida
    height, width = reduced_image_data.shape

    # Crear una lista para almacenar la información de las celdas
    cell_info_list = []

    # Dividir la imagen en celdas y asignar nombres siguiendo el patrón de cuadrados de ajedrez
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cell_data = reduced_image_data[y:y + cell_size, x:x + cell_size].tolist()  # Convertir a lista para guardar en JSON
            cell_name = f"{chr(x // cell_size + 97)}{y // cell_size + 1}"
            cell_info = {
                'name': cell_name,
                'x': x,
                'y': y,
                'data': cell_data
            }
            cell_info_list.append(cell_info)

    # Guardar la información de las celdas en un archivo JSON
    with open('cell_info.json', 'w') as jsonfile:
        json.dump(cell_info_list, jsonfile)


def calcular_metrica_ordenar_celdas():
    # Leer la información de las celdas desde el archivo JSON
    with open('cell_info.json', 'r') as jsonfile:
        cell_info_list = json.load(jsonfile)

    # Calcular la métrica de diferencia de contrastes para cada celda (en este caso, la desviación estándar)
    for cell_info in cell_info_list:
        cell_data = np.asarray(cell_info['data'], dtype=np.float32)  # Convertir a una matriz numérica
        cell_data = cell_data[np.isfinite(cell_data)]  # Filtrar valores no numéricos
        contrast_metric = np.std(cell_data)  # Calcular la desviación estándar de los valores de píxeles dentro de la celda
        cell_info['contrast_metric'] = contrast_metric

    # Ordenar la lista de celdas según la métrica de diferencia de contrastes en orden descendente
    cell_info_list.sort(key=lambda x: x['contrast_metric'], reverse=True)
    return cell_info_list

def mostrar_celdas_mayor_contraste(cell_info_list, N):
    # Seleccionar las N celdas con mayor diferencia de contrastes
    cells_of_interest = cell_info_list[:N]

    for cell_info in cells_of_interest:
        print(f"Celda {cell_info['name']} - Contraste: {cell_info['contrast_metric']}")

        # Obtener las coordenadas x e y de la celda
        x = cell_info['x']
        y = cell_info['y']

        # Obtener los datos de la celda de la imagen reducida
        cell_data = np.asarray(cell_info['data'], dtype=np.float32)

        # Visualizar la celda seleccionada en una nueva figura
        plt.figure()
        plt.imshow(cell_data, cmap='gray')
        plt.title(f"Celda {cell_info['name']} - Contraste: {cell_info['contrast_metric']}")
        plt.axis('off')
        plt.show()