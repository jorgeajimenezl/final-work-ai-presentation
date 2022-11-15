from manim import *
from utils import WrappedImage, PixelsFromVect, read_image


class ComputerVision(Scene):
    def construct(self):
        #text
        proc = Text('Procesamiento')
        op = Text('+')
        text = Text('Caraterísticas')
        op.to_edge(UP)
       
        self.play(FadeIn(op), FadeIn(proc.next_to(op, LEFT)), FadeIn(text.next_to(op, RIGHT)))
       
        self.wait(3)
        self.play(Transform(text,Text('Análisis').move_to(text)))
        self.pause()
        #self.play(Create(SurroundingRectangle(text, buff=SMALL_BUFF, stroke_color=WHITE)))
       
        line = Line(LEFT, RIGHT).scale(5)
        line.set_color(WHITE)
        line.next_to(op, DOWN)

        arr_right = Arrow(np.array([5, 3.15, 0]), np.array([5, 2, 0]))
        arr_left = Arrow(np.array([-5, 3.15, 0]), np.array([-5, 2, 0]))
        self.play(Create(line))
        self.play(Create(arr_right), Create(arr_left))

        men = Text('Hombre')
        pc = Text('PC')
        cv = Tex(r'Visión \\por\\Computador')

        self.play(Create(men.next_to(arr_left, DOWN)))
        self.play(Create(SurroundingRectangle(men, buff=SMALL_BUFF, stroke_color=WHITE)))

        # image
        lung_image = ImageMobject('resources/lung.png').scale(0.5)
        vibrio_image = ImageMobject('resources/vibrio.jpg').scale(1.28)
        cv_image = ImageMobject('resources/cv.png').scale(1.4)
        self.add(lung_image.next_to(men, DOWN))
        self.add(vibrio_image.next_to(lung_image, DOWN))

        self.pause()

        self.play(Create(pc.next_to(arr_right, DOWN)))
        self.play(Create(SurroundingRectangle(pc, buff=SMALL_BUFF, stroke_color=WHITE)))
        
        self.play(Create(cv.next_to(pc, DOWN)))
        self.play(Create(SurroundingRectangle(cv, buff=SMALL_BUFF, stroke_color=WHITE)))
        self.add(cv_image.next_to(cv, DOWN))

        self.wait(2)
