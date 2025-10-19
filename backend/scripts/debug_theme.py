#!/usr/bin/env python3
import sys
import os

print("=== DEBUG THEME GENERATION ===")
print("Python path:", sys.executable)
print("Current dir:", os.getcwd())

try:
    from astro_calcule import generate_theme

    print("✓ astro_calcule imported successfully")

    test_path = "/home/gaby/AstroSource/data/Utilisateurs/yopa/theme_simple.json"
    print(f"Test path: {test_path}")
    print(f"Parent dir: {os.path.dirname(test_path)}")
    print(f"Parent exists before: {os.path.exists(os.path.dirname(test_path))}")

    # Créer le répertoire manuellement
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    print(f"Parent exists after makedirs: {os.path.exists(os.path.dirname(test_path))}")

    print("Calling generate_theme...")
    result = generate_theme("yopa", "15/06/1985", "14:30", "Paris", "France", test_path)
    print(f"Result: {result}")
    print(f"File exists after generation: {os.path.exists(test_path)}")

    if os.path.exists(test_path):
        with open(test_path, "r") as f:
            content = f.read()
            print(f"File size: {len(content)} chars")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback

    traceback.print_exc()
