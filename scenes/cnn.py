from manim import *
from manim_slides import *
from utils import ColorVectAsCubes, CreateCubesFromCenter


class ConvolutionalNeuralNetwork(ThreeDSlide):
    def construct(self):
        self.renderer.camera.light_source.move_to(3 * IN)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-75 * DEGREES)

        title = Text("Redes convolucionales", color=BLUE)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)
        self.play(Write(title))

        self.section_001()

        self.play(
            title.animate.become(
                Text("Convolución?", color=BLUE).replace(title).scale(0.7)
            ),
        )
        self.wait()

        self.section_002()

        self.wait()

    def section_001(self):
        layer1 = (
            ColorVectAsCubes(11, 3, 11, fill_color=BLUE, buff=SMALL_BUFF)
            .scale(0.5)
            .shift(LEFT * 5)
        )

        layer2 = (
            ColorVectAsCubes(5, 5, 5, fill_color=PURPLE, buff=SMALL_BUFF)
            .scale(0.5)
            .shift(LEFT * 3.5)
        )

        layer3 = (
            ColorVectAsCubes(3, 7, 3, fill_color=ORANGE, buff=SMALL_BUFF)
            .scale(0.5)
            .shift(LEFT * 1.5)
        )

        fully1 = Prism([0.7, 0.7, 2], fill_opacity=0.5).shift(RIGHT * 0.5)
        neurons1 = VGroup()
        for _ in range(4):
            neurons1.add(Sphere(fully1.get_center(), radius=0.1))
        neurons1.arrange(IN, buff=0.2).move_to(fully1)
        fully1.add(neurons1)

        fully2 = Prism([0.7, 0.7, 2], fill_opacity=0.5).shift(RIGHT * 1.5)
        neurons2 = VGroup()
        for _ in range(4):
            neurons2.add(Sphere(fully2.get_center(), radius=0.1))
        neurons2.arrange(IN, buff=0.2).move_to(fully2)
        fully2.add(neurons2)

        self.play(
            CreateCubesFromCenter(layer1, run_time=0.5),
            CreateCubesFromCenter(layer2, run_time=0.5),
            CreateCubesFromCenter(layer3, run_time=0.5),
        )

        self.play(
            FadeIn(fully1),
            FadeIn(fully2),
        )
        self.pause()

        features_text = Tex(
            r"""
            \begin{itemize}
            \item Hacen asunciones\\de localidad
            \item Son relativamente\\eficientes en\\términos de memoria\\y capacidad de\\cómputo requerido.
            \end{itemize}
            """
        )
        self.add_fixed_in_frame_mobjects(features_text)
        features_text.shift(RIGHT * 4.6).scale(0.9)
        self.play(Write(features_text))

        self.pause()

        # Remove all this shit
        self.play(
            FadeOut(layer1),
            FadeOut(layer2),
            FadeOut(layer3),
            FadeOut(fully1),
            FadeOut(fully2),
            Unwrite(features_text),
        )

    def section_002(self):
        label = Text("Datos")
        self.add_fixed_in_frame_mobjects(label)

        cubes = ColorVectAsCubes(5, 5, 3, fill_color=RED)
        label.next_to(cubes, DOWN * 4).scale(0.8)

        self.play(CreateCubesFromCenter(cubes), Write(label))
        self.pause()

        data_obj = VGroup(cubes, label)
        self.play(data_obj.animate.move_to(LEFT * 3), Unwrite(label))
        self.wait()

        self.play(
            cubes.make_convolution(
                (3, 3),
                filters=3,
                filters_colors=[RED, GREEN, BLUE],
                buff=6
            )
        )
