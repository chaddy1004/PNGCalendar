from PIL import Image, ImageFont, ImageDraw
import argparse
from utils import get_dict_from_yml, draw_blank_canvas, make_transparency_mask, write_month_title, draw_lines
import datetime
from date_util import DateUtil
import numpy as np
import os

"""
Monday == 0
...
Sunday == 6
"""


def create_calendar(year, font_file, country, lang, draw_line):
    config_dict = get_dict_from_yml("config.yml")
    cell_dim = 150
    date_util = DateUtil(country=country)
    TITLE_FONT_SIZE = 100
    title_font = ImageFont.truetype(font_file, TITLE_FONT_SIZE)

    CELL_FONT_SIZE = 60
    cell_font = ImageFont.truetype(font_file, CELL_FONT_SIZE)

    for m in range(1, 13):
        month_name = config_dict['language'][lang]['months'][m]
        canvas_np = draw_blank_canvas(cell_dim=cell_dim)
        canvas_img = Image.fromarray(canvas_np.astype('uint8'), 'RGB')
        if draw_line:
            canvas_img = draw_lines(canvas_img)
        canvas_img = write_month_title(title=month_name, canvas_img=canvas_img, img_font=title_font)

        draw = ImageDraw.Draw(canvas_img)

        n_days = config_dict['days'][m]
        if m == 2 and date_util.is_leap_year(year):
            n_days += 1

        week = 1
        weekdays = [6, 0, 1, 2, 3, 4, 5]
        for d in range(1, n_days + 1):
            date = datetime.datetime(year, m, d)
            weekday = date.weekday()
            fill = (0, 0, 0)
            if weekday == 6 or date == date_util.is_holiday(date=(year, m, d)):  # If Sunday
                # TODO: Write in red
                fill = (255, 0, 0)

            date_text = f"{d}"
            text_width, text_height = cell_font.getsize(date_text)
            cell_corner_x = weekdays.index(weekday) * cell_dim
            cell_corner_y = week * cell_dim

            x = cell_corner_x +  cell_dim//2 - text_width // 2
            y = cell_corner_y +  cell_dim//2 -  text_height // 2
            draw.text(xy=(x, y), text=date_text, font=cell_font, fill=fill)
            if weekday == 5:  # change to new row when saturday is hit
                week += 1

        calendar_done_np = np.array(canvas_img)

        calendar_done_grayscale = np.array(canvas_img.convert('L'))  # convert to grayscale for finding alpha map
        transparency_mask = make_transparency_mask(calendar_done_grayscale[..., np.newaxis].astype('uint8'))
        calendar_png_np = np.concatenate([calendar_done_np, transparency_mask], axis=-1)
        calendar_png_img = Image.fromarray(calendar_png_np, mode="RGBA")

        calendar_png_img.save(f"saved_calendars/{m}_{month_name}_{year}_{country}_{lang}.png")

    return


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2021)
    ap.add_argument("--font", type=str, default="SDKukdetopokki-aLt.otf")
    ap.add_argument("--country", type=str, default="KR", help="two character country id string")
    ap.add_argument("--lang", type=str, default="EN", help="Korean: KR, English: EN, French: FR")
    ap.add_argument("--draw_line", action='store_true')
    args = vars(ap.parse_args())

    year = args["year"]
    font = args["font"]
    country = args["country"]
    lang = args["lang"]
    draw_line = args["draw_line"]

    font_file = os.path.join("fonts", font)
    create_calendar(year=year, font_file=font_file, country=country, lang=lang, draw_line=draw_line)
