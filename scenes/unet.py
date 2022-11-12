from manim import *

class UNet(Scene):
    def construct(self):
        text = Text("Qué es segmentación semántica?")
        self.play(Write(text))
        self.pause()

        self.play(
            text.animate.scale(0.8).to_corner(UP),
        )

        self.wait()
