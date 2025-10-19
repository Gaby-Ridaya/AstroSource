import os, random
from PIL import Image


def select_reference_images(signs, count=3):
    import logging

    categories = ["portraits", "paysages", "symboles", "abstrait"]
    image_paths = set()

    # Recherche dynamique du dossier 'resin' en remontant l'arborescence
    current_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = None
    while True:
        if os.path.isdir(os.path.join(current_dir, "resin")):
            project_root = current_dir
            break
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            raise RuntimeError(
                "Impossible de trouver le dossier 'resin' dans l'arborescence."
            )
        current_dir = parent
    for sign in signs:
        # On force la majuscule initiale pour correspondre aux dossiers sur disque
        sign_dir = sign.capitalize()
        base_dir = os.path.join(project_root, "resin", "prompts", sign_dir, "images")
        logging.warning(
            f"[select_reference_images] Signe: {sign} | Dossier: {base_dir}"
        )
        random.shuffle(categories)  # pour varier l’ordre à chaque appel

        for cat in categories:
            cat_dir = os.path.join(base_dir, cat)
            logging.warning(
                f"[select_reference_images]  Catégorie: {cat} | Dossier: {cat_dir}"
            )
            if os.path.isdir(cat_dir):
                imgs = [
                    os.path.join(cat_dir, f)
                    for f in os.listdir(cat_dir)
                    if f.lower().endswith(("png", "jpg", "jpeg"))
                ]
                logging.warning(f"[select_reference_images]   Images trouvées: {imgs}")
                if imgs:
                    chosen = random.choice(imgs)
                    logging.warning(
                        f"[select_reference_images]   Image choisie: {chosen}"
                    )
                    image_paths.add(chosen)
                    if len(image_paths) >= count:
                        logging.warning(
                            f"[select_reference_images]   Assez d'images, retour: {list(image_paths)}"
                        )
                        return list(image_paths)
            else:
                logging.warning(
                    f"[select_reference_images]   Dossier non trouvé: {cat_dir}"
                )

    logging.warning(f"[select_reference_images] Images finales: {list(image_paths)}")
    return list(image_paths)


def create_moodboard(image_paths, output_path):
    images = [Image.open(p).convert("RGB") for p in image_paths]
    moodboard = Image.new("RGB", (1024, 1024), (0, 0, 0))

    if len(images) == 3:
        images[0] = images[0].resize((512, 1024))
        images[1] = images[1].resize((512, 512))
        images[2] = images[2].resize((512, 512))
        moodboard.paste(images[0], (0, 0))
        moodboard.paste(images[1], (512, 0))
        moodboard.paste(images[2], (512, 512))
    elif len(images) == 4:
        for i, img in enumerate(images):
            img = img.resize((512, 512))
            x = (i % 2) * 512
            y = (i // 2) * 512

            import os
            from PIL import Image

            img = img.resize((1024 // len(images), 1024))
