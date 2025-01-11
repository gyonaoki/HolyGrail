El programa se basa en principios fundamentales de la **teoría musical occidental** y organiza sus funciones para reflejar conceptos clave relacionados con las escalas musicales y los modos.

---

### 1. **Fundamento en la Escala Cromática**
La escala cromática es la base del programa. Este sistema, usado en la música occidental, contiene 12 notas (o semitonos) por octava. Estas notas incluyen equivalencias enharmónicas, como `C#` y `Db`, que suenan igual pero se escriben diferente. El programa utiliza una lista estructurada para representar estas relaciones, lo que permite trabajar de manera flexible con cualquier representación de una nota.

---

### 2. **Modos Musicales y Patrones de Intervalos**
Los modos son variaciones de una escala que se originan al reorganizar las notas de una escala mayor. Por ejemplo, `Ionian` es la escala mayor estándar, mientras que `Dorian`, `Phrygian`, y otros modos se construyen ajustando la posición inicial o desplazando los intervalos.

- Cada modo tiene un patrón de distancias (en semitonos) entre sus notas, conocido como **patrón de intervalos**. 
- El programa define estos patrones y utiliza un sistema de desplazamiento para determinar la posición relativa de cada modo respecto a la escala mayor.

---

### 3. **Construcción de Escalas**
La creación de escalas es el núcleo del programa:
- A partir de una nota raíz, el programa sigue el patrón de intervalos del modo seleccionado para identificar las notas que forman la escala.
- Para garantizar una construcción precisa, utiliza:
  - La posición de la nota raíz en la escala cromática.
  - Cálculos matemáticos modulares para recorrer la escala cromática de forma cíclica, asegurando que las notas permanezcan dentro de una octava.

---

### 4. **Roles de Notas e Intervalos**
Cada nota en una escala tiene un **rol musical**, como "permitido" o "evitado", que depende del contexto del modo:
- Las notas "permitidas" son características del modo y suelen sonar naturales en la música.
- Las notas "evitadas" tienen una relación más disonante o inusual con la tónica y requieren cuidado en su uso.

El programa asigna roles a cada nota utilizando una lista predefinida de intervalos y sus nombres (por ejemplo, "Unísono perfecto", "Segunda mayor", etc.).

---

### 5. **Exploración de Modos y Grados**
El programa no se limita a construir una escala; también explora sus **modos asociados**:
- Cada grado de una escala puede convertirse en el punto de partida de un nuevo modo.
- Por ejemplo, si partes de la escala mayor de `C` (`C-D-E-F-G-A-B`):
  - El primer grado (`C`) es `Ionian`.
  - El segundo grado (`D`) es `Dorian`.
  - El tercer grado (`E`) es `Phrygian`, y así sucesivamente.

Esto permite estudiar cómo las relaciones entre notas cambian según el punto de partida.

---

### 6. **Variaciones y Personalización**
El programa incorpora **variaciones de modos**, lo que lo hace más versátil:
- Modos como `Mixolydian` pueden modificarse para incluir variaciones específicas (`sus4`, `7(b9,b13)`, etc.).
- Estas variaciones ajustan los patrones de intervalos y los roles de las notas, ofreciendo herramientas avanzadas para explorar escalas menos comunes.

---

### 7. **Matemática Modular y Cíclica**
La teoría musical tiene un carácter cíclico: después de 12 semitonos, las notas vuelven a su punto de partida (una octava más alta). El programa utiliza operaciones matemáticas modulares (`% 12`) para manejar esta ciclicidad, asegurando que los cálculos sean consistentes dentro de una octava.

---

### 8. **Estructura Modular y Reutilizable**
El código está diseñado de manera modular:
- Las funciones clave (`calculate_root_scale`, `calculate_major_scale`, etc.) son independientes, lo que facilita su comprensión y reutilización.
- Cada función tiene un propósito específico, como encontrar la nota raíz, construir una escala o explorar modos.

---

### 9. **Aplicaciones del Programa**
El programa tiene aplicaciones tanto educativas como creativas:
- **Educación Musical**: Es útil para estudiantes que desean aprender sobre escalas y modos de manera interactiva.
- **Composición y Análisis**: Ayuda a compositores y teóricos a analizar cómo funcionan los modos y escalas en diferentes contextos.
- **Exploración Creativa**: Permite experimentar con variaciones y escalas no convencionales.

---


### 1. **Definición de la Escala Cromática**

```python
chromatic_scale = [
    ["C", "B#", "Dbb"],  # 0
    ["C#", "Db", "B##"],  # 1
    ["D", "C##", "Ebb"],  # 2
    ...
]
```

- La escala cromática es una lista que representa las 12 notas de un sistema musical occidental, enumeradas desde `C` (índice 0) hasta `B` (índice 11). 
- Cada entrada contiene **todas las posibles representaciones enharmónicas** de una nota (notas que suenan igual pero se escriben diferente). Ejemplo:
  - `C` es equivalente a `B#` (si subes medio tono desde `B`) y `Dbb` (si bajas dos tonos desde `D`).

Esta estructura permite que el programa reconozca automáticamente cualquier representación de una nota en las funciones siguientes.

---

### 2. **Definición de Modos y Desplazamientos**

```python
mode_shifts = {
    "Ionian": 0,
    "Dorian": -2,
    "Phrygian": -4,
    ...
}
```

- Cada modo tiene un **desplazamiento** (en semitonos) relativo a la escala mayor (`Ionian`), que se usa para calcular la nota raíz ajustada al modo.
- Por ejemplo:
  - En el modo `Dorian`, la raíz se desplaza **2 semitonos hacia abajo**.
  - En el modo `Phrygian`, la raíz se desplaza **4 semitonos hacia abajo**.

El desplazamiento asegura que cada modo comience en el grado correcto de la escala mayor.

---

### 3. **Cálculo de la Nota Raíz Ajustada al Modo**

#### a. Función `find_root_index`
```python
def find_root_index(chromatic_scale, root_note):
    for i, names in enumerate(chromatic_scale):
        if root_note in names:
            return i
    return None
```

Esta función busca el índice de la nota raíz dentro de la escala cromática:
- Recorre cada lista de nombres en la escala cromática.
- Si encuentra la nota raíz (`root_note`) en la lista correspondiente, devuelve su índice.
- Si no encuentra la nota raíz, devuelve `None`.

#### b. Función `calculate_root_scale`
```python
def calculate_root_scale(root_note, mode):
    root_index = find_root_index(chromatic_scale, root_note)
    ...
```

Pasos detallados:
1. Llama a `find_root_index` para obtener el índice de la nota raíz en la escala cromática.
   - Ejemplo: Si `root_note = "C"`, el índice devuelto será `0`.
2. Valida si el modo (`mode`) existe en `mode_shifts`. Si no, lanza un error:
   ```python
   if mode not in mode_shifts:
       raise ValueError(f"Modo inválido: {mode}")
   ```
3. Calcula el índice ajustado al modo:
   ```python
   shift = mode_shifts[mode] % 12
   root_scale_index = (root_index + shift) % 12
   ```
   - **`% 12`** asegura que el índice permanece en el rango `0-11` (12 notas).
   - Ejemplo:
     - `root_index = 0` (C).
     - `mode = "Dorian"` (`shift = -2`).
     - `root_scale_index = (0 - 2) % 12 = 10` (Bb).
4. Devuelve la primera representación de la nota ajustada:
   ```python
   root_scale_note = chromatic_scale[root_scale_index][0]
   ```

Resultado:
- La nota raíz ajustada para `C` en el modo `Dorian` es `Bb`.

---

### 4. **Construcción de Escalas**
#### a. Función `calculate_major_scale`
```python
def calculate_major_scale(root_note, mode="Ionian", ...):
    ...
```

Pasos detallados:

1. **Obtener el índice de la nota raíz**:
   ```python
   root_index = find_root_index(chromatic_scale, root_note)
   ```
   - Encuentra el índice de `root_note` en `chromatic_scale`.
   - Ejemplo: Para `root_note = "C"`, el índice será `0`.

2. **Obtener el patrón del modo**:
   ```python
   mode_data = mode_definitions[mode]
   scale_pattern = mode_data["pattern"]
   chord_scale_roles = mode_data["roles"]
   ```
   - Busca en `mode_definitions` el patrón del modo y los roles asignados a cada intervalo.

3. **Construir la escala**:
   ```python
   for interval, role in sorted(chord_scale_roles.items()):
       current_index = (root_index + interval) % 12
       note_options = chromatic_scale[current_index]
   ```
   - Para cada intervalo definido en el patrón:
     - Calcula el índice de la nota (`current_index`).
     - Busca las posibles representaciones (`note_options`).

4. **Evitar repeticiones de letras**:
   ```python
   if option[0] not in used_letters:
       note = option
       break
   ```
   - Selecciona una representación que no repita la letra inicial de la nota.

5. **Almacenar resultados**:
   - Guarda las notas, intervalos y roles en listas.

---

### 5. **Cálculo de Modos para Cada Grado**
```python
def calculate_modes_for_degrees(root_note, mode):
    root_scale = calculate_root_scale(root_note, mode)
    base_scale = calculate_major_scale(root_scale, mode="Ionian")
    ...
```

Pasos detallados:
1. Calcula la escala raíz en modo `Ionian`.
2. Para cada grado de la escala:
   - Toma la nota correspondiente como nueva raíz.
   - Calcula la escala en el modo asociado al grado.
3. Imprime las notas, intervalos y roles de cada grado.

---

### 6. **Ejecución Principal**
```python
if __name__ == "__main__":
    root_note = "C"
    mode = "Ionian"
    result = calculate_major_scale(root_note, mode=mode)
    ...
```

- Calcula la escala mayor de `C` en modo `Ionian`.
- Calcula los modos de cada grado.
- Ejemplo:
  ```plaintext
  Escala Ionian desde C:
  C: Uníson perfecto - Permitido
  D: Segunda mayor - Permitido
  ...
  ```

---

Resumen Final del Flujo

1. **Entrada**:
   - Nota raíz (`root_note`), modo (`mode`), y variaciones opcionales.
2. **Procesamiento**:
   - Encuentra la raíz ajustada al modo.
   - Construye la escala según el patrón del modo.
   - Calcula modos para cada grado, si es necesario.
3. **Salida**:
   - Lista de notas, intervalos y roles con detalles específicos del modo y variaciones.
