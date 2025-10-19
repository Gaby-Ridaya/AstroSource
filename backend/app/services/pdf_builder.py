# backend/app/services/temp/pdf_builder.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors

DEFAULTS = {
    "font_main": "Times-Roman",
    "font_bold": "Times-Bold",
    "font_small": "Times-Roman",
    "title_size": 24,
    "subtitle_size": 13,
    "text_size": 11,
    "small_size": 9,
    "margin_x_cm": 2.2,
    "margin_y_cm": 2.2,
    "header_h_cm": 1.8,
    "footer_h_cm": 1.2,
    "line_h": 16,
    "body_leading_space_cm": 0.5,
    "max_chars": 96,
    "bullet_indent_cm": 0.7,
    "header_line_rgb": (0.18, 0.45, 0.68),
    "rule_rgb": (0.18, 0.45, 0.68),
}


def _get_meta(theme_json, json_path):
    meta = {"nom": "—", "ville": "—", "date": "—", "heure": "—"}
    if isinstance(theme_json, dict):
        m = theme_json.get("meta") or {}
        meta["nom"] = m.get("nom") or m.get("name") or meta["nom"]
        meta["ville"] = (
            m.get("ville") or m.get("city") or m.get("lieu") or meta["ville"]
        )
        meta["date"] = m.get("date") or m.get("date_naissance") or meta["date"]
        meta["heure"] = m.get("heure") or m.get("heure_naissance") or meta["heure"]
    user_dir = os.path.dirname(json_path or "")
    if meta["nom"] == "—" and user_dir:
        meta["nom"] = os.path.basename(user_dir)
    return meta


def make_pdf_pro(
    *,
    theme_json,
    txt_path,
    pdf_path,
    json_path=None,
    title="Interprétations astrologiques",
    subtitle="AstroSource",
    options=None,
):
    opt = dict(DEFAULTS)
    opt.update(options or {})
    meta = _get_meta(theme_json, json_path)
    text = open(txt_path, "r", encoding="utf-8").read()

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    FONT_MAIN, FONT_BOLD, FONT_SMALL = (
        opt["font_main"],
        opt["font_bold"],
        opt["font_small"],
    )
    TITLE_SIZE, SUBTITLE_SIZE, TEXT_SIZE, SMALL_SIZE = (
        opt["title_size"],
        opt["subtitle_size"],
        opt["text_size"],
        opt["small_size"],
    )
    margin_x, margin_y = opt["margin_x_cm"] * cm, opt["margin_y_cm"] * cm
    header_h, footer_h = opt["header_h_cm"] * cm, opt["footer_h_cm"] * cm
    line_h = opt["line_h"]
    body_top, body_bottom = height - margin_y - header_h, margin_y + footer_h

    def draw_header(page_no: int):
        r, g, b = opt["header_line_rgb"]
        c.setStrokeColorRGB(r, g, b)
        c.setLineWidth(1)
        c.line(
            margin_x,
            height - margin_y - 0.3 * cm,
            width - margin_x,
            height - margin_y - 0.3 * cm,
        )
        c.setFont(FONT_SMALL, SMALL_SIZE)
        c.setFillColor(colors.black)
        c.drawString(
            margin_x,
            height - margin_y - header_h + 0.2 * cm,
            f"{meta['nom']}  —  {meta['ville']}  —  {meta['date']} {meta['heure']}",
        )

    def draw_footer(page_no: int):
        c.setFillColor(colors.grey)
        c.setFont(FONT_SMALL, SMALL_SIZE)
        c.drawRightString(width - margin_x, margin_y - 0.2 * cm, f"Page {page_no}")

    # Page de garde
    c.setFillColor(colors.black)
    c.setFont(FONT_BOLD, TITLE_SIZE)
    title_y = height - margin_y - 3.0 * cm
    c.drawString(margin_x, title_y, title)
    c.setFont(FONT_MAIN, SUBTITLE_SIZE)
    c.setFillColor(colors.darkgrey)
    subtitle_y = title_y - 1.2 * cm
    c.drawString(margin_x, subtitle_y, subtitle)

    # Bloc méta
    c.setFillColor(colors.black)
    c.setFont(FONT_MAIN, TEXT_SIZE)
    block_top = subtitle_y - 1.6 * cm
    c.roundRect(
        margin_x,
        block_top - 3.2 * cm,
        width - 2 * margin_x,
        3.2 * cm,
        10,
        stroke=1,
        fill=0,
    )
    c.drawString(margin_x + 0.6 * cm, block_top - 0.6 * cm, f"Nom : {meta['nom']}")
    c.drawString(margin_x + 0.6 * cm, block_top - 1.2 * cm, f"Ville : {meta['ville']}")
    c.drawString(
        margin_x + 0.6 * cm,
        block_top - 1.8 * cm,
        f"Date/Heure : {meta['date']} {meta['heure']}",
    )

    # Filet
    r, g, b = opt["rule_rgb"]
    c.setStrokeColorRGB(r, g, b)
    c.setLineWidth(2)
    c.line(margin_x, block_top - 3.6 * cm, width - margin_x, block_top - 3.6 * cm)

    draw_footer(1)
    c.showPage()

    # Pages de contenu
    import textwrap

    page_no = 2
    c.setFont(FONT_MAIN, TEXT_SIZE)
    c.setFillColor(colors.black)
    draw_header(page_no)
    current_y = body_top - opt["body_leading_space_cm"] * cm
    max_chars = opt["max_chars"]
    bullet_indent = opt["bullet_indent_cm"] * cm
    wrap_width_pt = width - 2 * margin_x

    def new_page():
        nonlocal page_no, current_y
        draw_footer(page_no)
        c.showPage()
        page_no += 1
        c.setFont(FONT_MAIN, TEXT_SIZE)
        c.setFillColor(colors.black)
        draw_header(page_no)
        current_y = body_top - opt["body_leading_space_cm"] * cm

    def draw_justified_line(x, y, line, max_width):
        words = line.split()
        if len(words) <= 1:
            c.drawString(x, y, line)
            return
        w = sum(
            c.stringWidth(wd, FONT_MAIN, TEXT_SIZE) for wd in words
        ) + c.stringWidth(" ", FONT_MAIN, TEXT_SIZE) * (len(words) - 1)
        if w >= max_width * 0.92:
            c.drawString(x, y, line)
            return
        base_space = c.stringWidth(" ", FONT_MAIN, TEXT_SIZE)
        missing = max_width - w
        extra_per_gap = missing / (len(words) - 1)
        cx = x
        for i, wd in enumerate(words):
            c.drawString(cx, y, wd)
            cx += c.stringWidth(wd, FONT_MAIN, TEXT_SIZE)
            if i < len(words) - 1:
                cx += base_space + extra_per_gap

    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        p = paragraph.rstrip()
        if not p:
            current_y -= line_h
            if current_y < body_bottom:
                new_page()
            continue

        is_bullet = p.lstrip().startswith("- ")
        if is_bullet:
            content = p.lstrip()[2:].strip()
            wrapped = textwrap.wrap(content, width=max_chars)
            for i, line in enumerate(wrapped):
                x = margin_x + bullet_indent
                if i == 0:
                    c.drawString(margin_x, current_y, "•")
                if i == len(wrapped) - 1:
                    c.drawString(x, current_y, line)
                else:
                    draw_justified_line(
                        x, current_y, line, wrap_width_pt - bullet_indent
                    )
                current_y -= line_h
                if current_y < body_bottom:
                    new_page()
            current_y -= 4
            if current_y < body_bottom:
                new_page()
            continue

        wrapped = textwrap.wrap(p, width=max_chars)
        for j, line in enumerate(wrapped):
            if j == len(wrapped) - 1:
                c.drawString(margin_x, current_y, line)
            else:
                draw_justified_line(margin_x, current_y, line, wrap_width_pt)
            current_y -= line_h
            if current_y < body_bottom:
                new_page()
        current_y -= 6
        if current_y < body_bottom:
            new_page()

    draw_footer(page_no)
    c.showPage()
    c.save()
