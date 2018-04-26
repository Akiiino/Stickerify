
# coding: utf-8

# In[2]:


from PIL import Image, ImageChops, ImageOps
import numpy as np
from scipy import ndimage
from skimage import measure

from matplotlib import pyplot as plt

import sys
import os

folder = sys.argv[1]
imgs = [os.path.join(folder, img_path) for img_path in os.listdir(folder)]

res_dir = sys.argv[2]
os.makedirs(res_dir, exist_ok=True)

imshow = None

for file_num, img_file in enumerate(imgs):
    try:
        img = Image.open(img_file).convert("RGBA")
    except OSError as e:
        continue


    img_array = np.array(img)

    #if imshow is None:
    plt.cla()
    imshow = plt.imshow(img_array)
    #else:
    #    plt.cla()
    #    imshow.set_data(img_array)

    plt.draw()

    i = 0

    stopped = False
    mask = None

    while not stopped:
        try:
            click = plt.ginput(1)[0]
        except IndexError as e:
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

                masked_img.save(os.path.join(res_path, "{}-{}.png".format(file_num, i)))
                i += 1
                break
        else:
            stopped = True

