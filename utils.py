import yaml
import numpy as np
from PIL import ImageDraw


def draw_blank_canvas(cell_dim):
    ROWS = 7  # 6 rows: title row + row per max of 6 weeks in a month
    COLS = 7  # 7 days in a week
    canvas = np.ones((cell_dim * ROWS, cell_dim * COLS, 3)) * 255
    return canvas


def draw_lines(canvas_img):
    ROWS = 7  # 6 rows: title row + row per 5 weeks in a month
    COLS = 7  # 7 days in a week

    draw = ImageDraw.Draw(canvas_img)
    canvas_width = canvas_img.width
    canvas_height = canvas_img.height
    cell_dim = canvas_width // 7
    for r in range(1, ROWS):
        draw.line((0, r * cell_dim, canvas_width, r * cell_dim), fill=0, width=1)
    for c in range(1, COLS):
        draw.line((c * cell_dim, cell_dim, c * cell_dim, canvas_height), fill=0, width=1)
    # canvas_img.save("asf.png")
    return canvas_img


def write_month_title(title, canvas_img, img_font):
    canvas_width = canvas_img.width
    cell_dim = canvas_width // 7
    text_width, text_height = img_font.getsize(title)
    width_start = canvas_width // 2 - text_width // 2
    height_start = cell_dim // 2 - text_height // 2
    start = (width_start, height_start)
    draw = ImageDraw.Draw(canvas_img)
    draw.text(start, title, font=img_font, fill=(0, 0, 0))
    return canvas_img


def make_transparency_mask(image_np):
    transparency_mask = np.ones_like(image_np) * 255
    transparency_mask[np.nonzero(image_np == 255)] = 0
    return transparency_mask


def get_dict_from_yml(yml_file):
    """
    Get the config from a yml file
    :param yml_file:
    :return: config(namespace) or config(dictionary)
    """
    # parse the configurations from the config json file provided
    with open(yml_file, "r") as config_file:
        config_dict = yaml.load(config_file, Loader=yaml.FullLoader)

    return config_dict
