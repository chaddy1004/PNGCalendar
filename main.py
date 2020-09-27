from PIL import Image, ImageFont
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


def create_calendar(year, font_file, country, lang):
    config_dict = get_dict_from_yml("config.yml")
    cell_dim = 150
    date_util = DateUtil(country=country)
    FONT_SIZE = 100
    font = ImageFont.truetype(font_file, FONT_SIZE)

    for m in range(1, 13):
        month_name = config_dict['language'][lang]['months'][m]
        canvas_np = draw_blank_canvas(cell_dim=cell_dim)
        canvas_img = Image.fromarray(canvas_np.astype('uint8'), 'RGB')
        canvas_img = draw_lines(canvas_img)
        canvas_img = write_month_title(title=month_name, canvas_img=canvas_img, img_font=font)

        # n_days = config_dict['days'][m]
        # if m == 2 and date_util.is_leap_year(year):
        #     n_days += 1
        #
        # for d in n_days:
        #     date = datetime.datetime(year, m, d)
        #     weekday = date.weekday()
        #     if weekday == 6:  # If Sunday
        #         # TODO: Write in red
        #         pass
        #
        #
        #     elif date == date_util.is_holiday(date=(year, m, d)):
        #         # TODO: Write in red
        #         pass

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
    args = vars(ap.parse_args())

    year = args["year"]
    font = args["font"]
    country = args["country"]
    lang = args["lang"]

    font_file = os.path.join("fonts", font)
    create_calendar(year=year, font_file=font_file, country=country, lang=lang)
