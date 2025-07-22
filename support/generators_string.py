import random
import string


class GeneratorsString:
    @staticmethod
    def generate_random_string(
        length: int = random.randint(1, 100),
        charset: string = string.ascii_letters + string.digits,
    ):
        return ''.join(random.choice(charset) for _ in range(length))
