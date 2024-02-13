<template>
  <header class="m-3"><h1>Nutrition Labels</h1></header>
  <section>
    <DataView :value="labels" data-key="name" :rows="5" paginator>
      <template #list="slotProps">
        <div class="grid grid-nogutter">
          <div v-for="(item, index) in slotProps.items" :key="index" class="col-12">
            <div class="flex" :class="{ 'border-top-1 surface-border': index !== 0 }">
              <div class="flex-auto flex-column p-4 gap-3 flex-grow">
                <h3 class="mt-0">
                  {{ item.name }}
                  <Button icon="pi pi-pencil" style="width: 1.5rem; height: 1.5rem" rounded text />
                </h3>
                <template v-if="true">
                  <!-- aka view mode -->
                  <div class="flex flex-wrap gap-1">
                    <Chip v-for="ingredient in item.ingredients" :label="ingredient.toString()" />
                  </div>
                </template>
                <template v-else>
                  <Chips v-model="item.ingredients" />
                </template>
              </div>
              <div class="flex flex-row align-items-center gap-3 m-3">
                <Button icon="pi pi-plus" raised rounded />
              </div>
            </div>
          </div>
        </div>
      </template>
    </DataView>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import Button from 'primevue/button'
import Chip from 'primevue/chip'
import Chips from 'primevue/chips'
import DataView from 'primevue/dataview'

class Label {
  name: string
  ingredients: (Ingredient | string)[]
  created?: Date
  lastModified?: Date
  lastUsed?: Date

  constructor(name: string, ingredients: (Ingredient | string)[] = []) {
    this.name = name
    this.ingredients = ingredients
  }
}

class Ingredient {
  name: string

  constructor(name: string) {
    this.name = name
  }

  toString(): string {
    return this.name
  }
}

class CompositeIngredient extends Ingredient {
  ingredients: (Ingredient | string)[]
  created?: Date
  lastModified?: Date
  lastUsed?: Date

  constructor(name: string, ingredients: (Ingredient | string)[] = []) {
    super(name)
    this.ingredients = ingredients
  }

  toString(): string {
    return this.ingredients.map((i) => i.toString()).join(', ')
  }
}

const betterThanBoullionChicken = new CompositeIngredient('Better than Bouillion (Chicken)', [
  'chicken',
  'maltodextrin',
  'salt',
  'sugar',
  'food starch',
  'yeast extract',
  'tumeric'
])

const labels = ref([
  new Label('Roasted Carrots', ['carrots', 'salt', 'pepper', 'avocado oil']),
  new Label('Hamburger', [
    'beef',
    'onion powder',
    'garlic powder',
    'salt',
    'pepper',
    'avocado oil'
  ]),
  new Label('Green Beans', [
    'green beans',
    betterThanBoullionChicken,
    'salt',
    'pepper',
    'mushroom powder',
    'apple cider vinegar'
  ])
] as Label[])

onMounted(() => {})
</script>

<style>
html {
  font-size: 16px;
}
</style>
