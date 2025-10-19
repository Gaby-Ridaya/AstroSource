import os, shutil


def archive_results(user_id, json_path, image_path, moodboard_path, prompt):
    user_dir = f"app/data/{user_id}"
    os.makedirs(user_dir, exist_ok=True)

    shutil.copy(json_path, os.path.join(user_dir, "theme.json"))
    shutil.copy(image_path, os.path.join(user_dir, "generated.png"))
    shutil.copy(moodboard_path, os.path.join(user_dir, "moodboard.png"))

    with open(os.path.join(user_dir, "prompt.txt"), "w") as f:
        f.write(prompt)
