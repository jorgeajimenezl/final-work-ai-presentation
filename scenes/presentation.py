from manim import *
import itertools as it

from utils import WrappedImage, PixelsFromVect, read_and_downsample


class Presentation(Scene):
    def construct(self):
        text = Tex(r"Trabajo final\\de\\Inteligencia Artificial", font_size=80)
        title = Tex(
            r"Título:\\Segmentación semantica de imágenes",
            tex_to_color_map={"Título": YELLOW},
            font_size=75,
        )

        self.play(Write(text))
        self.pause()

        jorge_image = ImageMobject("resources/jorgeajimenezl.png")
        jorge_image.add(
            Text("Jorge Alejandro Jiménez Luna").scale(0.5).next_to(jorge_image, UP)
        )

        luis_image = ImageMobject("resources/Lcasan.png")
        luis_image.add(
            Text("Luis Miguel Casañ Gonzáles").scale(0.5).next_to(luis_image, DOWN)
        )

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
            FadeIn(authors),
        )
        self.pause()

        title.to_corner(UP)

        # Semantic segmentation image example
        image = WrappedImage(
            PixelsFromVect(read_and_downsample("resources/example-image.png", (50, 50)))
            .scale(16.0)
            .next_to(title, DOWN),
            # color=GREY_B,
            # buff=0,
        )
        mask = (
            PixelsFromVect(read_and_downsample("resources/example-mask.png", (50, 50)))
            .set_stroke(WHITE)
            .scale(16.0)
            .next_to(title, DOWN)
        )
        image[1].sort(lambda p: np.dot(p, DOWN + RIGHT))
        mask.sort(lambda p: np.dot(p, DOWN + RIGHT))

        cp = image[1].copy()
        # cp.sort(lambda p: np.dot(p, DOWN + RIGHT))

        self.play(
            FadeOut(authors),
            Transform(text, title),
            FadeIn(image[0]),
            LaggedStartMap(FadeIn, image[1]),
        )
        self.wait()
        self.play(
            LaggedStartMap(
                DrawBorderThenFill,
                cp,
                run_time=3,
                stroke_color=WHITE,
                remover=False,
            ),
            LaggedStartMap(FadeOut, image[1]),
            LaggedStartMap(FadeIn, mask),
        )
        self.pause()

        for c in it.chain(image[1], cp):
            self.remove(c)

        self.play(FadeOut(text, mask, image[0]))
        self.wait()
