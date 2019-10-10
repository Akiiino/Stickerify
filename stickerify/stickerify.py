import argparse
import os
import itertools

import numpy as np
from PIL import Image
from scipy import ndimage

from . import utils
from .screenshot import Screenshot


parser = argparse.ArgumentParser()
parser.add_argument("in_dir", help="directory with input screenshots", metavar='in-dir')
parser.add_argument("--out", help="directory where stickers are output",
                    required=False, default='stickerify_output')


def main():
    args = parser.parse_args()
    in_dir = args.in_dir
    out_dir = args.out

    images = [os.path.join(in_dir, image_path) for image_path in os.listdir(in_dir)]
    os.makedirs(out_dir, exist_ok=True)

    for file_num, image_file in enumerate(images, 1):
        try:
            screenshot = Screenshot(image_file)
        except OSError:
            continue

        screenshot.draw_image()
        screenshot.create_mask()

        for sticker_num in itertools.count(1):
            click = utils.get_left_click()
            sticker = screenshot.make_sticker(click)
            if sticker:
                sticker.save(os.path.join(out_dir, "{}-{}.png".format(file_num, sticker_num)))
            else:
                break


if __name__ == '__main__':
    main()
