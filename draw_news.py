#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (26, 26, 26)
RULE = (26, 26, 26)
MUTED = (90, 80, 60)
CARD_BG = (255, 251, 240)
CARD_LINE = (200, 185, 150)
ACCENT = (165, 30, 30)

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# Noto Color Emoji on this VM has a single 109px bitmap strike: load at 109,
# then downscale to the size we need.
EMOJI_SRC = 109


def emoji_tile(ch, size):
    f = ImageFont.truetype(EMOJI, EMOJI_SRC)
    tile = Image.new("RGBA", (EMOJI_SRC, EMOJI_SRC), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.text((0, 0), ch, font=f, embedded_color=True)
    return tile.resize((size, size), Image.LANCZOS)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("🚀", "RUSSIAN MISSILES HIT POLAND",
     "Two missiles and a suspected drone come down in Poland. Warsaw calls it "
     "a deliberate provocation; NATO calls it a grave violation of its airspace."),
    ("📉", "WALL STREET SLUMPS INTO CORRECTION",
     "The S&P 500 falls 3.7% and the Dow enters correction as AI shares plunge. "
     "The Nasdaq loses over 5%; Anthropic slides 11% a day after its debut."),
    ("🕵️", "DENMARK FOILS ASSASSINATION PLOT",
     "Denmark's PET security service says Russian intelligence plotted to kill "
     "a US-Ukrainian rapper in Denmark. The plot was thwarted before it could happen."),
    ("🔥", "TANKER ABLAZE IN STRAIT OF HORMUZ",
     "A tanker catches fire near Oman after being hit by an unknown projectile. "
     "UKMTO warns shipping in the strait as Gulf oil flows stay under threat."),
    ("💥", "RUSSIA POUNDS KYIV BRIDGES",
     "A massive Russian aerial offensive hits three Kyiv bridges, killing at "
     "least nine. A strike on Kryvyi Rih kills two and injures 42, four of them children."),
    ("⚖️", "PALISADES FIRE ARSONIST CONVICTED",
     "A Los Angeles jury convicts Jonathan Rinderknecht of starting the "
     "Palisades Fire, one of the most destructive wildfires in California history."),
]

FOOTER = ("ALSO TODAY: Pancreatic cancer pill breakthrough  ·  Gupta gets 19+ years "
          "in Sikh plot  ·  Houthi missiles intercepted over Riyadh  ·  "
          "Mongolia's president resigns")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = ImageFont.truetype(DEJAVU_B, 92)
    f_date = ImageFont.truetype(DEJAVU_B, 30)
    f_tag = ImageFont.truetype(DEJAVU, 24)
    f_head = ImageFont.truetype(DEJAVU_B, 27)
    f_body = ImageFont.truetype(DEJAVU, 22)
    f_foot = ImageFont.truetype(DEJAVU_B, 20)

    # Masthead
    d.text((W // 2, 34), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    d.line([(48, 150), (W - 48, 150)], fill=RULE, width=4)
    d.text((W // 2, 162), "SATURDAY, 21 NOVEMBER 2026", font=f_date, fill=ACCENT, anchor="ma")
    d.text((W // 2, 202), "Six stories that defined the day, around the globe",
           font=f_tag, fill=MUTED, anchor="ma")
    d.line([(48, 242), (W - 48, 242)], fill=RULE, width=2)

    # Story cards: 2 columns x 3 rows
    gx, gy = 48, 262
    cw, ch = 452, 212
    gap_x, gap_y = 24, 18
    for i, (emo, head, body) in enumerate(STORIES):
        x = gx + (i % 2) * (cw + gap_x)
        y = gy + (i // 2) * (ch + gap_y)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10, fill=CARD_BG,
                            outline=CARD_LINE, width=2)
        d.line([(x + 16, y + 64), (x + cw - 16, y + 64)], fill=CARD_LINE, width=1)
        tile = emoji_tile(emo, 40)
        img.paste(tile, (x + 14, y + 10), tile)
        hl = wrap(d, head, f_head, cw - 76)
        for j, ln in enumerate(hl[:2]):
            d.text((x + 62, y + 12 + j * 26), ln, font=f_head, fill=INK)
        bl = wrap(d, body, f_body, cw - 32)
        for j, ln in enumerate(bl[:5]):
            d.text((x + 16, y + 76 + j * 27), ln, font=f_body, fill=INK)

    # Footer strip
    fy = gy + 3 * ch + 2 * gap_y + 14
    d.line([(48, fy), (W - 48, fy)], fill=RULE, width=2)
    fl = wrap(d, FOOTER, f_foot, W - 96)
    for j, ln in enumerate(fl[:3]):
        d.text((W // 2, fy + 10 + j * 26), ln, font=f_foot, fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
