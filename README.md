# lexflash
Una app para aprender vocabulario usando tarjetas y reflejos mentales


# 🧠 LexiFlash

Una aplicación interactiva hecha en Python para aprender vocabulario mediante tarjetas de memoria (*flashcards*), con puntaje, límite de errores, y control de tiempo.

---

## 🚀 Características

- Carga de tarjetas desde un archivo CSV personalizado
- Temporizador por pregunta (30 segundos)
- Pérdida automática si cometes más de 5 errores
- Guardado de puntajes en una base de datos local (SQLite)
- Interfaz limpia y minimalista con `tkinter`
- Ideal para practicar idiomas de forma rápida

---

## 📂 Formato del archivo CSV

Tu archivo `.csv` debe tener **dos columnas separadas por punto y coma (`;`)**:

- La **primera columna** es la palabra original (ejemplo: en español)
- La **segunda columna** es la traducción correcta (ejemplo: en inglés)
