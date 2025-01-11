def calculate_root_scale(root_note, mode):
    chromatic_scale = [
        ["C", "B#", "Dbb"],  # 0
        ["C#", "Db", "B##"],  # 1
        ["D", "C##", "Ebb"],  # 2
        ["D#", "Eb", "Fbb"],  # 3
        ["E", "Fb", "D##"],  # 4
        ["F", "E#", "Gbb"],  # 5
        ["F#", "Gb", "E##"],  # 6
        ["G", "F##", "Abb"],  # 7
        ["G#", "Ab", "F###"],  # 8
        ["A", "G##", "Bbb"],  # 9
        ["A#", "Bb", "Cbb"],  # 10
        ["B", "Cb", "A##"]   # 11
    ]

    mode_shifts = {
        "Ionian": 0,
        "Dorian": -2,
        "Phrygian": -4,
        "Lydian": 5,
        "Mixolydian": -7,
        "Aeolian": -9,
        "Locrian": -11
    }

    if mode not in mode_shifts:
        raise ValueError(f"Modo inválido para calcular escala raíz: {mode}.")

    root_index = find_root_index(chromatic_scale, root_note)
    if root_index is None:
        raise ValueError(f"Nota raíz inválida: {root_note}.")

    shift = mode_shifts[mode] % 12
    root_scale_index = (root_index + shift) % 12
    root_scale_note = chromatic_scale[root_scale_index][0]  # Seleccionar la primera enarmonía
    return root_scale_note

def find_root_index(chromatic_scale, root_note):
    for i, names in enumerate(chromatic_scale):
        if root_note in names:
            return i
    return None

def calculate_modes_for_degrees(root_note, mode):
    root_scale = calculate_root_scale(root_note, mode)
    degrees_modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
    base_scale = calculate_major_scale(root_scale, mode="Ionian")

    print(f"Escala base (Ionian) desde {root_scale}: {base_scale['notes']}")
    for i, note in enumerate(base_scale["notes"]):
        mode_result = calculate_major_scale(note, mode=degrees_modes[i])
        print(f"Grado {i + 1} ({degrees_modes[i]}):")
        for n, interval, role in zip(mode_result["notes"], mode_result["intervals"], mode_result["roles"]):
            print(f"  {n}: {interval} - {role}")

def calculate_major_scale(root_note, mode="Ionian", chord_scale_type="standard", variation=None):
    chromatic_scale = [
        ["C", "B#", "Dbb"],  # 0
        ["C#", "Db", "B##"],  # 1
        ["D", "C##", "Ebb"],  # 2
        ["D#", "Eb", "Fbb"],  # 3
        ["E", "Fb", "D##"],  # 4
        ["F", "E#", "Gbb"],  # 5
        ["F#", "Gb", "E##"],  # 6
        ["G", "F##", "Abb"],  # 7
        ["G#", "Ab", "F###"],  # 8
        ["A", "G##", "Bbb"],  # 9
        ["A#", "Bb", "Cbb"],  # 10
        ["B", "Cb", "A##"]   # 11
    ]

    interval_names = {
        0: "Unín perfecto (1P)",
        1: "Segunda menor (2m) / Novena menor (b9)",
        2: "Segunda mayor (2M) / Novena mayor (9)",
        3: "Tercera menor (3m)",
        4: "Tercera mayor (3M)",
        5: "Cuarta justa (4J) / Oncena justa (11)",
        6: "Tritono (TT) / Quinta disminuida (b5) / Oncena aumentada (#11)",
        7: "Quinta justa (5J)",
        8: "Sexta menor (6m) / Trecena menor (b13)",
        9: "Sexta mayor (6M) / Trecena mayor (13)",
        10: "Séptima menor (7m)",
        11: "Séptima mayor (7M)",
        12: "Octava perfecta (8P)"
    }

    mode_definitions = {
        "Ionian": {
            "pattern": [2, 2, 1, 2, 2, 2, 1],
            "roles": {
                0: "Permitido",  # 1P
                2: "Permitido",  # 2M
                4: "Permitido",  # 3M
                5: "Evitado",    # 4J
                7: "Permitido",  # 5J
                9: "Permitido",  # 6M
                11: "Permitido"  # 7M
            }
        },
        "Dorian": {
            "pattern": [2, 1, 2, 2, 2, 1, 2],
            "roles": {
                0: "Permitido",  # 1P
                2: "Permitido",  # 2M
                3: "Permitido",  # 3m
                5: "Permitido",  # 4J
                7: "Permitido",  # 5J
                9: "Evitado",    # 6M
                10: "Permitido"  # 7m
            }
        },
        "Phrygian": {
            "pattern": [1, 2, 2, 2, 1, 2, 2],
            "roles": {
                0: "Permitido",  # 1P
                1: "Evitado",    # 2m
                3: "Permitido",  # 3m
                5: "Permitido",  # 4J
                7: "Permitido",  # 5J
                8: "Evitado",    # 6m
                10: "Permitido"  # 7m
            }
        },
        "Lydian": {
            "pattern": [2, 2, 2, 1, 2, 2, 1],
            "roles": {
                0: "Permitido",  # 1P
                2: "Permitido",  # 2M
                4: "Permitido",  # 3M
                6: "Permitido",  # TT
                7: "Permitido",  # 5J
                9: "Permitido",  # 6M
                11: "Permitido"  # 7M
            }     
        },
        "Mixolydian": {
            "pattern": [2, 2, 1, 2, 2, 1, 2],
            "roles": {
                0: "Permitido",  # 1P
                2: "Permitido",  # 2M
                4: "Permitido",  # 3M
                5: "Evitado",    # 4J
                7: "Permitido",  # 5J
                9: "Permitido",  # 6M
                10: "Permitido"  # 7m
            },
            "variations": {
                "sus4": {
                    "pattern": [2, 2, 1, 2, 2, 1, 2],
                    "roles": {
                        0: "Permitido",  # 1P
                        2: "Permitido",  # 2M
                        4: "Evitado",    # 3M
                        5: "Permitido",  # 4J
                        7: "Permitido",  # 5J
                        9: "Permitido",  # 6M
                        10: "Permitido"  # 7m
                    }
                },
                "7(b9,b13)": {
                    "pattern": [1, 3, 1, 2, 1, 2, 2],
                    "roles": {
                        0: "Permitido",  # 1P
                        1: "Permitido",  # b9
                        4: "Permitido",  # 3M
                        5: "Evitado",    # 4J
                        7: "Permitido (Excluyente)",  # 5J
                        8: "Permitido (Excluyente)",  # b13
                        10: "Permitido"  # 7m
                    }
                },
                "7(b9,#9,b13)": {
                    "pattern": [1, 2, 1, 1, 2, 1, 2],
                    "roles": {
                        0: "Permitido",  # 1P
                        1: "Permitido",  # b9
                        3: "Permitido",  # #9
                        4: "Permitido",  # 3M
                        5: "Evitado",    # 4J
                        7: "Permitido (Excluyente)",  # 5J
                        8: "Permitido (Excluyente)",  # b13
                        10: "Permitido"  # 7m
                    }
                },
                "7b5(b9,#9,b13)": {
                    "pattern": [1, 2, 1, 1, 2, 2, 2],
                    "roles": {
                        0: "Permitido",  # 1P
                        1: "Permitido",  # b9
                        3: "Permitido",  # #9
                        4: "Permitido",  # 3M
                        6: "Permitido",  # b5
                        8: "Permitido",  # b13
                        10: "Permitido"  # 7m
                    }
                },
                "7(b9,#9,#11,13)": {
                    "pattern": [1, 2, 1, 2, 2, 1, 2],
                    "roles": {
                        0: "Permitido",  # 1P
                        1: "Permitido",  # b9
                        3: "Permitido",  # #9
                        4: "Permitido",  # 3M
                        6: "Permitido",  # #11
                        7: "Permitido",  # 5J
                        9: "Permitido",  # 13
                        10: "Permitido"  # 7m
                    }
                }
            }
        },
        "Aeolian": {
            "pattern": [2, 1, 2, 2, 1, 2, 2],
            "roles": {
                0: "Permitido",  # 1P
                2: "Permitido",  # 2M
                3: "Permitido",  # 3m
                5: "Permitido",  # 4J
                7: "Permitido",  # 5J
                8: "Evitado",    # 6m
                10: "Permitido"  # 7m
            }
        },
        "Locrian": {
            "pattern": [1, 2, 2, 1, 2, 2, 2],
            "roles": {
                0: "Permitido",  # 1P
                1: "Evitado",    # 2m
                3: "Permitido",  # 3m
                5: "Permitido",  # 4J
                6: "Permitido",  # TT
                8: "Permitido",  # 6m
                10: "Permitido"  # 7m
            }
        }
    }

    if mode not in mode_definitions:
        raise ValueError(f"Modo inválido: {mode}. Modos disponibles: {', '.join(mode_definitions.keys())}")

    mode_data = mode_definitions[mode]

    if variation and "variations" in mode_data and variation in mode_data["variations"]:
        scale_pattern = mode_data["variations"][variation]["pattern"]
        chord_scale_roles = mode_data["variations"][variation]["roles"]
    else:
        scale_pattern = mode_data["pattern"]
        chord_scale_roles = mode_data["roles"]

    root_index = find_root_index(chromatic_scale, root_note)
    if root_index is None:
        raise ValueError(f"Nota raíz inválida: {root_note}.")

    scale_notes = []
    intervals = []
    roles = []
    used_letters = set()

    for interval, role in sorted(chord_scale_roles.items()):
        current_index = (root_index + interval) % 12
        note_options = chromatic_scale[current_index]

        if interval == 0:
            note = root_note
        else:
            note = note_options[0]
            for option in note_options:
                if option[0] not in used_letters:
                    note = option
                    break

        used_letters.add(note[0])
        scale_notes.append(note)
        intervals.append(interval_names.get(interval, "Desconocido"))
        roles.append(role)

    root_scale = calculate_root_scale(root_note, mode)

    return {"notes": scale_notes, "intervals": intervals, "roles": roles, "root_scale": root_scale}

if __name__ == "__main__":
    root_note = "C"
    mode = "Ionian"
    result = calculate_major_scale(root_note, mode=mode)

    print(f"Escala {mode} desde {root_note}:")
    for note, interval, role in zip(result["notes"], result["intervals"], result["roles"]):
        print(f"{note}: {interval} - {role}")

    print(f"Escala raíz: {result['root_scale']}")

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
