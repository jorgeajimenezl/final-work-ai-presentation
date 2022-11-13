from manim import *
from utils import WrappedImage, PixelsFromVect, read_image


class ImageStrcut(Scene):
    def construct(self):
        #image
        image = WrappedImage(
            PixelsFromVect(read_image("resources/mario.png", (32, 32)))
            .scale(30.0)
        )

        #copy
        cp = image[1].copy()
        cp.sort(lambda p: np.dot(p, DOWN + RIGHT))

        self.play(
            FadeIn(image[0]), 
            LaggedStartMap(FadeIn, 
            image[1])
        )
        
        self.play(
            LaggedStartMap(
                DrawBorderThenFill,
                cp,
                run_time=3,
                stroke_color=WHITE,
                remover=False,
            )
        )        
        self.wait()

        self.play(
            image.animate.scale(0.7), 
            cp.animate.scale(0.7),
        )

        #braces
        braces = VGroup(*[Brace(image[0], v) for v in (LEFT, DOWN)])
        brace_labels = VGroup(*[
            brace.get_text("32px")
            for brace in braces
        ])

        self.play(FadeIn(braces))
        self.play(FadeIn(brace_labels))
        self.wait()

        self.play(FadeOut(braces))
        self.play(FadeOut(brace_labels))
        self.play(
            image.animate.move_to(LEFT*4), 
            cp.animate.move_to(LEFT*4)
        )
        self.wait()

        # Gray escale, transparence, color
        table = ["#B8B2B6", "#84838B", "#463F43", "#A80925", "#DA1D1D"]
        color = [WHITE, BLUE, GREEN, YELLOW, RED]
        pixel = Square(side_length=0.8,color='#DA1D1D', fill_opacity=1)
        pixel.move_to(RIGHT*1.5 + UP*2.5)
        
        gray = VGroup(*[Circle(color = color, fill_opacity=1).scale(0.2) for color in table]).arrange()
        transparence = VGroup(*[Circle(color = "#DA1D1D", fill_opacity=0.25*r).scale(0.2) for r in range(5)]).arrange()
        color = VGroup(*[Circle(color = color, fill_opacity=1).scale(0.2) for color in color]).arrange()

        self.add(pixel)
        self.play(FadeIn(gray.next_to(pixel, DOWN*3)))
        self.play(FadeIn(transparence.next_to(gray, DOWN*3)))
        self.play(FadeIn(color.next_to(transparence, DOWN*3)))
        
        rect = SurroundingRectangle(gray[4], buff = SMALL_BUFF)
        self.play(Create(rect))    

        models = [Text('EG'), Text('RGB'), Text('RGBA')]
        change_color = 'red'
        
        for i,ob in enumerate([gray, transparence, color]):
            models[i].next_to(ob, RIGHT)
            models[i].scale(0.7)
            self.play(Create(models[i]))
            for n in 2, 0, 1, 4:
                self.play(
                    rect.animate.move_to(ob[n])
                )
                if ob == transparence:
                    pixel.set_opacity(ob[n].get_fill_opacity())
                else:
                    pixel.set_color(ob[n].get_color())

                    for sq in cp:
                        if str(sq.get_color()) == change_color: 
                            sq.set_fill(ob[n].get_color())
                
                    change_color = str(ob[n].get_color())
        
        self.wait()


