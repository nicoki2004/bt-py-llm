"""
Test write_file
"""

import os

from functions.write_file_content import write_file


def run_tests():
    # Asegurarnos de que el working directory existe para las pruebas
    os.makedirs("calculator", exist_ok=True)

    print("--- Test 1: Overwriting existing file ---")
    # Escribirá en calculator/lorem.txt
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    print("\n--- Test 2: Writing to a new subdirectory ---")
    # Debe crear 'pkg' si no existe y escribir morelorem.txt
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("\n--- Test 3: Security check (outside directory) ---")
    # Debe fallar porque /tmp está fuera de calculator
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    # Extra: Verificar si el contenido se escribió realmente
    print("\n--- Verification of Test 2 ---")
    if os.path.exists("calculator/pkg/morelorem.txt"):
        with open("calculator/pkg/morelorem.txt", "r") as f:
            print(f"File content: {f.read()}")


if __name__ == "__main__":
    run_tests()
