from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "pet" / "spritesheet.webp"
OUTPUT = ROOT / "assets" / "deepseek-girl-in-codex.gif"
FONT = Path(r"C:\Windows\Fonts\msjhbd.ttc")
CELL_W, CELL_H = 192, 208


def font(size: int):
    return ImageFont.truetype(str(FONT), size) if FONT.exists() else ImageFont.load_default()


def round_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def make_background() -> Image.Image:
    image = Image.new("RGBA", (960, 540), "#111315")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 960, 48), fill="#1a1d20")
    draw.ellipse((18, 19, 28, 29), fill="#ff6b66")
    draw.ellipse((36, 19, 46, 29), fill="#f4c44e")
    draw.ellipse((54, 19, 64, 29), fill="#62c975")
    draw.text((86, 14), "Codex  ·  deepseek娘", font=font(18), fill="#ecf0f3")

    draw.rectangle((0, 48, 220, 540), fill="#171a1d")
    draw.text((24, 76), "工作區", font=font(16), fill="#8c969f")
    round_rect(draw, (14, 108, 206, 150), 9, "#24282c")
    draw.text((30, 119), "upgrade pet", font=font(15), fill="#eef1f3")
    draw.text((24, 178), "最近任務", font=font(16), fill="#8c969f")
    draw.text((30, 214), "✓ v2 圖集驗證", font=font(14), fill="#a9b2ba")
    draw.text((30, 246), "✓ 16 個觀看方向", font=font(14), fill="#a9b2ba")
    draw.text((30, 278), "✓ 待機文字放大", font=font(14), fill="#a9b2ba")

    draw.text((258, 82), "已完成 deepseek娘 Codex 寵物", font=font(25), fill="#f2f5f7")
    draw.text((258, 123), "正在待機，隨時準備陪你工作。", font=font(16), fill="#9ca6ae")
    round_rect(draw, (258, 174, 686, 270), 14, "#1b1e21", outline="#30353a")
    draw.text((282, 195), "Codex", font=font(15), fill="#74d69b")
    draw.text((282, 226), "寵物已通過 v2 驗證與視覺 QA。", font=font(16), fill="#dbe0e4")

    round_rect(draw, (258, 452, 916, 506), 15, "#1b1e21", outline="#353a40")
    draw.text((284, 469), "Ask Codex anything…", font=font(15), fill="#727c85")
    draw.ellipse((872, 465, 902, 495), fill="#edf1f3")
    draw.polygon([(882, 474), (894, 480), (882, 486)], fill="#202428")
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(ATLAS) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (1536, 2288):
        raise SystemExit(f"unexpected atlas size: {atlas.size}")

    durations = [560, 150, 150, 180, 180, 620]
    frames = []
    background = make_background()
    for index in range(6):
        pet = atlas.crop((index * CELL_W, 0, (index + 1) * CELL_W, CELL_H))
        pet = pet.resize((288, 312), Image.Resampling.LANCZOS)
        frame = background.copy()
        frame.alpha_composite(pet, (650, 214))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))

    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
