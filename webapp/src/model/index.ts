import { v4 as uuidv4 } from 'uuid'

export class Label {
  name: string
  ingredients: Ingredient[]
  uuid: string
  created?: Date
  lastModified?: Date
  lastUsed?: Date

  constructor(name: string, ingredients: (Ingredient | string)[] = [], uuid: string = uuidv4()) {
    this.name = name
    this.ingredients = ingredients.map((ingredientOrString) => Ingredient.of(ingredientOrString))
    this.uuid = uuid
  }
}

export class Ingredient {
  name: string

  constructor(name: string) {
    this.name = name.toLocaleLowerCase()
  }

  static of(val: string | Ingredient): Ingredient {
    if (typeof val === 'string') {
      return new Ingredient(val as string)
    }

    return val as Ingredient
  }

  toString(): string {
    return this.name
  }
}

export class CompositeIngredient extends Ingredient {
  ingredients: Ingredient[]
  uuid: string
  created?: Date
  lastModified?: Date
  lastUsed?: Date

  constructor(name: string, ingredients: Ingredient[] = [], uuid: string = uuidv4()) {
    super(name)
    this.ingredients = ingredients
    this.uuid = uuid
  }

  toString(): string {
    return this.ingredients.map((i) => i.toString()).join(', ')
  }
}
