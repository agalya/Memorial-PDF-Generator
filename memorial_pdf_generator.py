# -*- coding: utf-8 -*-
"""
Memorial PDF Generator - Core PDF Generation Module
Generates PDFs with customizable title, poem, dates, author name, and images.
Can auto-detect optimal column layout or use specified columns.

Copyright (c) 2026 Agalya

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
import io
import tempfile
import urllib.request
from PIL import Image
from fpdf import FPDF

# ─────────────────────────────────────────────
#  CONFIGURATION (adjustable)
# ─────────────────────────────────────────────

PAGE_W, PAGE_H = 210, 297  # A4 mm
MARGIN = 12
BG = (22, 28, 48)
GOLD = (180, 155, 90)
TEXT = (255, 255, 255)
AUTHOR_COLOR = (255, 255, 255)
AUTHOR_BG = (30, 38, 62)  # No longer used since background removed
AUTHOR_SEPARATOR_MM = 8.0   # Thin gold rule above author (≈ mm); ~full column width used if wider

FONT_CACHE = os.path.join(tempfile.gettempdir(), "NotoSansTamil-Regular.ttf")
FONT_CACHE_BOLD = os.path.join(tempfile.gettempdir(), "NotoSansTamil-Bold.ttf")
FONT_URL = (
    "https://github.com/googlefonts/noto-fonts/raw/main/"
    "hinted/ttf/NotoSansTamil/NotoSansTamil-Regular.ttf"
)
FONT_URL_BOLD = (
    "https://github.com/googlefonts/noto-fonts/raw/main/"
    "hinted/ttf/NotoSansTamil/NotoSansTamil-Bold.ttf"
)


def ensure(pkg, import_as=None):
    try:
        __import__(import_as or pkg)
    except ImportError:
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg, "-q"],
            stdout=subprocess.DEVNULL,
        )


# Ensure dependencies
try:
    from fpdf import FPDF
    from PIL import Image
except ImportError:
    ensure("fpdf2", "fpdf")
    ensure("uharfbuzz")
    ensure("Pillow", "PIL")
    from fpdf import FPDF
    from PIL import Image


def get_tamil_fonts():
    """Download Tamil regular and bold fonts if not cached."""
    if not (os.path.exists(FONT_CACHE) and os.path.getsize(FONT_CACHE) > 50_000):
        print("Downloading Tamil regular font (one-time)…")
        urllib.request.urlretrieve(FONT_URL, FONT_CACHE)
    if not (os.path.exists(FONT_CACHE_BOLD) and os.path.getsize(FONT_CACHE_BOLD) > 50_000):
        print("Downloading Tamil bold font (one-time)…")
        urllib.request.urlretrieve(FONT_URL_BOLD, FONT_CACHE_BOLD)
    return FONT_CACHE, FONT_CACHE_BOLD


def load_image_from_bytes(image_bytes):
    """Load image from bytes."""
    if not image_bytes:
        return None
    try:
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        return None


def load_image_from_path(path):
    """Load image from file path."""
    if not path or not os.path.exists(path):
        return None
    try:
        return Image.open(path).convert("RGB")
    except Exception:
        return None


def read_poet_lines(poet_text):
    """Split author name on Enter/newlines."""
    return [line.strip() for line in poet_text.strip().splitlines() if line.strip()]


def top_photo_dimensions(img, content_w, photo_height_mm=72):
    """Calculate photo dimensions preserving aspect ratio."""
    box_w = content_w
    box_h = photo_height_mm

    if not img:
        return box_w, box_h

    iw, ih = img.size
    if iw <= 0 or ih <= 0:
        return box_w, box_h

    aspect = ih / iw
    w, h = box_w, box_w * aspect
    if h > box_h:
        h = box_h
        w = h / aspect
    return w, h


def save_temp_jpeg(img, tag, quality=88):
    """Save image to temp file."""
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    path = os.path.join(tempfile.gettempdir(), f"memorial_{tag}.jpg")
    with open(path, "wb") as f:
        f.write(buf.getvalue())
    return path


def make_poem_background(photo, box_w_px, box_h_px, opacity, bg_rgb=BG):
    """Create watermark from photo with opacity."""
    scale = max(box_w_px / photo.width, box_h_px / photo.height)
    resized = photo.resize(
        (max(1, int(photo.width * scale)), max(1, int(photo.height * scale))),
        Image.LANCZOS,
    )
    left = (resized.width - box_w_px) // 2
    top = (resized.height - box_h_px) // 2
    cropped = resized.crop((left, top, left + box_w_px, top + box_h_px)).convert("RGB")

    opacity = max(0.05, min(1.0, opacity))
    if opacity >= 0.99:
        return cropped

    base = Image.new("RGBA", (box_w_px, box_h_px), (*bg_rgb, 255))
    layer = cropped.convert("RGBA")
    layer.putalpha(int(opacity * 255))
    base.paste(layer, (0, 0), layer)
    return base.convert("RGB")


def add_tamil_font(pdf, regular_font_path, bold_font_path):
    """Add Tamil regular and bold fonts to PDF."""
    pdf.add_font("Tamil", "", regular_font_path)
    pdf.add_font("Tamil", "B", bold_font_path)


def text_width(pdf, text, size, bold=False):
    """Get text width in mm (Tamil shaping)."""
    pdf.set_font("Tamil", style="B" if bold else "", size=size)
    return pdf.get_string_width(text)


def author_font_pts(body_pts):
    """Author signature strictly smaller than body (min 5 pt)."""
    pt = max(5, body_pts - 2)
    if pt >= body_pts:
        pt = body_pts - 1
    return max(5, pt)


def measure_generator_header_mm(
    pdf, title, dates_text, title_pt, title_lh, content_w
):
    """Height (mm) from below photo block to poem area (matches draw order)."""
    y = 0.0
    if title.strip():
        tlh = title_lh + 1.0
        for line in wrap_tamil(pdf, title, title_pt, content_w, bold=True):
            y += tlh * 0.35 if not line.strip() else tlh
    y += 1.0
    if dates_text:
        for line in wrap_tamil(pdf, dates_text, 11, content_w, bold=False):
            y += 6 * 0.35 if not line.strip() else 6.0
        y += 1.0
    y += 7.0
    return y


def header_layout(poem_text, title):
    """Calculate optimal title size based on poem length."""
    n = len([ln for ln in poem_text.splitlines() if ln.strip()])
    title_size, title_lh = 20, 11
    if n > 28:
        title_size, title_lh = 19, 11
    if n > 38:
        title_size, title_lh = 17, 10
    if n > 48:
        title_size, title_lh = 15, 9
    if len(title) > 36:
        title_size = min(title_size, 16)
        title_lh = min(title_lh, 10)
    return title_size, title_lh


def line_block_height(poem_lines, line_h, blank_factor=0.38):
    """Calculate total height of text block."""
    h = 0.0
    for line in poem_lines:
        h += line_h * blank_factor if not line.strip() else line_h
    return h


def append_poet_to_right_column(right, poet_lines):
    """Add author lines to right column."""
    if not poet_lines:
        return right, None
    out = list(right)
    if out:
        out.append("")
    out.extend(poet_lines)
    return out, len(out) - len(poet_lines)


def split_into_columns(lines, right_extra_lines=0):
    """Split text into two balanced columns."""
    n = len(lines)
    if n <= 1:
        return lines, []

    target_left = max(1, min(n - 1, (n + right_extra_lines + 1) // 2))

    def split_score(idx):
        left_n = idx
        right_n = n - idx
        balance = abs(left_n - (right_n + right_extra_lines))
        if idx > 0 and not lines[idx - 1].strip():
            balance -= 1.5
        if idx < n and not lines[idx].strip():
            balance -= 0.5
        return balance

    best_idx = target_left
    best_score = split_score(best_idx)
    window = max(10, n // 4)
    for idx in range(max(1, target_left - window), min(n, target_left + window + 1)):
        score = split_score(idx)
        if score < best_score:
            best_score = score
            best_idx = idx

    left = lines[:best_idx]
    right = lines[best_idx:]
    while right and not right[0].strip():
        right = right[1:]
    while left and not left[-1].strip():
        left = left[:-1]
    return left, right


def two_column_height(left, right, line_h, blank_factor=0.38):
    """Calculate height of two-column layout."""
    rows = max(len(left), len(right))
    h = 0.0
    for i in range(rows):
        left_ln = left[i] if i < len(left) else ""
        right_ln = right[i] if i < len(right) else ""
        if not left_ln.strip() and not right_ln.strip():
            h += line_h * blank_factor
        else:
            h += line_h
    return h


def column_widths(content_w, num_cols=2, gutter=5):
    """Calculate column widths."""
    if num_cols < 2:
        return content_w - 4, 0, 0
    col_w = (content_w - gutter) / 2
    left_x = MARGIN
    right_x = MARGIN + col_w + gutter
    return col_w, left_x, right_x


def wrap_tamil(pdf, text, size, max_w_mm, bold=False):
    """Wrap text to fit width."""
    lines_out = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            lines_out.append("")
            continue
        words = paragraph.split()
        if len(words) > 1:
            current = ""
            for word in words:
                test = f"{current} {word}".strip()
                if text_width(pdf, test, size, bold=bold) <= max_w_mm:
                    current = test
                else:
                    if current:
                        lines_out.append(current)
                    current = word
            if current:
                lines_out.append(current)
            continue
        current = ""
        for ch in paragraph:
            test = current + ch
            if text_width(pdf, test, size, bold=bold) <= max_w_mm:
                current = test
            else:
                if current:
                    lines_out.append(current)
                current = ch
        if current:
            lines_out.append(current)
    return lines_out


def fit_poem_layout(pdf, poem_text, poet_lines, content_w, area_h_mm, num_cols=2, gutter=5):
    """Fit poem to available space, choosing font size."""
    col_w, _, _ = column_widths(content_w, num_cols, gutter)
    wrap_w = col_w - 2 if num_cols >= 2 else content_w - 4
    best = None

    line_count = len([ln for ln in poem_text.splitlines() if ln.strip()])
    if num_cols < 2:
        max_size = 40 if line_count <= 2 else 34 if line_count <= 4 else 30
    else:
        max_size = 32 if line_count <= 3 else 28

    for poem_size in range(max_size, 5, -1):
        line_h = max(2.6, poem_size * 0.50)
        poet_size = author_font_pts(poem_size)
        poet_line_h = max(3.5, poet_size * 0.50)
        wrapped = wrap_tamil(pdf, poem_text, poem_size, wrap_w)

        poet_start = None
        if num_cols >= 2:
            poet_extra = len(poet_lines) + (1 if poet_lines else 0)
            left, right = split_into_columns(wrapped, right_extra_lines=poet_extra)
            right, poet_start = append_poet_to_right_column(right, poet_lines)
            total = two_column_height(left, right, line_h)
        else:
            left, right = wrapped, []
            total = line_block_height(wrapped, line_h)
            if poet_lines:
                total += 2 + len(poet_lines) * poet_line_h

        if total <= area_h_mm - 1:
            best = (poem_size, line_h, left, right, poet_size, poet_line_h, poet_start)
            break
        best = (poem_size, line_h, left, right, poet_size, poet_line_h, poet_start)

    if best is None:
        poem_size, line_h = 6, 2.6
        wrapped = wrap_tamil(pdf, poem_text, poem_size, wrap_w)
        if num_cols >= 2:
            poet_extra = len(poet_lines) + (1 if poet_lines else 0)
            left, right = split_into_columns(wrapped, right_extra_lines=poet_extra)
            right, poet_start = append_poet_to_right_column(right, poet_lines)
        else:
            left, right = wrapped, []
            poet_start = None
        ps = author_font_pts(poem_size)
        best = (poem_size, line_h, left, right, ps, max(3.5, ps * 0.50), poet_start)
    return best


def draw_poem_columns(
    pdf,
    left,
    right,
    text_y,
    col_w,
    left_x,
    right_x,
    poem_size,
    line_h,
    poet_size=None,
    poet_row_start=None,
    author_separator_mm=AUTHOR_SEPARATOR_MM,
):
    """Draw poem in two columns. Optional thin line before author lines (right column)."""
    blank_gap = line_h * 0.38
    rows = max(len(left), len(right))
    if poet_size is None:
        poet_size = poem_size
    poet_row_start = poet_row_start if poet_row_start is not None else rows + 1

    for i in range(rows):
        left_ln = left[i] if i < len(left) else ""
        right_ln = right[i] if i < len(right) else ""

        if i == poet_row_start and poet_row_start < rows:
            text_y += 0.6
            pdf.set_draw_color(*GOLD)
            pdf.set_line_width(0.1)
            inset = max(1.0, col_w * 0.06)
            line_w = max(author_separator_mm, col_w - 2 * inset)
            seg_left = right_x + col_w - line_w - inset
            pdf.line(seg_left, text_y, seg_left + line_w, text_y)
            text_y += 1.4

        step = (
            blank_gap
            if not left_ln.strip() and not right_ln.strip()
            else line_h
        )

        pdf.set_font("Tamil", size=poem_size)
        pdf.set_text_color(*TEXT)
        pdf.set_xy(left_x, text_y)
        pdf.cell(col_w, step, left_ln, align="L")

        is_author = i >= poet_row_start
        if is_author:
            pdf.set_font("Tamil", size=poet_size)
            pdf.set_text_color(*AUTHOR_COLOR)
            right_align = "R"
        else:
            pdf.set_font("Tamil", size=poem_size)
            pdf.set_text_color(*TEXT)
            right_align = "L"
        pdf.set_xy(right_x, text_y)
        pdf.cell(col_w, step, right_ln, align=right_align)
        text_y += step
    return text_y


def draw_centered_lines(pdf, y, text, size, color=TEXT, line_h=None, max_w=None):
    """Draw centered text."""
    if not text.strip():
        return y
    line_h = line_h or size * 0.55
    max_w = max_w or (PAGE_W - 2 * MARGIN)
    for line in wrap_tamil(pdf, text, size, max_w):
        if not line.strip():
            y += line_h * 0.35
            continue
        pdf.set_font("Tamil", size=size)
        pdf.set_text_color(*color)
        pdf.set_xy(MARGIN, y)
        pdf.cell(PAGE_W - 2 * MARGIN, line_h, line, align="C")
        y += line_h
    return y


def auto_detect_columns(poem_text):
    """Auto-detect optimal column count based on poem length."""
    line_count = len([ln for ln in poem_text.splitlines() if ln.strip()])
    # Use 2 columns for longer poems, 1 for shorter
    return 2 if line_count > 20 else 1


def generate_memorial_pdf(
    title="Memorial",
    dates="",
    poem="",
    author="",
    photo_data=None,
    photo_path=None,
    background_photo_data=None,
    num_columns=0,  # 0=auto-detect, 1 or 2 for fixed
    opacity=1.0,
    gutter=5,
    footer_text="என்றும் நினைவில் வாழ்கிறீர்கள்",
):
    """
    Generate memorial PDF with given parameters.
    
    Args:
        title: Memorial title (also used for PDF filename)
        dates: Date string (optional)
        poem: Poem text (required)
        author: Author name(s) - can be multi-line
        photo_data: Image bytes for top photo (JPG/PNG)
        photo_path: Path to image file for top photo (alternative to photo_data)
        background_photo_data: Image bytes for poem watermark (optional, overrides auto-selection)
        num_columns: 0 for auto-detect, 1 or 2 for fixed layout
        opacity: Watermark opacity (0.0-1.0)
        gutter: Space between columns in mm
        footer_text: Text for page footer
    
    Returns:
        PDF as bytes
    
    Note:
        If num_columns auto-detects:
        - 1 column layout looks for "uncle_1_col.jpg"
        - 2 column layout looks for "uncle_2_col.jpg"
    """
    
    regular_font_path, bold_font_path = get_tamil_fonts()
    poem_text = poem.strip()
    dates_text = dates.strip()
    author_text = author.strip()
    
    if not poem_text:
        raise ValueError("Poem text is required")
    
    # Load photo for top of page
    top_photo = None
    if photo_data:
        top_photo = load_image_from_bytes(photo_data)
    elif photo_path:
        top_photo = load_image_from_path(photo_path)
    
    # Auto-detect columns if needed (before loading background image)
    if num_columns <= 0:
        num_columns = auto_detect_columns(poem_text)
    
    # Load background photo for watermark behind poem (disabled)
    background_photo = None
    # if num_columns >= 2:
    #     if background_photo_data:
    #         background_photo = load_image_from_bytes(background_photo_data)
    #     else:
    #         # Use background image only for 2-column layout
    #         bg_path = "uncle_3_col.jpg"
    #         background_photo = load_image_from_path(bg_path)
    
    # Create PDF
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    pdf.set_text_shaping(True)
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.add_page()
    
    add_tamil_font(pdf, regular_font_path, bold_font_path)
    
    # Background
    pdf.set_fill_color(*BG)
    pdf.rect(0, 0, PAGE_W, PAGE_H, style="F")
    
    y = MARGIN
    content_w = PAGE_W - 2 * MARGIN
    poet_lines = read_poet_lines(author_text)
    base_title_pts, title_lh = header_layout(poem_text, title)
    footer_h = 8
    poem_bottom = PAGE_H - MARGIN - footer_h
    
    # Top photo
    if top_photo:
        photo_w, photo_h = top_photo_dimensions(top_photo, content_w)
        photo_x = MARGIN + (content_w - photo_w) / 2
        frame = 1.2
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.45)
        pdf.rect(
            photo_x - frame,
            y - frame,
            photo_w + 2 * frame,
            photo_h + 2 * frame,
            style="D",
        )
        tmp_top = save_temp_jpeg(top_photo, "top")
        pdf.image(tmp_top, x=photo_x, y=y, w=photo_w, h=photo_h)
        y += photo_h + 6
    
    y_after_photo = y

    # Title > poem body > author — converge header height vs poem area
    title_i = int(min(26, max(base_title_pts, 14)))
    poem_size = 11
    line_h = 8
    left_col, right_col = [], []
    poet_size, poet_line_h, poet_row_start = 5, 6, None
    for _ in range(8):
        header_mm = measure_generator_header_mm(
            pdf, title, dates_text, title_i, title_lh, content_w
        )
        area_try = poem_bottom - y_after_photo - header_mm
        if area_try < 28:
            area_try = 28
        poem_size, line_h, left_col, right_col, poet_size, poet_line_h, poet_row_start = (
            fit_poem_layout(
                pdf, poem_text, poet_lines, content_w, area_try, num_columns, gutter
            )
        )
        title_next = int(min(26, max(base_title_pts, poem_size + 3)))
        if title_next == title_i:
            break
        title_i = title_next

    title_final = int(min(26, max(title_i, base_title_pts, poem_size + 3)))

    # Title (bold; wrap widths use bold Tamil)
    if title.strip():
        title_line_h = title_lh + 1
        pdf.set_font("Tamil", style="B", size=title_final)
        pdf.set_text_color(255, 255, 255)
        for line in wrap_tamil(pdf, title, title_final, content_w, bold=True):
            if not line.strip():
                y += title_line_h * 0.35
                continue
            pdf.set_xy(MARGIN, y)
            pdf.cell(content_w, title_line_h, line, align="C")
            y += title_line_h
    y += 1
    
    # Dates
    if dates_text:
        y = draw_centered_lines(pdf, y, dates_text, size=11, color=GOLD, line_h=6)
        y += 1
    
    # Divider
    div_y = y + 2
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.25)
    mid = PAGE_W / 2
    pdf.line(MARGIN + 8, div_y, mid - 4, div_y)
    pdf.line(mid + 4, div_y, PAGE_W - MARGIN - 8, div_y)
    pdf.set_font("Tamil", size=10)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(0, div_y - 3)
    pdf.cell(PAGE_W, 5, "✦", align="C")
    y = div_y + 5
    
    poem_area_h = poem_bottom - y
    col_w, col_left_x, col_right_x = column_widths(content_w, num_columns, gutter)
    
    poem_size, line_h, left_col, right_col, poet_size, poet_line_h, poet_row_start = (
        fit_poem_layout(pdf, poem_text, poet_lines, content_w, poem_area_h, num_columns, gutter)
    )
    
    # Watermark behind poem (disabled)
    # if background_photo and poem_area_h > 25:
    #     px = int(content_w * 11.81)
    #     py = int(poem_area_h * 11.81)
    #     wm = make_poem_background(background_photo, px, py, opacity)
    #     wm_path = save_temp_jpeg(wm, "watermark", quality=92)
    #     pdf.image(wm_path, x=0, y=y, w=PAGE_W, h=poem_area_h)
    
    # Poem layout
    if num_columns >= 2:
        body_h = two_column_height(left_col, right_col, line_h)
        total_text_h = body_h
    else:
        body_h = line_block_height(left_col, line_h)
        poet_block_h = (2 + len(poet_lines) * poet_line_h) if poet_lines else 0
        total_text_h = body_h + poet_block_h
    
    if total_text_h >= poem_area_h * 0.92:
        text_y = y + 1
    else:
        text_y = y + max(1, (poem_area_h - total_text_h) / 2)
    
    # Column separator
    if num_columns >= 2 and col_right_x:
        sep_x = MARGIN + col_w + gutter / 2
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.15)
        pdf.line(sep_x, text_y, sep_x, y + poem_area_h - 2)
    
    # Draw poem
    if num_columns >= 2:
        text_y = draw_poem_columns(
            pdf,
            left_col,
            right_col,
            text_y,
            col_w,
            col_left_x,
            col_right_x,
            poem_size,
            line_h,
            poet_size=poet_size,
            poet_row_start=poet_row_start,
        )
    else:
        blank_gap = line_h * 0.38
        pdf.set_font("Tamil", size=poem_size)
        pdf.set_text_color(*TEXT)
        for line in left_col:
            step = blank_gap if not line.strip() else line_h
            pdf.set_xy(MARGIN, text_y)
            pdf.cell(content_w, step, line, align="L")
            text_y += step
    
    # Author in single column
    if poet_lines and num_columns < 2:
        text_y += 1.5
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.1)
        line_len = min(max(52.0, AUTHOR_SEPARATOR_MM * 6.5), content_w - 24)
        x1 = PAGE_W - MARGIN - line_len
        x2 = PAGE_W - MARGIN
        pdf.line(x1, text_y, x2, text_y)
        text_y += 2.0
        pdf.set_font("Tamil", size=poet_size)
        for line in poet_lines:
            pdf.set_text_color(*AUTHOR_COLOR)
            pdf.set_xy(MARGIN, text_y)
            pdf.cell(content_w, poet_line_h, line, align="R")
            text_y += poet_line_h
    
    # Footer
    foot_y = PAGE_H - MARGIN - 4
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.2)
    pdf.line(MARGIN, foot_y - 3, PAGE_W - MARGIN, foot_y - 3)
    draw_centered_lines(
        pdf,
        foot_y,
        footer_text,
        size=8,
        color=(130, 115, 80),
        line_h=5,
    )
    
    # Return PDF as bytes
    return pdf.output()


if __name__ == "__main__":
    # Test: Generate sample PDF
    sample_poem = """நீ சென்றாலும் நினைவுகள் நிலைக்கும்,
உன் அன்பு என்றும் மனதில் வாழும்.
கண்ணீரால் விடைகொடுக்கிறோம்,
இதயத்தில் என்றும் வாழ்கிறாய்."""

    pdf_bytes = generate_memorial_pdf(
        title="Test Memorial",
        dates="18 - மே - 2026",
        poem=sample_poem,
        author="Test Author",
    )
    
    with open("test_output.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("Test PDF saved: test_output.pdf")
