import argparse
import os

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("in_dir", help="directory with input screenshots", metavar='in-dir')
parser.add_argument("--out", help="directory where stickers are output",
                    required=False, default='stickerify_output')


def main():
    args = parser.parse_args()
    in_dir = args.in_dir
    out_dir = args.out

    imgs = [os.path.join(in_dir, img_path) for img_path in os.listdir(in_dir)]
    os.makedirs(out_dir, exist_ok=True)

    for file_num, img_file in enumerate(imgs):
        try:
            img = Image.open(img_file).convert("RGBA")
        except OSError:
            continue

        img_array = np.array(img)

        plt.cla()
        plt.imshow(img_array)
        plt.draw()

        i = 0

        stopped = False
        mask = None

        while not stopped:
            try:
                click = plt.ginput(1)[0]
            except IndexError:
                pass

            if mask is None:
                size = (np.array(img.size) / 10).astype(int)

                msg_color = sorted(img.crop((*(click - size), *(click + size))).getcolors(np.prod(size) * 4), reverse=True)[0][1]

                mask = ndimage.morphology.binary_fill_holes((np.array(img) == np.array(msg_color)).all(axis=2))

                labels = ndimage.label(mask)[0]

                for label in set(labels.flatten()):
                    if (labels == label).sum() < 10000:
                        labels[labels == label] = 0

                labels = ndimage.label(labels)[0]

                contours = measure.find_contours(labels, 0.8)
                for contour in contours:
                    plt.plot(contour[:, 1], contour[:, 0], linewidth=2, c="red")
                plt.draw()

            objects = ndimage.find_objects(ndimage.label(labels)[0])

            for object_ in objects:
                if all((c >= range_.start and c <= range_.stop) for c, range_ in zip(click[::-1], object_)):
                    masked_img = Image.fromarray(img_array[object_] * ndimage.binary_dilation(mask[object_])[..., None])
                    size = np.array(masked_img.size, dtype=float)
                    size /= max(size/512)
                    masked_img = masked_img.resize(size.astype(int), Image.ANTIALIAS)

                    masked_img.save(os.path.join(out_dir, "{}-{}.png".format(file_num, i)))
                    i += 1
                    break
            else:
                stopped = True


if __name__ == '__main__':
    main()
