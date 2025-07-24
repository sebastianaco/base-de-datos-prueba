from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# --- Configuración de Conexión a MongoDB ---
# IMPORTANTE: Reemplaza esta URI con la de tu cluster de MongoDB Atlas si lo usas.
# Si es local, probablemente sea 'mongodb://localhost:27017/'
MONGO_URI = "mongodb+srv://felipepoblete:Monster@cluster.niexarr.mongodb.net/" # Ejemplo para Atlas: "mongodb+srv://<user>:<password>@clustername.mongodb.net/mi_base_alimentos?retryWrites=true&w=majority"
DB_NAME = "mi_base_alimentos" # Nombre de la base de datos que creaste/usarás
COLLECTION_NAME = "alimentos" # Nombre de la colección que creaste/usarás

# --- Funciones de Utilidad ---
def get_collection():
    """Establece la conexión a MongoDB y devuelve la colección."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print(f"Conexión exitosa a la colección '{COLLECTION_NAME}' en la base de datos '{DB_NAME}'.")
        return collection
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

# --- Operaciones CRUD ---

# 1. CREATE (Creación de nuevos documentos)
def crear_alimento(alimento):
    """Inserta un nuevo documento de alimento en la colección."""
    collection = get_collection()
    if collection is not None:
        try:
            if "fecha_creacion" not in alimento:
                alimento["fecha_creacion"] = datetime.now()
            result = collection.insert_one(alimento)
            print(f"Alimento '{alimento['nombre']}' insertado con ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"Error al insertar alimento: {e}")
    return None

def crear_varios_alimentos(alimentos_list):
    """Inserta múltiples documentos de alimentos en la colección."""
    collection = get_collection()
    if collection is not None:
        try:
            for alimento in alimentos_list:
                if "fecha_creacion" not in alimento:
                    alimento["fecha_creacion"] = datetime.now()
            result = collection.insert_many(alimentos_list)
            print(f"Insertados {len(result.inserted_ids)} alimentos.")
            return result.inserted_ids
        except Exception as e:
            print(f"Error al insertar varios alimentos: {e}")
    return None

# 2. READ (Lectura con filtros, operadores lógicos y estructuras anidadas)
def leer_todos_alimentos():
    """Lee y muestra todos los documentos de la colección."""
    collection = get_collection()
    if collection is not None:
        print("\n--- Todos los Alimentos ---")
        alimentos = list(collection.find())
        for alimento in alimentos:
            print(alimento)
        return alimentos
    return []

def buscar_por_nombre(nombre_alimento):
    """Busca y muestra un alimento por su nombre exacto."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Buscando alimento: {nombre_alimento} ---")
        alimento = collection.find_one({"nombre": nombre_alimento})
        if alimento:
            print(alimento)
            return alimento
        else:
            print(f"Alimento '{nombre_alimento}' no encontrado.")
    return None

def buscar_por_rango_calorias(min_calorias, max_calorias):
    """Busca alimentos con porciones dentro de un rango de calorías (Operador de comparación)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos con porciones entre {min_calorias} y {max_calorias} calorías ---")
        # $elemMatch asegura que 'calorias' dentro de *una misma* porción esté en el rango.
        query = {
            "porciones": {
                "$elemMatch": {
                    "calorias": {"$gte": min_calorias, "$lte": max_calorias}
                }
            }
        }
        alimentos_encontrados = list(collection.find(query))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print("No se encontraron alimentos en ese rango de calorías.")
        return alimentos_encontrados
    return []

def buscar_por_categoria_y_proyectar(categoria, campos_a_proyectar):
    """Busca alimentos por categoría y muestra solo los campos especificados (Proyección)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos en categoría '{categoria}' (solo {', '.join(campos_a_proyectar)}) ---")
        projection = {"_id": 0} # Excluir _id por defecto
        for campo in campos_a_proyectar:
            projection[campo] = 1 # Incluir los campos solicitados

        alimentos_encontrados = list(collection.find({"categoria": categoria}, projection))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print(f"No se encontraron alimentos en la categoría '{categoria}'.")
        return alimentos_encontrados
    return []

def buscar_alimentos_con_micronutriente(nombre_micronutriente):
    """Busca alimentos que contengan un micronutriente específico (Filtro en estructura anidada)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos con '{nombre_micronutriente}' ---")
        query = {"micronutrientes.nombre": nombre_micronutriente}
        alimentos_encontrados = list(collection.find(query))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print(f"No se encontraron alimentos con '{nombre_micronutriente}'.")
        return alimentos_encontrados
    return []

def buscar_por_alergenos(alergia):
    """Busca alimentos que contengan un alergeno específico (Filtro en array)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos que contienen el alergeno '{alergia}' ---")
        query = {"alergenos": alergia} # Busca si el valor existe en el array
        alimentos_encontrados = list(collection.find(query))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print(f"No se encontraron alimentos con el alergeno '{alergia}'.")
        return alimentos_encontrados
    return []


# 3. UPDATE (Actualización de documentos o campos internos)
def actualizar_calorias_por_nombre(nombre_alimento, nueva_caloria_por_unidad, unidad_porciones="unidad"):
    """Actualiza las calorías de una porción específica de un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Actualizando calorías de '{nombre_alimento}' (unidad: {unidad_porciones}) ---")
        result = collection.update_one(
            {"nombre": nombre_alimento, "porciones.unidad": unidad_porciones},
            {"$set": {"porciones.$[elem].calorias": nueva_caloria_por_unidad}},
            array_filters=[{"elem.unidad": unidad_porciones}]
        )
        if result.matched_count > 0:
            print(f"Alimento '{nombre_alimento}' actualizado. Documentos modificados: {result.modified_count}")
        else:
            print(f"Alimento '{nombre_alimento}' o unidad '{unidad_porciones}' no encontrado para actualizar.")
        return result

def agregar_o_actualizar_micronutriente(nombre_alimento, nombre_micronutriente, cantidad_mg):
    """Agrega o actualiza un micronutriente para un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Agregando/Actualizando '{nombre_micronutriente}' para '{nombre_alimento}' ---")
        # Intenta actualizar si el micronutriente ya existe
        result = collection.update_one(
            {"nombre": nombre_alimento, "micronutrientes.nombre": nombre_micronutriente},
            {"$set": {"micronutrientes.$.cantidad_mg": cantidad_mg}}
        )
        if result.matched_count > 0:
            print(f"Micronutriente '{nombre_micronutriente}' actualizado para '{nombre_alimento}'.")
        else:
            # Si no existe, lo agrega con $push
            result = collection.update_one(
                {"nombre": nombre_alimento},
                {"$push": {"micronutrientes": {"nombre": nombre_micronutriente, "cantidad_mg": cantidad_mg}}}
            )
            if result.matched_count > 0:
                print(f"Micronutriente '{nombre_micronutriente}' agregado a '{nombre_alimento}'.")
            else:
                print(f"Alimento '{nombre_alimento}' no encontrado para agregar/actualizar micronutriente.")
        return result

def actualizar_campo_directo(nombre_alimento, campo, nuevo_valor):
    """Actualiza un campo directo (no anidado ni array) de un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Actualizando '{campo}' de '{nombre_alimento}' a '{nuevo_valor}' ---")
        result = collection.update_one(
            {"nombre": nombre_alimento},
            {"$set": {campo: nuevo_valor}}
        )
        if result.matched_count > 0:
            print(f"Campo '{campo}' de '{nombre_alimento}' actualizado. Documentos modificados: {result.modified_count}")
        else:
            print(f"Alimento '{nombre_alimento}' no encontrado.")
        return result


# 4. DELETE (Eliminación controlada de registros)
def eliminar_alimento_por_nombre(nombre_alimento):
    """Elimina un alimento por su nombre."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Eliminando alimento: {nombre_alimento} ---")
        result = collection.delete_one({"nombre": nombre_alimento})
        if result.deleted_count > 0:
            print(f"Alimento '{nombre_alimento}' eliminado exitosamente.")
        else:
            print(f"Alimento '{nombre_alimento}' no encontrado para eliminar.")
        return result

def eliminar_alimentos_por_categoria(categoria):
    """Elimina todos los alimentos de una categoría específica."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Eliminando alimentos de la categoría: {categoria} ---")
        result = collection.delete_many({"categoria": categoria})
        if result.deleted_count > 0:
            print(f"Eliminados {result.deleted_count} alimentos de la categoría '{categoria}'.")
        else:
            print(f"No se encontraron alimentos en la categoría '{categoria}' para eliminar.")
        return result

def eliminar_micronutriente_de_alimento(nombre_alimento, nombre_micronutriente):
    """Elimina un micronutriente específico del array de un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Eliminando '{nombre_micronutriente}' de '{nombre_alimento}' ---")
        result = collection.update_one(
            {"nombre": nombre_alimento},
            {"$pull": {"micronutrientes": {"nombre": nombre_micronutriente}}}
        )
        if result.matched_count > 0 and result.modified_count > 0:
            print(f"Micronutriente '{nombre_micronutriente}' eliminado de '{nombre_alimento}'.")
        else:
            print(f"Alimento '{nombre_alimento}' o micronutriente '{nombre_micronutriente}' no encontrado.")
        return result

# --- Función de Menú Interactivo ---
def menu_interactivo_crud():
    """Muestra un menú interactivo para realizar operaciones CRUD."""
    while True:
        print("\n=== MENÚ DE OPERACIONES CRUD ===")
        print("1. Crear Nuevo Alimento")
        print("2. Buscar Alimentos (Read)")
        print("3. Actualizar Alimento")
        print("4. Eliminar Alimento")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1': # CREAR ALIMENTO
            print("\n--- Crear Nuevo Alimento ---")
            nombre = input("Nombre del alimento: ")
            categoria = input("Categoría (ej. Fruta, Proteína, Dulce): ")
            unidad_porcion = input("Unidad de porción (ej. unidad, 100g, taza): ")
            cantidad_porcion = float(input("Cantidad de la porción (número): "))
            gramos_porcion = float(input("Gramos de la porción: "))
            calorias_porcion = float(input("Calorías de la porción: "))
            proteinas = float(input("Proteínas (g): "))
            carbohidratos = float(input("Carbohidratos (g): "))
            grasas = float(input("Grasas (g): "))
            fibra = float(input("Fibra (g): "))
            azucar = float(input("Azúcar (g): "))
            alergenos_str = input("Alérgenos (separados por coma, ej. gluten,lactosa): ")
            alergenos = [a.strip() for a in alergenos_str.split(',') if a.strip()]

            nuevo_alimento_usuario = {
                "nombre": nombre,
                "categoria": categoria,
                "porciones": [{ "unidad": unidad_porcion, "cantidad": cantidad_porcion, "gramos": gramos_porcion, "calorias": calorias_porcion }],
                "macros": { "proteinas_g": proteinas, "carbohidratos_g": carbohidratos, "grasas_g": grasas },
                "micronutrientes": [], # Simplificado, podrías extender esto si el profe lo pide
                "fibra_g": fibra,
                "azucar_g": azucar,
                "alergenos": alergenos
            }
            crear_alimento(nuevo_alimento_usuario)

        elif opcion == '2': # BUSCAR ALIMENTOS (READ)
            print("\n--- Opciones de Búsqueda ---")
            print("1. Ver Todos los Alimentos (primeros 10)")
            print("2. Buscar por Nombre")
            print("3. Buscar por Rango de Calorías")
            print("4. Buscar por Categoría y Proyectar Campos")
            print("5. Buscar por Micronutriente")
            print("6. Buscar por Alérgeno")
            sub_opcion = input("Selecciona una opción de búsqueda: ")

            if sub_opcion == '1':
                collection_read_all = get_collection()
                if collection_read_all is not None:
                    print("\n--- Primeros 10 Alimentos ---")
                    for alimento in collection_read_all.find().limit(10):
                        print(alimento)
            elif sub_opcion == '2':
                nombre = input("Nombre del alimento a buscar: ")
                buscar_por_nombre(nombre)
            elif sub_opcion == '3':
                min_c = float(input("Calorías mínimas: "))
                max_c = float(input("Calorías máximas: "))
                buscar_por_rango_calorias(min_c, max_c)
            elif sub_opcion == '4':
                categoria = input("Categoría a buscar: ")
                campos_str = input("Campos a proyectar (separados por coma, ej. nombre,categoria): ")
                campos = [c.strip() for c in campos_str.split(',') if c.strip()]
                buscar_por_categoria_y_proyectar(categoria, campos)
            elif sub_opcion == '5':
                micro = input("Nombre del micronutriente a buscar: ")
                buscar_alimentos_con_micronutriente(micro)
            elif sub_opcion == '6':
                alergeno = input("Alérgeno a buscar: ")
                buscar_por_alergenos(alergeno)
            else:
                print("Opción de búsqueda no válida.")

        elif opcion == '3': # ACTUALIZAR ALIMENTO
            print("\n--- Actualizar Alimento ---")
            nombre_alimento = input("Nombre del alimento a actualizar: ")
            print("¿Qué quieres actualizar?")
            print("1. Calorías de una porción (ej. 'unidad')")
            print("2. Un campo directo (ej. 'categoria')")
            print("3. Agregar/Actualizar Micronutriente")
            update_opcion = input("Selecciona una opción de actualización: ")

            if update_opcion == '1':
                nueva_cal = float(input("Nueva cantidad de calorías para la porción 'unidad': "))
                actualizar_calorias_por_nombre(nombre_alimento, nueva_cal, "unidad")
            elif update_opcion == '2':
                campo = input("Nombre del campo directo a actualizar (ej. 'categoria', 'macros.grasas_g'): ")
                nuevo_valor_str = input(f"Nuevo valor para '{campo}': ")
                # Intentar convertir a número si aplica (simple heurística)
                try:
                    if '.' in campo: # Si es un campo anidado, podría ser un float (ej. macros.grasas_g)
                        nuevo_valor = float(nuevo_valor_str)
                    elif nuevo_valor_str.isdigit(): # Si es un número entero
                        nuevo_valor = int(nuevo_valor_str)
                    else:
                        nuevo_valor = nuevo_valor_str # Si no, es un string
                except ValueError:
                    nuevo_valor = nuevo_valor_str # Dejar como string si falla la conversión
                actualizar_campo_directo(nombre_alimento, campo, nuevo_valor)
            elif update_opcion == '3':
                nombre_micro = input("Nombre del micronutriente: ")
                cantidad_micro = float(input("Cantidad del micronutriente (mg/mcg): "))
                agregar_o_actualizar_micronutriente(nombre_alimento, nombre_micro, cantidad_micro)
            else:
                print("Opción de actualización no válida.")

        elif opcion == '4': # ELIMINAR ALIMENTO
            print("\n--- Eliminar Alimento ---")
            print("1. Eliminar por Nombre")
            print("2. Eliminar por Categoría (múltiples)")
            print("3. Eliminar Micronutriente de un Alimento")
            delete_opcion = input("Selecciona una opción de eliminación: ")

            if delete_opcion == '1':
                nombre = input("Nombre del alimento a eliminar: ")
                eliminar_alimento_por_nombre(nombre)
            elif delete_opcion == '2':
                categoria = input("Categoría de alimentos a eliminar: ")
                eliminar_alimentos_por_categoria(categoria)
            elif delete_opcion == '3':
                nombre_alimento = input("Nombre del alimento (para eliminar micronutriente): ")
                nombre_micro = input("Nombre del micronutriente a eliminar: ")
                eliminar_micronutriente_de_alimento(nombre_alimento, nombre_micro)
            else:
                print("Opción de eliminación no válida.")

        elif opcion == '0': # SALIR
            print("Saliendo del menú interactivo. ¡Adiós!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

        input("\nPresiona Enter para continuar...") # Pausa para ver la salida

# --- Bloque de Ejecución Principal de la Aplicación ---
if __name__ == "__main__": 
    # si se quiere empezar con una colección vacía cada vez que se ejecute el script.
    # collection = get_collection()
    # if collection is not None:
    #     collection.delete_many({})
    #     print("Colección 'alimentos' limpiada.")

    # IMPORTANTE: 
    # Si quieres insertar ALIMENTOS ADICIONALES a los 99 ya cargados, puedes usar la función:
    # crear_alimento({
    #     "nombre": "Nuevo Alimento Extra",
    #     "categoria": "Snack",
    #     "porciones": [{ "unidad": "unidad", "cantidad": 1, "gramos": 50, "calorias": 200 }],
    #     "macros": { "proteinas_g": 5.0, "carbohidratos_g": 20.0, "grasas_g": 10.0 },
    #     "micronutrientes": [], "fibra_g": 2.0, "azucar_g": 10.0, "alergenos": []
    # })

    print("\n¿Qué quieres hacer?")
    print("1. Ejecutar la demostración automática de CRUD (para la evaluación)")
    print("2. Iniciar el menú CRUD interactivo (para probar tú mismo)")
    eleccion_modo = input("Elige una opción (1 o 2): ")

    if eleccion_modo == '1':
        print("\n=== INICIANDO DEMOSTRACIÓN AUTOMÁTICA DE CRUD ===")
        # 1. Crear (Insertar) algunos alimentos para demostración (estos se añadirán a los 99 existentes)
        print("\n=== DEMOSTRACIÓN DE CREATE ===")
        nuevo_alimento_demo1 = {
            "nombre": "Galletas de Arroz (sin gluten)",
            "categoria": "Snack Saludable",
            "porciones": [
                { "unidad": "unidad", "cantidad": 1, "gramos": 10, "calorias": 35 }
            ],
            "macros": { "proteinas_g": 0.5, "carbohidratos_g": 7.5, "grasas_g": 0.5 },
            "micronutrientes": [],
            "fibra_g": 0.2, "azucar_g": 0.1, "alergenos": [],
        }
        crear_alimento(nuevo_alimento_demo1)

        nuevo_alimento_demo2 = {
            "nombre": "Cereal de Maíz Tostado (sin azucar)",
            "categoria": "Cereal",
            "porciones": [
                { "unidad": "taza", "cantidad": 1, "gramos": 28, "calorias": 100 }
            ],
            "macros": { "proteinas_g": 2.0, "carbohidratos_g": 23.0, "grasas_g": 0.5 },
            "micronutrientes": [{ "nombre": "Hierro", "cantidad_mg": 8.0 }],
            "fibra_g": 1.0, "azucar_g": 0.0, "alergenos": [],
        }
        crear_alimento(nuevo_alimento_demo2)

        alimento_para_eliminar_masivo_demo = {
            "nombre": "Bebida Energética Monster",
            "categoria": "Bebida",
            "porciones": [
                { "unidad": "lata (500ml)", "cantidad": 1, "gramos": 500, "calorias": 200 }
            ],
            "macros": { "proteinas_g": 0.0, "carbohidratos_g": 54.0, "grasas_g": 0.0 },
            "micronutrientes": [{ "nombre": "Cafeína", "cantidad_mg": 160 }],
            "fibra_g": 0.0, "azucar_g": 54.0, "alergenos": [],
        }
        crear_alimento(alimento_para_eliminar_masivo_demo)


        # 2. Leer (Consultar) diferentes tipos de datos
        print("\n=== LECTURA / CONSULTAS ===")
        print("\n--- Lectura 2.1: Todos los alimentos (primeros 5 para no saturar la terminal) ---")
        collection_read_all = get_collection()
        if collection_read_all is not None:
            for alimento in collection_read_all.find().limit(5):
                print(alimento)

        print("\n--- Lectura 2.2: Alimento por nombre exacto ---")
        buscar_por_nombre("Manzana Roja")

        print("\n--- Lectura 2.3: Alimentos con porciones entre 100 y 150 calorías ---")
        buscar_por_rango_calorias(100, 150)

        print("\n--- Lectura 2.4: Nombre y calorías de Frutas ---")
        buscar_por_categoria_y_proyectar("Fruta", ["nombre", "porciones.calorias"])

        print("\n--- Lectura 2.5: Alimentos con Vitamina K ---")
        buscar_alimentos_con_micronutriente("Vitamina K")

        print("\n--- Lectura 2.6: Alimentos Proteicos con más de 10g de Proteínas (AND implícito) ---")
        collection_read_protein = get_collection()
        if collection_read_protein is not None:
            alimentos_proteicos_altos = collection_read_protein.find({
                "categoria": "Proteína",
                "macros.proteinas_g": { "$gt": 10.0 }
            })
            encontrados = False
            for alimento in alimentos_proteicos_altos:
                print(alimento)
                encontrados = True
            if not encontrados:
                print("No se encontraron alimentos proteicos con más de 10g de proteínas.")

        print("\n--- Lectura 2.7: Alimentos Lácteos O Vegetales (OR explícito) ---")
        collection_read_or = get_collection()
        if collection_read_or is not None:
            alimentos_lacteos_vegetales = collection_read_or.find({
                "$or": [
                    { "categoria": "Lácteo" },
                    { "categoria": "Vegetal" }
                ]
            })
            encontrados = False
            for alimento in alimentos_lacteos_vegetales:
                print(alimento)
                encontrados = True
            if not encontrados:
                print("No se encontraron alimentos Lácteos o Vegetales.")

        print("\n--- Lectura 2.8: Galletas con Alergeno 'gluten' (Filtro en array) ---")
        buscar_por_alergenos("gluten")

        # 3. Actualizar datos
        print("\n=== ACTUALIZACIONES ===")
        actualizar_calorias_por_nombre("Manzana Roja", 100, "unidad")
        actualizar_campo_directo("Naranja", "categoria", "Cítrico")
        agregar_o_actualizar_micronutriente("Plátano", "Vitamina A", 0.05)
        actualizar_campo_directo("Brownie NutraBien", "macros.grasas_g", 10.0)

        # Verificación después de actualizaciones
        print("\n--- VERIFICANDO ACTUALIZACIONES ---")
        buscar_por_nombre("Manzana Roja")
        buscar_por_nombre("Naranja")
        buscar_por_nombre("Plátano")
        buscar_por_nombre("Brownie NutraBien")

        # 4. Eliminar datos
        print("\n=== ELIMINACIONES ===")
        eliminar_alimento_por_nombre("Espinaca (cocida)")
        eliminar_alimentos_por_categoria("Bebida Alcohólica")
        eliminar_micronutriente_de_alimento("Manzana Roja", "Potasio")

        # Verificación después de eliminaciones
        print("\n--- VERIFICANDO ELIMINACIONES ---")
        leer_todos_alimentos()

        print("\n=== Todas las operaciones CRUD han sido demostradas. ===")

    elif eleccion_modo == '2':
        menu_interactivo_crud() # Esta línea llama a la función del menú interactivo
    else:
        print("Opción no válida. Por favor, ejecuta el script de nuevo y elige 1 o 2.")