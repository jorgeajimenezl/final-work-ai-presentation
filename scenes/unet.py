from manim import *
from manim_slides import *

class UNet(Scene):
    def construct(self):
        text = MarkupText("Qué es segmentación semántica? 🤔")
        self.play(Write(text))

        self.wait()
