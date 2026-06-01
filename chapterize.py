from bs4 import BeautifulSoup, Tag
import re
import sys

def slugify_chapter(text):
    """Convierte el título del capítulo en un ID tipo 'chapter-1-loomings'"""
    # Limpiar el texto del título
    text = re.sub(r'^CHAPTER\s+\d+\.?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^ETYMOLOGY$', 'etymology', text, flags=re.IGNORECASE)
    text = re.sub(r'^EXTRACTS', 'extracts', text, flags=re.IGNORECASE)
    text = re.sub(r'^Epilogue', 'epilogue', text, flags=re.IGNORECASE)
    # Normalizar
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)          # eliminar puntuación
    text = re.sub(r'[\s_]+', '-', text)           # espacios a guiones
    return f"chapter-{text}"

def main(html_path, output_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Trabajaremos dentro del <body> (podría haber varios elementos fuera, pero normalmente todo está en body)
    body = soup.body
    if body is None:
        # Si no hay body, usar el propio soup (pero en Project Gutenberg sí hay)
        container = soup
    else:
        container = body

    # Recopilar todos los elementos hijos del container (lista plana)
    elements = list(container.children)
    
    # Buscar los índices donde comienza un capítulo (etiquetas h2 que son títulos de capítulo)
    chapter_starts = []  # lista de índices en 'elements' donde comienza un capítulo (incluyendo el título y su preámbulo)
    for i, elem in enumerate(elements):
        if elem.name == 'h2':
            text = elem.get_text(strip=True)
            if re.match(r'^(CHAPTER|ETYMOLOGY|EXTRACTS|Epilogue)', text, re.IGNORECASE):
                # Determinar el índice real de inicio: puede haber un <div> con height:4em y un <a> antes
                start_idx = i
                # Retroceder si hay un div de separación antes
                if start_idx > 0 and elements[start_idx-1].name == 'div' and 'height' in elements[start_idx-1].get('style', '') and '4em' in elements[start_idx-1].get('style', ''):
                    start_idx = start_idx - 1
                    # Retroceder si antes de ese div hay un anchor
                    if start_idx > 0 and elements[start_idx-1].name == 'a' and elements[start_idx-1].get('id', '').startswith('link2HCH'):
                        start_idx = start_idx - 1
                elif start_idx > 0 and elements[start_idx-1].name == 'a' and elements[start_idx-1].get('id', '').startswith('link2HCH'):
                    start_idx = start_idx - 1
                
                chapter_starts.append((start_idx, i, elem))  # (inicio real, índice del h2, etiqueta h2)

    # Si no hay capítulos, salir
    if not chapter_starts:
        print("No se encontraron capítulos.")
        return

    # Añadir un punto final ficticio al final de todos los elementos
    chapter_starts.append((len(elements), len(elements), None))

    # Construir la nueva lista de elementos que reemplazará a 'container.children'
    new_children = []

    # Elementos antes del primer capítulo (si existen)
    first_start = chapter_starts[0][0]
    if first_start > 0:
        new_children.extend(elements[:first_start])

    # Procesar cada capítulo
    for idx in range(len(chapter_starts)-1):
        start_idx, h2_idx, h2_tag = chapter_starts[idx]
        end_idx = chapter_starts[idx+1][0]   # el inicio del siguiente capítulo (exclusivo)

        # Elementos que componen este capítulo
        chapter_elements = elements[start_idx:end_idx]

        # Crear un nuevo div contenedor
        div = Tag(name='div')
        div['class'] = 'chapter'
        div['id'] = slugify_chapter(h2_tag.get_text(strip=True))

        # Añadir todos los elementos del capítulo dentro del div
        for elem in chapter_elements:
            div.append(elem)

        # Añadir el div a la nueva lista de hijos
        new_children.append(div)

    # Reemplazar los hijos del container por los nuevos
    container.clear()
    for child in new_children:
        container.append(child)

    # Guardar el resultado
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python chapterize.py archivo_entrada.html archivo_salida.html")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])