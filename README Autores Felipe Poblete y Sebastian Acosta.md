# 🍲 App de Gestión de Alimentos con MongoDB y Python

Este proyecto es una aplicación de consola desarrollada en Python que interactúa con una base de datos NoSQL MongoDB. Su propósito es demostrar las operaciones esenciales CRUD (Crear, Leer, Actualizar, Eliminar) sobre un conjunto de datos de alimentos, incluyendo productos naturales y de marcas conocidas, con una interfaz interactiva y una secuencia de demostración automática para evaluación.

---

## 🚀 Características y Funcionalidades

* **Base de Datos Temática Personalizada:** Utiliza una base de datos de 99 alimentos variados, incluyendo datos nutricionales detallados y alérgenos.
* **Modelo de Documentos Flexible:** El diseño de los documentos de alimentos incorpora subdocumentos (`macros`) y arrays de subdocumentos (`porciones`, `micronutrientes`) para una representación rica y realista.
* **Operaciones CRUD Completas:**
    * **Creación (Create):** Inserción de nuevos documentos de alimentos.
    * **Lectura (Read):** Consultas avanzadas con filtros de comparación (`$gte`, `$lte`), operadores lógicos (`$or`), proyecciones de campos, y búsquedas en estructuras anidadas y arrays (`$elemMatch`, dot notation).
    * **Actualización (Update):** Modificación de campos de nivel superior, campos anidados, y elementos específicos dentro de arrays mediante el uso de `$set` y `array_filters`.
    * **Eliminación (Delete):** Borrado de documentos individuales, múltiples documentos por criterio, y elementos específicos de arrays (`$pull`).
* **Modos de Ejecución Dual:**
    * **Demostración Automática:** Ejecuta una secuencia predefinida de operaciones CRUD para una presentación rápida y consistente (ideal para evaluación).
    * **Menú Interactivo:** Permite al usuario realizar operaciones CRUD manualmente a través de un menú de consola, ideal para pruebas y exploración.
* **Conectividad Robusta:** Configurable para conectar a instancias de MongoDB local o a clusters de MongoDB Atlas en la nube.

---

## 🛠️ Tecnologías y Herramientas

* **MongoDB:** Base de Datos NoSQL.
* **Python 3.x:** Lenguaje de programación.
* **PyMongo:** Controlador oficial de MongoDB para Python.
* **Visual Studio Code (VS Code):** Editor de código.
* **MongoDB Compass / Studio 3T:** Herramientas GUI para gestión y visualización de la base de datos.

---

## ⚙️ Configuración y Ejecución del Proyecto

Sigue estos pasos para configurar tu entorno y ejecutar la aplicación.

### 1. Requisitos Previos (Verifica Instalación)

Asegúrate de tener instalados los siguientes componentes:

* **Python 3.x:**
    * Descárgalo de [python.org/downloads/](https://www.python.org/downloads/).
    * **Crucial:** Marca la casilla **"Add Python X.X to PATH"** durante la instalación.
* **MongoDB Community Server:**
    * Descárgalo de [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community/).
    * Asegúrate de que el servicio de MongoDB esté en ejecución en tu máquina.
* **Visual Studio Code (VS Code):**
    * Descárgalo de [code.visualstudio.com](https://code.visualstudio.com/).
    * Instala la **extensión de Python de Microsoft** en VS Code.
* **MongoDB Compass o Studio 3T:**
    * Descárgalos de [mongodb.com/products/compass](https://www.mongodb.com/products/compass) o [studio3t.com/download](https://studio3t.com/download/).

### 2. Clonar el Repositorio

Abre tu terminal (o Git Bash) y clona este repositorio:

```bash
git clone [https://github.com/TuUsuario/NombreDeTuRepositorio.git](https://github.com/TuUsuario/NombreDeTuRepositorio.git)
cd NombreDeTuRepositorio # Navega a la carpeta del proyecto
