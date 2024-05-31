# example.py
from manim import Code, Scene, Text, LEFT, DOWN, UP, Line, Write, Create, YELLOW, WHITE, FadeIn, FadeOut, ApplyMethod
from manim_slides.slide import Slide
import re

def CodeText(text):
    return Text(text, font="JetBrains Mono")

def from_binary_string_to_int(str):
    # sanitize to only contain 0s and 1s
    str = ''.join([c for c in str if c in ['0', '1']])
    return int(str, 2)

def is_digit(c):
    return c in ['0', '1']

def num_actual_digits(num):
    return len(re.sub(r"[^0-9]", "", str(num)))

def int_to_binary_string(num, num_digits, lane_size=4):
    string = bin(num)[2:].zfill(num_digits)
    # every `lane_size` digits, add a single quote
    return "'".join([string[i:i + lane_size] for i in range(0, len(string), lane_size)])

print(int_to_binary_string(11, 16, 4))

class BinaryAddition(Scene):
    def construct(self):
        # Binary numbers
        num_chars = 8
        lane_size = 4

        a = 11
        b = 5
        c = a + b

        a_str = int_to_binary_string(a, num_chars, lane_size)
        b_str = int_to_binary_string(b, num_chars, lane_size)
        c_str = int_to_binary_string(c, num_chars, lane_size)

        # Display the binary numbers
        bin1 = CodeText(a_str).shift(UP * 2 + LEFT * 2)
        bin2 = CodeText(b_str).next_to(bin1, DOWN)
        plus = CodeText("+").next_to(bin2, LEFT)
        line = Line(bin2.get_left(), bin2.get_right()).next_to(bin2, DOWN)

        # Display the result
        result_bin = CodeText(c_str).next_to(line, DOWN)

        self.play(Write(bin1), Write(bin2), Write(plus))
        self.play(Create(line))
        self.wait()

        # Highlight the binary digits and show the addition process
        carry = 0
        carry_text = CodeText("")
        result_digits = []

        for i in range(len(a_str) - 1, -1, -1):
            # Move the carry to the next column
            next_index = i - 1
            next_char = c_str[next_index]
            if not is_digit(next_char):
                next_index -= 1

            if not is_digit(a_str[i]) and not is_digit(b_str[i]):
                result_digits.append(CodeText(c_str[i]).replace(result_bin[i]))
                continue

            if not is_digit(a_str[i]) or not is_digit(b_str[i]):
                raise Exception("Invalid binary number pair formatting")

            digit1 = int(a_str[i])
            digit2 = int(b_str[i])
            current_sum = digit1 + digit2 + carry
            carry = current_sum // 2

            digit1_text = bin1[i]
            digit2_text = bin2[i]

            self.play (
                digit1_text.animate.set_color(YELLOW),
                digit2_text.animate.set_color(YELLOW),
            )

            if carry > 0:
                carry_text = CodeText(str(carry)).next_to(digit1_text, UP)
                self.play(FadeIn(carry_text))

            # Draw the column's result
            result_text = CodeText(str(current_sum % 2)).replace(result_bin[i])
            result_digits.append(result_text)
            self.play(FadeIn(result_text))

            self.wait()

            self.play(
                digit1_text.animate.set_color(WHITE),
                digit2_text.animate.set_color(WHITE),
            )

            if carry > 0:
                if next_index >= 0:
                    next_digit1_text = bin1[next_index]
                    self.play(ApplyMethod(carry_text.next_to, next_digit1_text, UP))
                else:
                    self.play(FadeOut(carry_text))

        # Display the final result
        self.play(*[FadeOut(digit) for digit in result_digits])
        self.play(FadeIn(result_bin))

        self.wait(2)
