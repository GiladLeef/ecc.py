import random
from ecc import *

class Kangaroo:
    def __init__(self, target):
        self.target = target
        self.position = None
        self.steps = 0
        self.basket = {}

    def move(self):
        step_size = random.randint(1, 2)
        self.position = mul(G, self.steps + step_size)
        self.steps += step_size

    def run(self):
        self.position = G
        while True:
            if self.position == self.target:
                return self.steps

            current_y = self.position.y
            self.basket[(current_y, self.position.x)] = self.steps

            if current_y in self.basket:
                steps_a = self.basket[current_y]
                steps_b = self.steps
                return (steps_b - steps_a) % N

            self.move()

def main():
    target_point = G * 1234
    kangaroo = Kangaroo(target_point)
    result = kangaroo.run()

    if result is not None:
        print(f"Discrete log found: {result}")
    else:
        print("Discrete log not found.")

if __name__ == "__main__":
    main()
