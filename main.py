# example.py

from manim import Text, LEFT, DOWN, UP, Line, Write, Create, YELLOW, WHITE, FadeIn, FadeOut

from manim_slides.slide import Slide


def CodeText(text):
    return Text(text, font="JetBrains Mono")


class BinaryAddition(Slide):
    def construct(self):
        # Binary numbers
        num1 = "01011"
        num2 = "00101"

        # Convert binary numbers to integer
        int1 = int(num1, 2)
        int2 = int(num2, 2)

        # Calculate the sum
        total = int1 + int2

        # Display the binary numbers
        bin1 = CodeText(num1).shift(UP * 2 + LEFT * 2)
        bin2 = CodeText(num2).next_to(bin1, DOWN)
        plus = CodeText("+").next_to(bin2, LEFT)
        line = Line(bin2.get_left(), bin2.get_right()).next_to(bin2, DOWN)

        # Display the result
        result_bin = CodeText(bin(total)[2:]).next_to(line, DOWN)
        result_int = CodeText(str(total)).next_to(result_bin, DOWN)

        self.play(Write(bin1), Write(bin2), Write(plus))
        self.play(Create(line))
        self.wait()

        self.play(Write(result_bin))
        self.play(Write(result_int))
        self.wait(2)

        # Highlight the binary digits and show the addition process
        carry = 0
        carry_text = None
        for i in range(len(num1) - 1, -1, -1):
            digit1 = int(num1[i])
            digit2 = int(num2[i]) if i < len(num2) else 0

            current_sum = digit1 + digit2 + carry
            carry = current_sum // 2

            digit1_text = bin1[i]
            digit2_text = bin2[i] if i < len(num2) else CodeText("0").next_to(bin1[i], DOWN)

            self.play(
                digit1_text.animate.set_color(YELLOW),
                digit2_text.animate.set_color(YELLOW),
            )

            if carry > 0:
                carry_text = CodeText(str(carry)).next_to(digit1_text, UP)
                self.play(FadeIn(carry_text))

            self.wait()

            self.play(
                digit1_text.animate.set_color(WHITE),
                digit2_text.animate.set_color(WHITE),
            )

            if carry > 0:
                self.play(FadeOut(carry_text))

        self.wait(2)
