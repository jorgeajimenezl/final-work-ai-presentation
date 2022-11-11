from turtle import width
from manim import *
from manim_slides import *
from PIL import Image
import numpy as np


def create_image(path: str, size: tuple[int, int] = None) -> ImageMobject:
    with Image.open(path) as im:
        if size is not None:
            im.thumbnail(size, resample=Image.BOX)
        image = ImageMobject(np.asarray(im))
        return image


class Presentation(Slide):
    def construct(self):
        text = Tex(r"Trabajo final\\de\\Inteligencia Artificial", font_size=80)
        title = Tex(
            r"Título:\\Segmentación semantica de imágenes",
            tex_to_color_map={"Título": YELLOW},
            font_size=75,
        )

        self.play(Write(text))
        self.pause()

        jorge_image = create_image("resources/jorgeajimenezl.png")
        jorge_image.add(Text("Jorge Alejandro Jiménez Luna").scale(0.5).next_to(jorge_image, UP))

        luis_image = create_image("resources/Lcasan.png")
        luis_image.add(Text("Luis Miguel Casañ Gonzáles").scale(0.5).next_to(luis_image, DOWN))

        authors = Group(jorge_image, luis_image)
        authors.arrange()

        self.play(
            Transform(
                text,
                Tex(
                    "Autores",
                    tex_to_color_map={"Autores": YELLOW},
                    font_size=65,
                ).to_corner(UP),
            ),
            FadeIn(authors)
        )
        self.pause()

        title.to_corner(UP)

        image = create_image("resources/example-image.png")
        image = (
            image.add(SurroundingRectangle(image, BLUE_A, buff=0.015))
            .scale(3.5)
            .next_to(title, DOWN)
        )

        self.play(
            FadeOut(authors),
            Transform(text, title),
            FadeIn(image)
        )
        self.pause()

        group = Group(text, image)
        self.play(FadeOut(group))
        self.pause()

        self.wait()
