# Visor de Asignación Académica

Este repositorio contiene la aplicación web estática que permite visualizar y descargar la asignación académica.

## Contenido
- `index.html` – la aplicación generada (renombrada desde `visor_asignacion.html`).
- `extract_data.py` y `build_app.py` – scripts para regenerar `index.html` a partir del archivo Excel.
- `Asignacion LUIS CARLOS.xlsx` – archivo de datos inicial (puede actualizarse).
- `.github/workflows/deploy.yml` – workflow de GitHub Actions que genera y despliega la página en GitHub Pages.

## Cómo actualizar los datos
1. Modifica o reemplaza `Asignacion LUIS CARLOS.xlsx` con la nueva versión.
2. Ejecuta localmente:
   ```bash
   python build_app.py
   ```
   Esto regenerará `index.html` con los datos actualizados.
3. Haz commit y push de los cambios (incluyendo el nuevo Excel) al repositorio.
   El workflow de CI se encargará de volver a generar y publicar la página automáticamente.

## Despliegue automático (GitHub Pages)
- El workflow publica el contenido del repositorio en la rama `gh-pages` y habilita GitHub Pages.
- La URL pública será algo como `https://<usuario>.github.io/<repo>/`.

## Requisitos
- Python 3.11+ con `pandas` y `openpyxl`.
- Git y una cuenta en GitHub.

## Pasos para crear el repositorio
1. Crea un nuevo repositorio en GitHub (p. ej., `academic-assignment-viewer`).
2. Clona el repositorio en tu máquina.
3. Copia los archivos de este proyecto al directorio del repositorio.
4. Renombra `visor_asignacion.html` a `index.html`.
5. Añade y confirma los archivos:
   ```bash
   git add .
   git commit -m "Initial commit with viewer and CI workflow"
   git push origin main
   ```
6. Habilita GitHub Pages en la configuración del repositorio (fuente: rama `gh-pages`).

## Notas
- Si el archivo Excel es grande, considera usar **Git LFS**.
- Puedes usar otras plataformas de hosting estático (Netlify, Vercel) conectando el mismo repositorio y configurando el comando de construcción `python build_app.py`.
