from manim import *
from utils import WrappedImage, PixelsFromVect, read_image


class ImageProcessing(Scene):
    def construct(self):
        # image
        image = WrappedImage(
            PixelsFromVect(read_image("resources/mario.png", (32, 32))).scale(20.0)
        )

        #scale
        image.scale(0.7)

        title = Text("Procesamiento de Imagenes").scale(0.8)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(5)
        h_line.set_color(WHITE)
        h_line.next_to(title, DOWN)


        self.add(image.move_to(LEFT * 4))

        #pixels
        pixels = VGroup()
        for _ in range(15 * 15):
            square = Square(
                stroke_width=1.0,
            )
            pixels.add(square)
        pixels.arrange_in_grid(15, 15, buff=0)
        pixels.rescale_to_fit(image[1].length_over_dim(0), dim=0, stretch=False)
        pixels.rescale_to_fit(image[1].length_over_dim(1), dim=1, stretch=False)
        pixels.move_to(image[1])

        path = [
            'resources/mario_layer.jpg', 
            'resources/mario_layer1.jpg', 
            'resources/mario_layer2.jpg',
            'resources/mario_layer3.jpg'
        ]

        self.play(FadeIn(title), FadeIn(h_line))
        for i in range(4):
            cp = image.copy()
            self.add(cp)

            layer = WrappedImage(
                PixelsFromVect(read_image(path[i], (32, 32))).scale(20.0)
            ).scale(0.7)
            layer.move_to(image)

            self.play(
                cp[1].animate.set_opacity(0.5),
                Transform(cp, layer),
                FadeIn(
                    pixels,
                    stroke_color=WHITE,
                )
            )

            self.play(
                FadeOut(pixels),
                cp.animate.move_to(RIGHT*4)
            )
        self.wait(2)
        

            
                


