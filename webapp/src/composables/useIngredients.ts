import { CompositeIngredient, Ingredient } from '@/model'
import { ref, type Ref } from 'vue'

export const betterThanBoullionChicken = new CompositeIngredient(
  'Better than Bouillion (Chicken)',
  [
    new Ingredient('chicken'),
    new Ingredient('maltodextrin'),
    new Ingredient('salt'),
    new Ingredient('sugar'),
    new Ingredient('food starch'),
    new Ingredient('yeast extract'),
    new Ingredient('tumeric')
  ]
)

export const useIngredients = (): {
  betterThanBoullionChicken: typeof betterThanBoullionChicken
  suggestionBank: Ref<Ingredient[]>
} => {
  const suggestionBank: Ref<Ingredient[]> = ref([
    betterThanBoullionChicken,
    new Ingredient('salt'),
    new Ingredient('pepper'),
    new Ingredient('mushroom powder'),
    new Ingredient('avocado oil'),
    new Ingredient('apple cider vinegar'),
    new Ingredient('garlic power'),
    new Ingredient('onion powder'),
    new Ingredient('beef'),
    new Ingredient('pork'),
    new Ingredient('chicken'),
    new Ingredient('carrot')
  ])

  return {
    betterThanBoullionChicken,
    suggestionBank
  }
}
