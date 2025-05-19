def pokemon(name):
    # Importamos la biblioteca necesaria para hacer solicitudes HTTP
    import requests
    
    # Definimos la URL base de la PokeAPI
    URL = "https://pokeapi.co/api/v2/pokemon/"
    
    # Hacemos una solicitud GET para obtener los datos del Pokémon por nombre
    response = requests.get(URL + name)
    
    # Convertimos la respuesta en formato JSON a un diccionario de Python
    datos = response.json()
    
    # Mostramos el contenido del Pokémon solicitado
    print(datos)

def prueba():
    # Importamos las bibliotecas necesarias para solicitudes y manipulación de datos
    import requests
    import pandas as pd
    import numpy as np

    # URL base para acceder a los datos de los Pokémon
    URL2 = "https://pokeapi.co/api/v2/pokemon/"
    
    # Lista donde almacenaremos los datos de todos los Pokémon
    pokemon_data = []

    # Recorremos los primeros 151 Pokémon (de la Pokédex original)
    for i in range(1, 152):
        # Hacemos la solicitud para cada Pokémon por ID
        response = requests.get(URL2 + str(i))
        
        # Verificamos que la respuesta fue exitosa (código 200)
        if response.status_code == 200:
            # Convertimos la respuesta a formato JSON
            data = response.json()

            # Obtenemos los tipos del Pokémon (puede tener uno o dos)
            types_list = []
            for t in data["types"]:
                types_list.append(t["type"]["name"])
            types = ", ".join(types_list)  # Unimos los tipos en un string separados por coma

            # Obtenemos las habilidades del Pokémon
            abilities_list = []
            for a in data["abilities"]:
                abilities_list.append(a["ability"]["name"])
            abilities = ", ".join(abilities_list)  # Unimos habilidades en un string separados por coma

            # Obtenemos las estadísticas base del Pokémon (hp, ataque, defensa, etc.)
            stats_dict = {}
            for stat in data["stats"]:
                stat_name = stat["stat"]["name"]
                base_stat = stat["base_stat"]
                stats_dict[stat_name] = base_stat  # Guardamos cada estadística por su nombre

            # Obtener ubicaciones donde se puede encontrar el Pokémon
            location_url = data["location_area_encounters"]
            encounter_response = requests.get(location_url)

            # Si la respuesta fue exitosa, extraemos los nombres de las ubicaciones
            if encounter_response.status_code == 200:
                locations_data = encounter_response.json()
                locations = []
                for loc in locations_data:
                    location_name = loc["location_area"]["name"]
                    locations.append(location_name)
                location_names = ", ".join(locations)  # Unimos los nombres de ubicación
            else:
                location_names = "No disponible"  # Si falla la solicitud, indicamos que no está disponible

            # Creamos un diccionario con todos los datos relevantes del Pokémon
            pokemon_info = {
                "id": data["id"],
                "name": data["name"],
                "base_experience": data["base_experience"],
                "height": data["height"],
                "weight": data["weight"],
                "order": data["order"],
                "default": data["is_default"],
                "location_area_encounters": location_names,
                "types": types,
                "abilities": abilities,
                "hp": stats_dict.get("hp"),
                "attack": stats_dict.get("attack"),
                "defense": stats_dict.get("defense"),
                "special-attack": stats_dict.get("special-attack"),
                "special-defense": stats_dict.get("special-defense"),
                "speed": stats_dict.get("speed")
            }

            # Agregamos el diccionario a la lista de datos
            pokemon_data.append(pokemon_info)
        else:
            # Si no se pudo obtener el Pokémon, mostramos un error
            print("Error de la extracción de datos")

    # Convertimos la lista de diccionarios a un DataFrame de pandas
    df = pd.DataFrame(pokemon_data)
    
    # Mostramos las primeras 5 filas del DataFrame
    return df

def guardar_pokemon_json(df, filename='pokemon.json', folder='data'):
    import json
    import os
    import pandas as pd
    """
    Guarda un DataFrame de Pokémon como archivo JSON dentro de la carpeta especificada.

    Parámetros:
    - df: DataFrame con la información de los Pokémon.
    - filename: Nombre del archivo donde se guardará el JSON (por defecto: 'pokemon.json').
    - folder: Carpeta donde se guardará el archivo (por defecto: 'datos').
    """
    # Crear la ruta completa al archivo
    if not os.path.exists(folder):
        os.makedirs(folder)  # Crea la carpeta si no existe, solo por precaución

    filepath = os.path.join(folder, filename)

    # Convertir el DataFrame a una lista de diccionarios
    pokemon_dict = df.to_dict(orient='records')

    # Guardamos el JSON en el archivo
    if isinstance(pokemon_dict, list):
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(pokemon_dict, file, ensure_ascii=False, indent=4)
        print(f"Archivo guardado correctamente en {filepath}")
    else:
        print("Error: El DataFrame no pudo convertirse a una lista de diccionarios.")