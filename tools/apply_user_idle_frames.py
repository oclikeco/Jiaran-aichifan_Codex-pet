from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


ROOT = Path("/Users/macmini/Work/CodexPet")
PET_DIR = Path("/Users/macmini/.codex/pets/jiana-aichifan")
SRC = ROOT / "jiana-spritesheet-clean-v7-dark-outline.png"
OPEN_SRC = Path("/Users/macmini/Downloads/睁眼版本_眼睛调高.png")
CLOSED_SRC = Path("/Users/macmini/Downloads/仅闭眼像素版.png")

OUT = ROOT / "jiana-spritesheet-clean-v11-user-idle-frames.png"
DARK_PREVIEW = ROOT / "jiana-spritesheet-clean-v11-user-idle-frames-dark-preview.png"
IDLE_STRIP = ROOT / "jiana-v11-user-idle-112px-strip.png"
BOOKRUN_STRIP = ROOT / "jiana-v11-bookrun-112px-strip.png"
OPEN_CELL = ROOT / "jiana-v11-open-cell-192x208.png"
CLOSED_CELL = ROOT / "jiana-v11-closed-cell-192x208.png"
PET_WEBP = PET_DIR / "spritesheet-v11-user-idle-frames.webp"

CELL_W = 192
CELL_H = 208
COLS = 8
DARK_BG = (30, 55, 35, 255)
TARGET_H = 170
TARGET_Y0 = 17
TARGET_CX = 96


def cell_box(row: int, col: int) -> tuple[int, int, int, int]:
    return (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)


def bbox(cell: Image.Image) -> tuple[int, int, int, int] | None:
    return cell.getchannel("A").getbbox()


def remove_border_white(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    rgb = arr[:, :, :3].astype(np.int16)
    near_white = (rgb[:, :, 0] > 238) & (rgb[:, :, 1] > 238) & (rgb[:, :, 2] > 238)
    h, w = near_white.shape

    bg = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near_white[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if near_white[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and near_white[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                q.append((nx, ny))

    alpha = arr[:, :, 3].copy()
    alpha[bg] = 0
    arr[:, :, 3] = alpha
    return Image.fromarray(arr, "RGBA")


def keep_largest_component(im: Image.Image) -> Image.Image:
    arr = np.array(im)
    mask = arr[:, :, 3] > 0
    labels, count = ndimage.label(mask)
    if count == 0:
        return im

    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    largest = int(sizes.argmax())
    keep = labels == largest
    arr[:, :, 3] = np.where(keep, arr[:, :, 3], 0).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def make_cell(path: Path) -> Image.Image:
    im = keep_largest_component(remove_border_white(path))
    bb = bbox(im)
    if bb is None:
        raise RuntimeError(f"no foreground in {path}")
    obj = im.crop(bb)
    scale = TARGET_H / obj.height
    obj = obj.resize((max(1, round(obj.width * scale)), TARGET_H), Image.Resampling.NEAREST)

    cell = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    x = round(TARGET_CX - obj.width / 2)
    y = TARGET_Y0
    x = max(0, min(CELL_W - obj.width, x))
    y = max(0, min(CELL_H - obj.height, y))
    cell.alpha_composite(obj, (x, y))
    return cell


def normalize_cell_from_sheet(cell: Image.Image, target_cx: float, target_y0: int, target_h: int) -> Image.Image:
    bb = bbox(cell)
    if bb is None:
        return cell
    obj = cell.crop(bb)
    if obj.height != target_h:
        scale = target_h / obj.height
        obj = obj.resize((max(1, round(obj.width * scale)), target_h), Image.Resampling.NEAREST)
    out = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    x = round(target_cx - obj.width / 2)
    y = target_y0
    x = max(0, min(CELL_W - obj.width, x))
    y = max(0, min(CELL_H - obj.height, y))
    out.alpha_composite(obj, (x, y))
    return out


def redraw_bookrun_row(sheet: Image.Image, src: Image.Image) -> None:
    row = 7
    stats = []
    for col in [1, 2, 3, 4, 5]:
        bb = bbox(src.crop(cell_box(row, col)))
        if bb is None:
            continue
        x0, y0, x1, y1 = bb
        stats.append(((x0 + x1) / 2, y0, y1 - y0))
    target_cx = float(np.median([s[0] for s in stats]))
    target_y0 = round(float(np.median([s[1] for s in stats])))
    target_h = round(float(np.median([s[2] for s in stats])))

    # Avoid the old undersized first frame. Recompose this state from the
    # normal-sized frames only.
    for dest_col, src_col in enumerate([1, 2, 3, 4, 5, 2, 3, 4]):
        cell = normalize_cell_from_sheet(src.crop(cell_box(row, src_col)), target_cx, target_y0, target_h)
        sheet.paste(cell, cell_box(row, dest_col))


def save_dark_preview(sheet: Image.Image) -> None:
    bg = Image.new("RGBA", sheet.size, DARK_BG)
    bg.alpha_composite(sheet)
    bg.save(DARK_PREVIEW)


def save_strip(sheet: Image.Image, row: int, path: Path) -> None:
    scale_w = 112
    scale_h = round(scale_w * CELL_H / CELL_W)
    canvas = Image.new("RGBA", (scale_w * COLS, scale_h), DARK_BG)
    for col in range(COLS):
        source = sheet.crop(cell_box(row, col))
        rendered = Image.new("RGBA", (CELL_W, CELL_H), DARK_BG)
        rendered.alpha_composite(source)
        canvas.alpha_composite(rendered.resize((scale_w, scale_h), Image.Resampling.NEAREST), (col * scale_w, 0))
    canvas.save(path)


def rebuild(install: bool = True) -> None:
    base = Image.open(SRC).convert("RGBA")
    sheet = base.copy()
    open_cell = make_cell(OPEN_SRC)
    closed_cell = make_cell(CLOSED_SRC)
    open_cell.save(OPEN_CELL)
    closed_cell.save(CLOSED_CELL)

    # Codex idle uses columns 0..5. Use one short closed-eye frame and return to
    # open eyes immediately; columns 6..7 are rest/preview copies.
    idle = [open_cell, open_cell, open_cell, closed_cell, open_cell, open_cell, open_cell, open_cell]
    for col, cell in enumerate(idle):
        sheet.paste(cell, cell_box(0, col))

    redraw_bookrun_row(sheet, base)

    sheet.save(OUT)
    save_dark_preview(sheet)
    save_strip(sheet, 0, IDLE_STRIP)
    save_strip(sheet, 7, BOOKRUN_STRIP)

    if install:
        sheet.save(PET_WEBP, "WEBP", lossless=True, quality=100, method=6)

    print(f"out={OUT}")
    print(f"idle_strip={IDLE_STRIP}")
    print(f"bookrun_strip={BOOKRUN_STRIP}")
    print(f"open_cell={OPEN_CELL}")
    print(f"closed_cell={CLOSED_CELL}")
    if install:
        print(f"installed={PET_WEBP}")


if __name__ == "__main__":
    rebuild(install=True)
