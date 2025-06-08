# 🧠 LexFlash

**LexFlash** es una aplicación interactiva hecha en Python para aprender vocabulario mediante tarjetas de memoria (*flashcards*). Incluye puntajes, límite de errores y control de tiempo.

---

## 🚀 Características

- 📂 Carga de tarjetas desde un archivo CSV personalizado
- ⏱️ Temporizador por pregunta (30 segundos)
- ❌ Fin del juego si cometes más de 5 errores
- 💾 Guardado automático de puntajes en base de datos local (SQLite)
- 🎨 Interfaz limpia y minimalista con `tkinter`
- 🌍 Ideal para practicar idiomas (español, inglés, italiano, etc.)

---

## 📂 Formato del archivo CSV

Tu archivo `.csv` debe tener **dos columnas separadas por punto y coma (`;`)**:

- La **primera columna** es la palabra original (por ejemplo, en español)
- La **segunda columna** es la traducción correcta (por ejemplo, en inglés)

### Ejemplo válido:

Perro;Dog
Casa;House
Gato;Cat
Gracias;Thank you

⚠️ Asegúrate de que el archivo:

- No tenga encabezados
- Esté guardado en codificación `Latin-1` o `UTF-8`
- Use `;` como separador

---

## 💻 Requisitos

- Python 3.6 o superior
- Sistema operativo con soporte para `tkinter` (Linux, Windows, macOS)
- No se requieren librerías externas

---

## ▶️ Cómo ejecutar

Desde terminal (Linux o Windows):

```bash
python lexflash.py
