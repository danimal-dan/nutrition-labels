from typing import List
from Models import Label, CompositeIngredient


class EmptySpacerLabel(Label):
    def __init__(self):
        super().__init__('', [])

class BlackEyePeas(Label):
    def __init__(self):
        super().__init__('Black Eye Peas', ['salt', 'pepper'])

class ButtRub(CompositeIngredient):
    def __init__(self):
        super().__init__('Butt Rub', ['salt', 'pepper', 'garlic', 'paprika', 'chipotle powder'])

class Chicken(Label):
    def __init__(self):
        super().__init__('Chicken', [ButtRub(), 'salt', 'pepper', 'lemon', 'thyme', 'oregano'])

class Grits(Label):
    def __init__(self):
        super().__init__('Grits', ['salt', 'pepper', 'vegan butter (nut free)', 'vegan heavy cream (nut free)'])

class Broccoli(Label):
    def __init__(self):
        super().__init__('Steamed Broccoli', [])

class DirtyRice(Label):
    def __init__(self):
        super().__init__('Dirty Rice', ['basmati rice', 'green pepper', 'celery', 'onion', 'garlic', 'oregano', 'avocado oil', 'salt', 'pepper'])
