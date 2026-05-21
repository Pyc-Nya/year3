from pathlib import Path
from PIL import Image

SRC_DIR = Path(r"C:\projects\year3\sem6\ai_3\dataset")
OUT_DIR = Path(r"C:\projects\year3\sem6\ai_3\dataset_64")

IMG_SIZE = 64

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
CENTER_CROP = True


def center_crop_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    side = min(w, h)

    left = (w - side) // 2
    top = (h - side) // 2
    right = left + side
    bottom = top + side

    return img.crop((left, top, right, bottom))


def resize_dataset(src_dir: Path, out_dir: Path, img_size: int):
    image_paths = [
        p for p in src_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    ]

    total = len(image_paths)
    print(f"Найдено изображений: {total}")

    errors = []

    for index, src_path in enumerate(image_paths, start=1):
        relative_path = src_path.relative_to(src_dir)
        out_path = out_dir / relative_path.with_suffix(".jpg")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with Image.open(src_path) as img:
                img = img.convert("RGB")

                if CENTER_CROP:
                    img = center_crop_square(img)

                img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
                img.save(out_path, quality=95, optimize=True)

        except Exception as e:
            errors.append((src_path, str(e)))

        if index % 100 == 0 or index == total:
            print(f"Обработано: {index}/{total}")

    print(f"Готово. Сохранено в: {out_dir}")

    if errors:
        print(f"Ошибок: {len(errors)}")
        for path, err in errors[:10]:
            print(path, "->", err)


if __name__ == "__main__":
    resize_dataset(SRC_DIR, OUT_DIR, IMG_SIZE)