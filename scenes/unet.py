from manim import *
from utils import WrappedImage, read_image
from layers import Convolutional3DToImage
import matplotlib as mpl
import itertools as it
from manim_ml.neural_network.neural_network import NeuralNetwork
from manim_ml.neural_network.layers import *

# Hack connective list
connective_layers_list.append(Convolutional3DToImage)


def get_mask(array, colormap: str = "viridis"):
    cm = mpl.colormaps[colormap]
    a, b = array.min(), array.max()

    return (cm((array - a) / (b - a)) * 255).astype(np.uint8)


def repeat_animation(times: int, anim: Animation):
    return Succession(*[anim.copy() for _ in range(times)])


class UNet(Scene):
    def construct(self):
        # Make title
        title = Text("Detección de objectos")
        # self.play(Write(title))
        # self.pause()

        # Explanation about semantic segmentation section
        # self.section_001(title)

        # Change title
        # self.play(
        #     title.animate.become(Text("Aplicaciones", color=BLUE).replace(title)),
        # )

        # Applications section
        # self.section_002(title)

        # Change title
        # self.play(
        #     title.animate.become(
        #         Text("Cómo resolverlo? U-Net", color=BLUE).replace(title)
        #     ),
        # )

        # Play explanation
        self.section_003(title)

        self.wait()

    def section_001(self, title: Text) -> None:
        image = WrappedImage(
            ImageMobject("resources/segm.png").scale(1.8).shift(DOWN * 0.5)
        )

        self.play(
            Succession(
                title.animate.scale(0.8).next_to(image, UP, SMALL_BUFF),
                FadeToColor(title, BLUE),
            ),
            FadeIn(image),
        )
        self.pause()

        # Set bounding boxes
        bound_box = (
            Rectangle(width=2.2, height=1)
            .set_stroke(RED)
            .arrange(DOWN, buff=SMALL_BUFF)
            .move_to(image[1].get_center() + RIGHT * 1.2 + UP * 0.1)
        )

        self.play(Create(bound_box))
        self.wait(2)
        self.play(
            bound_box.animate.stretch_to_fit_width(1.3)
            .stretch_to_fit_height(2.6)
            .move_to(image[1].get_center() + RIGHT * 3.6 + UP * 1.5),
        )
        self.wait(2)
        self.play(
            bound_box.animate.stretch_to_fit_width(0.8)
            .stretch_to_fit_height(1.6)
            .move_to(image[1].get_center() + RIGHT * 1.8 + UP),
        )

        self.pause()

        self.play(Uncreate(bound_box))
        self.wait()

        self.play(
            title.animate.become(
                Text("Segmentación semántica?", color=BLUE).replace(title)
            ),
            # Transform(
            #     image[1],
            #     ImageMobject(mask_vect).scale(1.8).shift(DOWN * 0.5),
            #     replace_mobject_with_target_in_scene=True,
            # ),
        )
        self.pause()

        pixels = VGroup()
        for i in range(32 * 24):
            square = Square(
                stroke_width=1.0,
            )
            pixels.add(square)

        pixels.arrange_in_grid(24, 32, buff=0)
        pixels.rescale_to_fit(image[1].length_over_dim(0), dim=0, stretch=False)
        pixels.rescale_to_fit(image[1].length_over_dim(1), dim=1, stretch=False)
        pixels.move_to(image[1])

        numbers = VGroup()
        mask_id = read_image("resources/segm-mask.png", (32, 24))[:, :, 0]
        mask_cmap = get_mask(mask_id, "hsv")

        p = 0
        pixel_map = dict()
        for y in range(24):
            for x in range(32):
                square = pixels[p]
                p += 1
                num = Integer(mask_id[y, x])

                num.set_stroke(width=1)

                rgb = mask_cmap[y, x, :3]
                num.scale_to_fit_height(0.5 * square.width)
                num.set_color(rgb_to_color(rgb / 255))
                num.move_to(square)
                numbers.add(num)

                pixel_map[(y, x)] = (square, num)

        pixels.sort(lambda p: np.dot(p, DOWN + RIGHT))

        self.play(
            image[1].animate.set_opacity(0.5),
            LaggedStartMap(
                Create,
                pixels,
                run_time=3,
                stroke_color=WHITE,
                remover=False,
            ),
        )

        self.play(Write(numbers))
        self.pause()

        pixel_index = (12, 19)

        self.play(
            *[
                FadeOut(pixel)
                for index, (pixel, _) in pixel_map.items()
                if index != pixel_index
            ],
            *[
                FadeOut(num)
                for index, (_, num) in pixel_map.items()
                if index != pixel_index
            ],
        )

        # Save state of (image, pixel square, pixel number)
        tmp_group = Group(image, pixel_map[pixel_index][0], pixel_map[pixel_index][1])
        pos = tmp_group.get_center()
        self.play(tmp_group.animate.scale(0.8).move_to(LEFT * 3))

        # Write classes
        classes = (
            VGroup(
                Text("..."),
                Text("[9] Árbol", color=YELLOW),
                Text("[10] Automóvil", color=GREEN),
                Text("[11] Luces de tráfico", color=RED),
                Text("..."),
            )
            .arrange(DOWN, buff=MED_LARGE_BUFF)
            .scale(0.5)
            .move_to(RIGHT * 3)
        )
        tmp_box = SurroundingRectangle(classes[2])
        arrow = Arrow(
            start=pixel_map[pixel_index][0].get_right(),
            end=tmp_box.get_left(),
            stroke_width=3,
        )

        self.play(Write(classes), Create(tmp_box), Create(arrow))

        self.pause()
        self.play(
            FadeOut(classes),
            FadeOut(tmp_box),
            FadeOut(arrow),
            # tmp_group.animate.scale(2).move_to(pos),
        )

        # Go back to restore everything
        self.wait()
        self.play(
            FadeOut(pixel_map[pixel_index][0]),
            FadeOut(pixel_map[pixel_index][1]),
            image[1].animate.set_opacity(1.0),
        )

        mask_vect = get_mask(read_image("resources/segm-mask.png")[:, :, 0], "hsv")
        mask_image = ImageMobject(mask_vect).replace(image[1])
        self.play(
            Transform(
                image[1],
                mask_image,
                replace_mobject_with_target_in_scene=True,
            ),
        )

        features_text = (
            Tex(
                r"""
            \begin{itemize}
            \item Etiqueta cada pixel
            \item No existe diferencias entre\\instancias de una misma\\clase
            \end{itemize}
            """
            )
            .scale(0.9)
            .move_to(RIGHT * 4)
        )
        self.play(Write(features_text))

        self.pause()
        self.remove(mask_image)
        self.play(FadeOut(image), Uncreate(features_text))

    def section_002(self, title: Text) -> None:
        medical_images = Group(
            Group(
                ImageMobject("resources/medical-application-01.png").scale(2.0),
                Text("Radiografía de tórax").scale(0.5),
            ).arrange(DOWN),
            Group(
                ImageMobject("resources/medical-application-02.png").scale(2.0),
                Text("Resonancia magnética del cerebro").scale(0.5),
            ).arrange(DOWN, SMALL_BUFF),
        ).arrange(buff=LARGE_BUFF)

        self.play(FadeIn(medical_images))
        self.pause()
        self.play(FadeOut(medical_images))

    def section_003(self, title: Text) -> None:
        in_image = ImageLayer(read_image("resources/example-image.png")).scale(2.0)

        down_block1 = (
            Group(
                Convolutional3DLayer(3, 10, 10, filter_spacing=0.2),
                Convolutional3DLayer(3, 10, 10, filter_spacing=0.2),
            )
            .arrange(buff=0.01)
            .scale(0.5).next_to(in_image, RIGHT)
        )

        down_block2 = (
            Group(
                Convolutional3DLayer(6, 5, 5, filter_spacing=0.2),
                Convolutional3DLayer(6, 5, 5, filter_spacing=0.2),
            )
            .arrange(buff=0.01)
            .scale(0.5)
            .next_to(down_block1, DR)
        )

        down_block3 = (
            Group(
                Convolutional3DLayer(12, 2, 2, filter_spacing=0.2),
                Convolutional3DLayer(12, 2, 2, filter_spacing=0.2),
            )
            .arrange(buff=0.01)
            .scale(0.5)
            .next_to(down_block2, DR)
        )

        center_block = (
            Group(
                Convolutional3DLayer(24, 1, 1, color=GREEN, filter_spacing=0.2),
            )
            .arrange(buff=0.01)
            .scale(0.5)
            .next_to(down_block3, DR)
        )

        up_block3 = (
            Group(
                Convolutional3DLayer(12, 2, 2, color=PURPLE, filter_spacing=0.2),
                Convolutional3DLayer(12, 2, 2, color=PURPLE, filter_spacing=0.2),
            )
            .arrange(buff=0.01)
            .scale(0.5)
            .next_to(center_block, UR)
        )

        up_block2 = (
            Group(
                Convolutional3DLayer(6, 5, 5, color=PURPLE, filter_spacing=0.2),
                Convolutional3DLayer(6, 5, 5, color=PURPLE, filter_spacing=0.2),
            )
            .arrange(buff=0.01)
            .scale(0.5)
            .next_to(up_block3, UR)
        )

        up_block1 = (
            Group(
                Convolutional3DLayer(3, 10, 10, color=PURPLE, filter_spacing=0.2),
                Convolutional3DLayer(3, 10, 10, color=PURPLE, filter_spacing=0.2)
            )
            .arrange(buff=0.01)
            .scale(0.5)
            .next_to(up_block2, UR)
        )

        out_image = ImageLayer(read_image("resources/example-mask.png")).next_to(up_block1, RIGHT * 7).scale(2.0)

        skip_conn_1 = Line(start=LEFT * 3, end=RIGHT * 3).shift(UP * 1.5)
        skip_conn_2 = Line(start=LEFT * 2, end=RIGHT * 2).shift(DOWN * 1.0)
        skip_conn_3 = Line(start=LEFT * 0.5, end=RIGHT * 0.5).shift(DOWN * 2.1)

        nn = NeuralNetwork(
            it.chain(
                [in_image],
                down_block1,
                down_block2,
                down_block3,
                center_block,
                up_block3,
                up_block2,
                up_block1,
                [out_image],
            ),
            arrange_layers=False,
        ).scale(0.5)

        self.play(FadeIn(nn))
        self.wait()
        
        self.play(
            nn.make_forward_pass_animation(run_time=15),
            repeat_animation(4, ShowPassingFlash(skip_conn_1)),
            repeat_animation(4, ShowPassingFlash(skip_conn_2)),
            repeat_animation(4, ShowPassingFlash(skip_conn_3)),
        )
        self.pause()

        self.play(FadeOut(nn))


