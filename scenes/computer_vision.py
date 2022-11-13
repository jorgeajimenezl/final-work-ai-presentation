from manim import *
from utils import WrappedImage, PixelsFromVect, read_image


class ComputerVision(Scene):
    def construct(self):
        image = WrappedImage(
            PixelsFromVect(read_image("resources/mario.png", (32, 32))).scale(20.0)
        )

        cp = image[1].copy()
        cp.sort(lambda p: np.dot(p, DOWN + RIGHT))

        self.play(FadeIn(image[0]), LaggedStartMap(FadeIn, image[1]))
        self.wait()

        self.play(
            LaggedStartMap(
                DrawBorderThenFill,
                cp,
                run_time=3,
                stroke_color=WHITE,
                remover=False,
            ),
        )

        self.wait()
        self.play(FadeOut(cp, image))
