from manim import *
from manim_slides import *

class Presentation(Slide):
    def construct(self):
        text = Text("Trabajo final\nde\nInteligencia Artificial")
        title = Text("Título:\nSegmentación semantica de imágenes")
        authors = Tex(
            "Autores:\n\n"
            r"\begin{itemize}"
            "\n"
            r"\item Jorge Alejandro Jiménez Luna"
            "\n"
            r"\item Luis Miguel Casañ Gonzáles"
            "\n"
            r"\end{itemize}",
            tex_environment="flushleft"
        )

        self.play(Write(text))
        self.pause()
        self.play(Transform(text, title))
        self.pause()
        self.play(Transform(text, authors))
        self.pause()
        self.play(FadeOut(text))
        self.pause()
        self.wait()