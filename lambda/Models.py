from uuid import uuid4
from typing import List, Union, Optional

class IngredientJsonFactory:
    @staticmethod
    def load(data: Union[dict, str]):
        if (isinstance(data, dict)) and 'ingredients' in data:
            return CompositeIngredient(**data)
        else:
            return Ingredient.of(data)

class Ingredient:
    def __init__(self, name: str, uuid: str = None):
        self.name = name.lower()
        self.uuid = uuid
    
    @classmethod
    def of(cls, val: Union[dict, 'Ingredient', str]):
        if isinstance(val, str):
            return cls(val)
        if isinstance(val, dict):
            return cls(**val)
        return val
    
    
    def getListing(self):
        return [str(self)]

    def __str__(self):
        return self.name

class CompositeIngredient(Ingredient):
    def __init__(self, name: str, ingredients: List[Ingredient] = [], uuid: str = None):
        super().__init__(name)
        self.ingredients = ingredients
        self.uuid = uuid or str(uuid4())
        self.created = None
        self.lastModified = None
        self.lastUsed = None

    def getListing(self):
        return [str(ingredient) for ingredient in self.ingredients]

    def __str__(self):
        return ', '.join([str(ingredient) for ingredient in self.ingredients])
    
class Label:
    def __init__(self, name: str, ingredients: List[Union[dict, Ingredient, str]] = [], uuid: str = None):
        self.name = name
        self.ingredients = [IngredientJsonFactory.load(ingredient) for ingredient in ingredients]
        self.uuid = uuid or str(uuid4())
        self.created = None
        self.lastModified = None
        self.lastUsed = None

    def getIngredientList(self):
        return list(set([item for ingredient in self.ingredients for item in ingredient.getListing()]))

    
class LabelQuantityPair:
    def __init__(self, quantity: int, label: Union[dict, Label]):
        self.quantity = quantity
        self.label =  Label(**label) if isinstance(label, dict) else label
