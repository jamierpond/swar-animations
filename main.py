# example.py
from manim import Animation, Scene, Text, LEFT, DOWN, UP, Line, Write, Create, GRAY, YELLOW, WHITE, FadeIn, FadeOut, ApplyMethod
import re

def CodeText(text, color=WHITE):
    return Text(text,
                font="JetBrains Mono",
                ).set_color(color)

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

# highlight appears
# result appears
# new carry (if any) appears
# highlight disappears


class BinaryAddition(Scene):
    def make_yellow(self, *args) -> list[Animation]:
        return [*[arg.animate.set_color(YELLOW) for arg in args]]

    def make_white(self, *args):
        self.play (*[arg.animate.set_color(WHITE) for arg in args] )

    def make_gray(self, *args):
        self.play (*[arg.animate.set_color(GRAY) for arg in args] )

    def construct(self):
        # Binary numbers
        num_chars = 8
        lane_size = 4

        a = 9 + 16
        b = 5 + 16 + 32
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
        carry: list[int] = [0]
        carry_text: list[Text] = [CodeText("")]
        result_digits: list[list[Text]] = [[]]
        prev_carry: list[Text] = []

        for i in range(len(a_str) - 1, -1, -1):
            # Move the carry to the next column
            next_index = i - 1
            next_char = c_str[next_index]
            if not is_digit(next_char):
                next_index -= 1

            if not is_digit(a_str[i]) and not is_digit(b_str[i]):
                result_digits[0].append(CodeText(c_str[i]).replace(result_bin[i]))
                continue

            if not is_digit(a_str[i]) or not is_digit(b_str[i]):
                raise Exception("Invalid binary number pair formatting")

            digit1 = int(a_str[i])
            digit2 = int(b_str[i])
            current_sum = digit1 + digit2 + carry[0]
            carry[0] = current_sum // 2

            digit1_text = bin1[i]
            digit1_text_after = bin1[next_index]
            digit2_text = bin2[i]
            creates_carry = carry[0] > 0

            hl_animations: list[Animation] = [digit1_text.animate.set_color(YELLOW), digit2_text.animate.set_color(YELLOW)]
            self.play(*hl_animations)

            # Draw the column's result
            result_text = CodeText(str(current_sum % 2)).replace(result_bin[i])
            result_digits[0].append(result_text)

            animations: list[Animation] = [FadeIn(result_text)]
            if creates_carry:
                carry_text[0] = CodeText(str(carry[0]), GRAY).next_to(digit1_text_after, UP)
                animations.append(FadeIn(carry_text[0]))

            self.play(*animations)

            if creates_carry:
                next_digit1_text = bin1[next_index]
                self.play(ApplyMethod(carry_text[0].next_to, next_digit1_text, UP))
            else:
                self.make_yellow(digit1_text, digit2_text)


            self.make_white(digit1_text, digit2_text)

            self.wait()



        self.wait(2)
