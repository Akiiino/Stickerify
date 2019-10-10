try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib as mpl; mpl.use('TkAgg')
    import matplotlib.pyplot as plt

STICKER_SIZE = 512


def draw_contours(contours):
    for contour in contours:
        plt.plot(contour[:, 1], contour[:, 0], linewidth=2, c="red")
    plt.draw()


def get_left_click():
    return plt.ginput(1, mouse_pop=None, mouse_stop=None, timeout=0, show_clicks=True)[0]
