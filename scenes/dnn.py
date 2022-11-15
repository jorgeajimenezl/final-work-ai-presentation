from manim import *


class DepthNeuralNetwork(Scene):
    def construct(self):
        title = Text("Tecnologías").scale(0.9)
        title.to_edge(UP)
        line = Line(LEFT, RIGHT).scale(5)
        line.set_color(WHITE)
        line.next_to(title, DOWN)
        self.add(title, line)
        self.wait()
        
        t1 = Text('Reconocimiento de objetos').next_to(line, DOWN)
        t2 = Text('Detección de objetos').next_to(t1, DOWN)
        t3 = Text('Reconstrucción de escenas').next_to(t2, DOWN)
        t4 = Text('Restauración de imagenes').next_to(t3, DOWN)

        self.play(Create(t1))
        self.play(Create(t2))
        self.play(Create(t3))
        self.play(Create(t4))
        self.pause()

        self.play(Transform(title, Text('Deep Learing', color=BLUE).move_to(title)))
        self.play(FadeOut(t1))
        self.play(FadeOut(t2))
        self.play(FadeOut(t3))
        self.play(FadeOut(t4))

        dnn_image = ImageMobject('resources/deepl-learning.png').scale(1.5)
        self.add(dnn_image)
        self.wait(2)