# ---------------------------------------------
# 1) ESCALA CROMÁTICA Y ESTRUCTURAS GLOBALES
# ---------------------------------------------
chromatic_scale = [
    ["C", "B#", "Dbb"],   # 0
    ["C#", "Db", "B##"],  # 1
    ["D", "C##", "Ebb"],  # 2
    ["D#", "Eb", "Fbb"],  # 3
    ["E", "Fb", "D##"],   # 4
    ["F", "E#", "Gbb"],   # 5
    ["F#", "Gb", "E##"],  # 6
    ["G", "F##", "Abb"],  # 7
    ["G#", "Ab", "F###"], # 8
    ["A", "G##", "Bbb"],  # 9
    ["A#", "Bb", "Cbb"],  # 10
    ["B", "Cb", "A##"]    # 11
]

# Armaduras de las tonalidades mayores (en inglés)
major_key_signatures_en = {
    # 0 accidentals
    "C":  0,
    # + sharps (1 a 7)
    "G":  1,  
    "D":  2,
    "A":  3,
    "E":  4,
    "B":  5,
    "F#": 6,
    "C#": 7,
    # - flats (1 a 7)
    "F":  -1, 
    "Bb": -2,
    "Eb": -3,
    "Ab": -4,
    "Db": -5,
    "Gb": -6,
    "Cb": -7
}

# Mapeo: modo → offset (en semitonos) para llegar a su relativo mayor
mode_to_major_offset = {
    "Ionian":     0,
    "Dorian":    -2,
    "Phrygian":  -4,
    "Lydian":     5,
    "Mixolydian": -7,
    "Aeolian":   -9,
    "Locrian":   -11
}


# ---------------------------------------------
# 2) FUNCIONES DE UTILIDAD
# ---------------------------------------------
def find_root_index(chromatic_scale, root_note):
    """
    Devuelve el índice (0-11) en 'chromatic_scale' donde se halle 'root_note'.
    Si no lo encuentra, retorna None.
    """
    for i, names in enumerate(chromatic_scale):
        if root_note in names:
            return i
    return None

def get_relative_major(root_note, mode):
    """
    Dado (root_note, mode), retorna la tónica de la 'escala mayor' relativa.
    Ejemplo: get_relative_major("G", "Aeolian") -> "Bb".
    """
    root_index = find_root_index(chromatic_scale, root_note)
    if root_index is None:
        raise ValueError(f"Nota raíz inválida: {root_note}")

    if mode not in mode_to_major_offset:
        raise ValueError(f"Modo inválido: {mode}")

    offset = mode_to_major_offset[mode] % 12
    major_index = (root_index + offset) % 12

    # De las enarmonías en major_index, elegimos la que esté en major_key_signatures_en
    candidates = chromatic_scale[major_index]
    for cand in candidates:
        if cand in major_key_signatures_en:
            return cand
    # Fallback
    return candidates[0]

def pick_note_for_key_signature(candidates, key_sig):
    """
    Elige la enarmonía de 'candidates' más conveniente según 'key_sig'.
      - key_sig > 0 => preferimos '#'
      - key_sig < 0 => preferimos 'b'
      - key_sig = 0 => preferimos notas naturales.
    """
    if key_sig < 0:
        # Preferimos 'b'
        for cand in candidates:
            if "b" in cand and "#" not in cand:
                return cand
        return candidates[0]
    elif key_sig > 0:
        # Preferimos '#'
        for cand in candidates:
            if "#" in cand and "b" not in cand:
                return cand
        return candidates[0]
    else:
        # key_sig == 0 => preferimos forma natural
        for cand in candidates:
            if "#" not in cand and "b" not in cand:
                return cand
        return candidates[0]


# ---------------------------------------------
# 3) CALCULAR LA "ROOT SCALE" (OPCIONAL)
# ---------------------------------------------
def calculate_root_scale(root_note, mode):
    """
    (Esta función estaba antes en tu código. 
     Puedes mantenerla si aún deseas usarla en otros lugares.
     Pero para el enarmonizado fino, usaremos la lógica de get_relative_major.)
    """
    shift = mode_to_major_offset[mode] % 12
    root_index = find_root_index(chromatic_scale, root_note)
    if root_index is None:
        raise ValueError(f"Nota raíz inválida: {root_note}.")

    root_scale_index = (root_index + shift) % 12
    # Elige la PRIMERA enarmonía
    root_scale_note = chromatic_scale[root_scale_index][0]
    return root_scale_note


# ---------------------------------------------
# 4) FUNCION PRINCIPAL PARA ESCALAS/MODOS
# ---------------------------------------------
def calculate_major_scale(root_note, mode="Ionian", chord_scale_type="standard", variation=None):
    """
    Construye la escala (o modo) desde 'root_note', usando 
    la armadura de su escala mayor relativa para asignar enarmonías convenientes.
    """
    interval_names = {
        0:  "Unín perfecto (1P)",
        1:  "Segunda menor (2m) / Novena menor (b9)",
        2:  "Segunda mayor (2M) / Novena mayor (9)",
        3:  "Tercera menor (3m)",
        4:  "Tercera mayor (3M)",
        5:  "Cuarta justa (4J) / Oncena justa (11)",
        6:  "Tritono (TT) / Quinta disminuida (b5) / Oncena aumentada (#11)",
        7:  "Quinta justa (5J)",
        8:  "Sexta menor (6m) / Trecena menor (b13)",
        9:  "Sexta mayor (6M) / Trecena mayor (13)",
        10: "Séptima menor (7m)",
        11: "Séptima mayor (7M)",
        12: "Octava perfecta (8P)"
    }

    mode_definitions = {
        "Ionian": {
            "pattern": [2, 2, 1, 2, 2, 2, 1],
            "roles": {
                0: "Permitido",
                2: "Permitido",
                4: "Permitido",
                5: "Evitado",
                7: "Permitido",
                9: "Permitido",
                11: "Permitido"
            }
        },
        "Dorian": {
            "pattern": [2, 1, 2, 2, 2, 1, 2],
            "roles": {
                0: "Permitido",
                2: "Permitido",
                3: "Permitido",
                5: "Permitido",
                7: "Permitido",
                9: "Evitado",
                10: "Permitido"
            }
        },
        "Phrygian": {
            "pattern": [1, 2, 2, 2, 1, 2, 2],
            "roles": {
                0: "Permitido",
                1: "Evitado",
                3: "Permitido",
                5: "Permitido",
                7: "Permitido",
                8: "Evitado",
                10: "Permitido"
            }
        },
        "Lydian": {
            "pattern": [2, 2, 2, 1, 2, 2, 1],
            "roles": {
                0: "Permitido",
                2: "Permitido",
                4: "Permitido",
                6: "Permitido",
                7: "Permitido",
                9: "Permitido",
                11: "Permitido"
            }
        },
        "Mixolydian": {
            "pattern": [2, 2, 1, 2, 2, 1, 2],
            "roles": {
                0: "Permitido",
                2: "Permitido",
                4: "Permitido",
                5: "Evitado",
                7: "Permitido",
                9: "Permitido",
                10: "Permitido"
            },
            "variations": {
                "sus4": {
                    "pattern": [2, 2, 1, 2, 2, 1, 2],
                    "roles": {
                        0: "Permitido",
                        2: "Permitido",
                        4: "Evitado",
                        5: "Permitido",
                        7: "Permitido",
                        9: "Permitido",
                        10: "Permitido"
                    }
                },
                "7(b9,b13)": {
                    "pattern": [1, 3, 1, 2, 1, 2, 2],
                    "roles": {
                        0: "Permitido",
                        1: "Permitido",
                        4: "Permitido",
                        5: "Evitado",
                        7: "Permitido (Excluyente)",
                        8: "Permitido (Excluyente)",
                        10: "Permitido"
                    }
                },
                "7(b9,#9,b13)": {
                    "pattern": [1, 2, 1, 1, 2, 1, 2],
                    "roles": {
                        0: "Permitido",
                        1: "Permitido",
                        3: "Permitido",
                        4: "Permitido",
                        5: "Evitado",
                        7: "Permitido (Excluyente)",
                        8: "Permitido (Excluyente)",
                        10: "Permitido"
                    }
                },
                "7b5(b9,#9,b13)": {
                    "pattern": [1, 2, 1, 1, 2, 2, 2],
                    "roles": {
                        0: "Permitido",
                        1: "Permitido",
                        3: "Permitido",
                        4: "Permitido",
                        6: "Permitido",
                        8: "Permitido",
                        10: "Permitido"
                    }
                },
                "7(b9,#9,#11,13)": {
                    "pattern": [1, 2, 1, 2, 2, 1, 2],
                    "roles": {
                        0: "Permitido",
                        1: "Permitido",
                        3: "Permitido",
                        4: "Permitido",
                        6: "Permitido",
                        7: "Permitido",
                        9: "Permitido",
                        10: "Permitido"
                    }
                }
            }
        },
        "Aeolian": {
            "pattern": [2, 1, 2, 2, 1, 2, 2],
            "roles": {
                0: "Permitido",
                2: "Permitido",
                3: "Permitido",
                5: "Permitido",
                7: "Permitido",
                8: "Evitado",
                10: "Permitido"
            }
        },
        "Locrian": {
            "pattern": [1, 2, 2, 1, 2, 2, 2],
            "roles": {
                0: "Permitido",
                1: "Evitado",
                3: "Permitido",
                5: "Permitido",
                6: "Permitido",
                8: "Permitido",
                10: "Permitido"
            }
        }
    }

    if mode not in mode_definitions:
        raise ValueError(f"Modo inválido: {mode}. Modos disponibles: {', '.join(mode_definitions.keys())}")

    mode_data = mode_definitions[mode]

    # Chequeo de variaciones (Mixolydian, etc.)
    if variation and "variations" in mode_data and variation in mode_data["variations"]:
        scale_pattern = mode_data["variations"][variation]["pattern"]
        chord_scale_roles = mode_data["variations"][variation]["roles"]
    else:
        scale_pattern = mode_data["pattern"]
        chord_scale_roles = mode_data["roles"]

    # 1) Averigua la tonalidad mayor relativa y su armadura
    relative_major = get_relative_major(root_note, mode)   # p.ej. "Bb"
    key_sig = major_key_signatures_en[relative_major]      # p.ej. -2

    # 2) Encuentra el índice de la nota raíz
    root_index = find_root_index(chromatic_scale, root_note)
    if root_index is None:
        raise ValueError(f"Nota raíz inválida: {root_note}.")

    # 3) Construir la escala
    scale_notes = []
    intervals = []
    roles = []
    used_letters = set()

    for interval, role in sorted(chord_scale_roles.items()):
        current_index = (root_index + interval) % 12
        note_options = chromatic_scale[current_index]

        if interval == 0:
            # Raíz tal como la ingresó el usuario, si quieres
            note = root_note
        else:
            # Elegir enarmonía según la armadura
            chosen = pick_note_for_key_signature(note_options, key_sig)
            # Adicionalmente, chequeo 'used_letters' para no repetir la misma letra consecutiva
            note = chosen
            for opt in note_options:
                if opt[0] not in used_letters:
                    note = pick_note_for_key_signature([opt], key_sig)
                    break

        used_letters.add(note[0])
        scale_notes.append(note)
        intervals.append(interval_names.get(interval, "Desconocido"))
        roles.append(role)

    # 4) Como "root_scale", devolvemos la mayor relativa 
    #    (o puedes quedarte con la antigua calculate_root_scale(root_note, mode), 
    #     pero te generaría enarmonías no tan limpias).
    return {
        "notes": scale_notes,
        "intervals": intervals,
        "roles": roles,
        "root_scale": relative_major
    }


# ---------------------------------------------
# 5) CALCULAR MODOS DE CADA GRADO
# ---------------------------------------------
def calculate_modes_for_degrees(root_note, mode):
    # 1) Obtener la tonalidad mayor relativa (por ejemplo, "Bb" si pides G Aeolian)
    major_relative = get_relative_major(root_note, mode)

    # 2) Sacar la escala Ionian de esa tonalidad mayor
    base_scale = calculate_major_scale(major_relative, mode="Ionian")
    print(f"Escala base (Ionian) desde {major_relative}: {base_scale['notes']}")

    # 3) Listado de modos para cada grado
    degrees_modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]

    # 4) Para cada nota de la escala Ionian base, calculamos su modo
    for i, note in enumerate(base_scale["notes"]):
        current_mode = degrees_modes[i]
        mode_result = calculate_major_scale(note, mode=current_mode)
        print(f"Grado {i + 1} ({current_mode}):")
        for n, interval, role in zip(mode_result["notes"], mode_result["intervals"], mode_result["roles"]):
            print(f"  {n}: {interval} - {role}")


# ---------------------------------------------
# 6) MAIN DE PRUEBA
# ---------------------------------------------
if __name__ == "__main__":
    root_note = "G"
    mode = "Aeolian"
    result = calculate_major_scale(root_note, mode=mode)

    print(f"Escala {mode} desde {root_note}:")
    for note, interval, role in zip(result["notes"], result["intervals"], result["roles"]):
        print(f"{note}: {interval} - {role}")

    print(f"Escala raíz (mayor relativa): {result['root_scale']}")

    print("\nCalculando modos de la Escala Raíz:")
    calculate_modes_for_degrees(root_note, mode)

    # Ejemplo de Mixolydian con variación
    root_note = "G"
    mode = "Mixolydian"
    variation = "sus4"
    result = calculate_major_scale(root_note, mode=mode, variation=variation)

    print(f"\nEscala {mode} con variación {variation} desde {root_note}:")
    for note, interval, role in zip(result["notes"], result["intervals"], result["roles"]):
        print(f"{note}: {interval} - {role}")
