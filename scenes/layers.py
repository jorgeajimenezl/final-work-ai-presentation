from manim import *
from manim_ml.neural_network.layers.parent_layers import ConnectiveLayer
from manim_ml.neural_network.layers import ImageLayer, Convolutional3DLayer


class Convolutional3DToImage(ConnectiveLayer):
    input_class = ImageLayer
    output_class = Convolutional3DLayer

    def __init__(
        self,
        input_layer,
        output_layer,
        pulse_color=ORANGE,
        **kwargs
    ):
        super().__init__(
            input_layer,
            output_layer,
            input_class=ImageLayer,
            output_class=Convolutional3DLayer,
            **kwargs
        )
        self.pulse_color = pulse_color

        self.conv_layer = output_layer
        self.image_layer = input_layer

    def make_forward_pass_animation(self, layer_args={}, run_time=1.5, **kwargs):
        animations = []

        image_mobject = self.image_layer.image_mobject
        image_location = image_mobject.get_center()

        output_rectangle = self.output_layer.rectangles[0]
        output_vertices = output_rectangle.get_vertices()

        for vertex in output_vertices:
            line = Line(
                start=image_location, end=vertex, color=self.color, stroke_opacity=0.0
            )
            animations.append(
                ShowPassingFlash(
                    line.set_color(self.pulse_color).set_stroke(opacity=1.0),
                    time_width=0.5,
                    run_time=run_time,
                )
            )

        animation_group = AnimationGroup(*animations)
        return animation_group

    @override_animation(Create)
    def _create_override(self, **kwargs):
        return AnimationGroup()

class ImageToConvolutional3D(ConnectiveLayer):
    input_class = Convolutional3DLayer
    output_class = ImageLayer

    def __init__(
        self,
        input_layer,
        output_layer,
        pulse_color=ORANGE,
        **kwargs
    ):
        super().__init__(
            input_layer,
            output_layer,
            input_class=Convolutional3DLayer,
            output_class=ImageLayer,
            **kwargs
        )
        self.pulse_color = pulse_color

        self.conv_layer = input_layer
        self.image_layer = output_layer

    def make_forward_pass_animation(self, layer_args={}, run_time=1.5, **kwargs):
        animations = []

        image_mobject = self.image_layer.image_mobject
        image_location = image_mobject.get_center()

        output_rectangle = self.output_layer.rectangles[0]
        output_vertices = output_rectangle.get_vertices()

        for vertex in output_vertices:
            line = Line(
                start=vertex, end=image_location, color=self.color, stroke_opacity=0.0
            )
            animations.append(
                ShowPassingFlash(
                    line.set_color(self.pulse_color).set_stroke(opacity=1.0),
                    time_width=0.5,
                    run_time=run_time,
                )
            )

        animation_group = AnimationGroup(*animations)
        return animation_group

    @override_animation(Create)
    def _create_override(self, **kwargs):
        return AnimationGroup()

