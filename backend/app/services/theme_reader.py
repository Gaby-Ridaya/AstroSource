import json


def get_zodiac_sign(degree, sign_boundaries):
    for sign, start_deg in reversed(
        sorted(sign_boundaries.items(), key=lambda x: x[1])
    ):
        if degree >= start_deg:
            return sign
    return "Pisces"  # fallback par défaut


def extract_sun_and_asc_signs(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    sun_deg = data["planetes"]["Sun"]
    asc_deg = data["ascendant"]
    signs = data["signes"]

    sun_sign = get_zodiac_sign(sun_deg, signs)
    asc_sign = get_zodiac_sign(asc_deg, signs)

    return sun_sign, asc_sign
