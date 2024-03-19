from typing import List
from Models import Label, CompositeIngredient


class EmptySpacerLabel(Label):
    def __init__(self):
        super().__init__('', [])

class FullSampler(Label):
    def __init__(self):
        super().__init__('Full Long Sampler', ['salt', 'pepper', 'salt2', 'pepper2', 'salt3', 'pepper3', 'salt4', 'pepper4', 'salt5', 'pepper5', 'salt6', 'pepper6', 'salt7', 'pepper7', 'salt8', 'pepper8', 'salt9', 'pepper9', 'salt10', 'pepper10', 'salt11', 'pepper11', 'salt12', 'pepper12', 'salt13', 'pepper13', 'salt14', 'pepper14', 'salt15', 'pepper15', 'salt16', 'pepper16', 'salt17', 'pepper17', 'salt18', 'pepper18', 'salt19', 'pepper19', 'salt20', 'pepper20', 'salt21', 'pepper21'])

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
