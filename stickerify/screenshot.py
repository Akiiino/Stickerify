import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure
try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib as mpl; mpl.use('TkAgg')
    import matplotlib.pyplot as plt

from . import utils


class Screenshot:
    """
    Screenshot class containing PIL image, np.array image,
    mask of messages on image and corresponding labels array
    """
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGBA")
        self.image_array = np.array(self.image)
        self.mask = None
        self.labels = None

    def create_mask(self):
        """
        Waits for a click and creates a mask and labels
        """
        click = utils.get_left_click()
        size = (np.array(self.image.size) / 10).astype(int)

        msg_color = \
            sorted(self.image.crop((*(click - size), *(click + size))).getcolors(np.prod(size) * 4), reverse=True)[0][1]
        self.mask = ndimage.morphology.binary_fill_holes((self.image_array == np.array(msg_color)).all(axis=2))
        self.labels = ndimage.label(self.mask )[0]

        for label in set(self.labels.flatten()):
            if (self.labels == label).sum() < 10000:
                self.labels[self.labels == label] = 0

        self.labels = ndimage.label(self.labels)[0]

        contours = measure.find_contours(self.labels, 0.8)
        utils.draw_contours(contours)

    def make_sticker(self, click):
        """
        Makes sticker from prepared screen shot and click and returns final image
        :param click: coordinates of the click on the image
        :return: image of sticker if click was on message and None otherwise
        """
        if self.mask is None:
            raise ScreenshotNotReady('Using non-prepared screenshot to make stickers. Have you called create_mask()?')
        objects = ndimage.find_objects(ndimage.label(self.labels)[0])

        for object_ in objects:
            if all((range_.start <= c <= range_.stop) for c, range_ in zip(click[::-1], object_)):
                masked_image = Image.fromarray(
                    self.image_array[object_] * ndimage.binary_dilation(self.mask[object_])[..., None])
                size = np.array(masked_image.size, dtype=float)
                size /= max(size / utils.STICKER_SIZE)
                masked_image = masked_image.resize(size.astype(int), Image.ANTIALIAS)
                return masked_image
        else:
            return

    def draw_image(self):
        """
        Clears the view and draws current image
        """
        plt.cla()
        plt.imshow(self.image)
        plt.draw()


class ScreenshotNotReady(Exception):
    pass
