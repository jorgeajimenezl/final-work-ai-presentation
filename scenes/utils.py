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


def read_image(
    filename: str,
    size: tuple[int, int] = None,
    resample: Image.Resampling = Image.Resampling.NEAREST,
) -> np.ndarray:
    with Image.open(filename) as im:
        if size is not None:
            im.thumbnail(size, resample)
        return np.asarray(im)


class ColorVectAsCubes(VGroup):
    def __init__(
        self,
        rows: int,
        cols: int,
        depth: int,
        side_length: float = 0.5,
        fill_opacity: float = 0.75,
        fill_color: str | list[str] = BLUE,
        stroke_width: float = 0,
        buff: float | tuple[float, float] = MED_SMALL_BUFF,
        **kwargs
    ):
        if isinstance(fill_color, list) and len(fill_color) != depth:
            raise ValueError("Fill color list length must match with layers")
        super().__init__(**kwargs)

        if not isinstance(fill_color, list):
            fill_color = [fill_color] * depth

        self.size = (rows, cols, depth)
        for _ in range(rows):
            row = VGroup()

            for l in range(depth):
                for _ in range(cols):
                    row.add(
                        Cube(
                            side_length=side_length,
                            fill_opacity=fill_opacity,
                            fill_color=fill_color[l],
                            stroke_width=stroke_width,
                        )
                    )

            row.arrange_in_grid(depth, cols, buff=buff)
            if len(self) != 0:
                row.next_to(self[-1], direction=IN * buff)
            self.add(row)

        self.move_to(ORIGIN)

    def get_cube(self, row: int, col: int, layers: int) -> Cube:
        return self[row][layers * self.size[1] + col]

    def get_row(self, row: int) -> VGroup:
        return self[row]

    def make_convolution(
        self,
        kernel_size: tuple[int, int],
        filters: int,
        filters_colors: list[str],
        buff: float | tuple[float, float] = LARGE_BUFF,
        run_time: float | None = None,
        lag_ratio: float = 1,
        fast_forward_from: int = None,
    ) -> AnimationGroup:
        if len(filters_colors) != filters:
            raise ValueError(
                "The length of filters_colors must match with filters value"
            )
        size = [self.size[0] - kernel_size[0] + 1, self.size[1] - kernel_size[1] + 1]
        res_obj = (
            ColorVectAsCubes(*size, filters, fill_color=list(reversed(filters_colors)))
            .next_to(self, RIGHT * buff)
            .set_opacity(0.0)
        )

        animations = [self.animate.set_opacity(0.1)]

        def get_focus(x, y):
            res = set()
            for i in range(x, x + kernel_size[0]):
                for j in range(y, y + kernel_size[1]):
                    for k in range(self.size[2]):
                        res.add(self.get_cube(i, j, k))
            return res

        last = None
        last_animation = []
        cnt = 0

        for index, color in enumerate(filters_colors):
            for x in range(size[0]):
                for y in range(size[1]):
                    focus = get_focus(x, y)
                    anim = []

                    if last != None:
                        ret = last - focus
                        for item in ret:
                            anim.append(item.animate.set_opacity(0.1))

                    last = focus
                    for item in focus:
                        anim.append(item.animate.set_opacity(1.0).set_color(color))

                    res_item = res_obj.get_cube(x, y, filters - index - 1)
                    anim.append(res_item.animate.set_opacity(1.0))

                    cnt += 1
                    if fast_forward_from is not None and cnt >= fast_forward_from:
                        last_animation.append(AnimationGroup(*anim))
                    else:
                        animations.append(AnimationGroup(*anim))

        if fast_forward_from is not None:
            animations.append(Succession(*last_animation, lag_ratio=0.2))

        return Succession(*animations, run_time=run_time, lag_ratio=lag_ratio)


class CreateCubesFromCenter(LaggedStartMap):
    def __init__(self, cubes: Group, run_time: float = 2, **kwargs) -> None:
        items = VGroup(*[cube for row in cubes for cube in row])
        items.sort(lambda p: np.square(np.sum(np.abs(p - cubes.get_center()))))

        super().__init__(Create, items, run_time=run_time, **kwargs)
