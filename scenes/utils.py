from manim import *
from PIL import Image
import numpy as np


class PixelsAsSquares(VGroup):
    CONFIG = {
        "height": 2,
    }

    def __init__(self, image_mobject: ImageMobject, **kwargs) -> None:
        VGroup.__init__(self, **kwargs)
        for row in image_mobject.pixel_array:
            for rgba in row:
                square = Square(
                    stroke_width=0,
                    fill_opacity=rgba[3] / 255.0,
                    fill_color=rgba_to_color(rgba / 255.0),
                )
                self.add(square)
        self.arrange_in_grid(*image_mobject.pixel_array.shape[:2], buff=0)
        self.replace(image_mobject)


class PixelsFromVect(PixelsAsSquares):
    def __init__(self, vect, **kwargs) -> None:
        PixelsAsSquares.__init__(self, ImageMobject(vect), **kwargs)


class WrappedImage(Group):
    CONFIG = {
        "rect_kwargs": {
            "color": BLUE,
            "buff": SMALL_BUFF,
        }
    }

    def __init__(self, image_mobject: ImageMobject, **kwargs) -> None:
        Group.__init__(self, **kwargs)
        rect = SurroundingRectangle(image_mobject, color=BLUE, buff=SMALL_BUFF)
        self.add(rect, image_mobject)


def read_and_downsample(filename: str, size: tuple[int, int]) -> np.ndarray:
    with Image.open(filename) as im:
        im.thumbnail(size, Image.Resampling.BOX)
        return np.asarray(im)
