<template>
  <header class="flex m-3 align-items-center">
    <h1 class="flex-auto">Nutrition Labels</h1>
    <i v-badge="totalQuantity" class="pi pi-tags p-overlay-badge" style="font-size: 2rem" />
  </header>
  <section>
    <div class="flex flex-auto my-3">
      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-search" />
        </InputGroupAddon>
        <InputText
          icon="pi pi-search"
          v-model="magicInputTextValue"
          placeholder="Start typing a label name..."
          @input="onMagicInputChange($event)"
          @focus="onMagicInputChange($event)"
        />
      </InputGroup>
      <OverlayPanel ref="magicInputOverlay">
        Search results will go here as well as a [CREATE NEW] button
      </OverlayPanel>
    </div>
    <DataView :value="labels" data-key="uuid" :rows="5" paginator>
      <template #list="slotProps">
        <div class="grid grid-nogutter">
          <div v-for="(item, index) in slotProps.items" :key="item.uuid" class="col-12">
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
              <div class="flex flex-column align-items-center justify-content-center gap-3 m-3">
                <template v-if="(selectedQuantityByUuid.get(item.uuid) ?? 0) > 0">
                  <InputNumber
                    class="quantity-input"
                    show-buttons
                    :model-value="selectedQuantityByUuid.get(item.uuid)"
                    button-layout="vertical"
                    :min="1"
                    @update:model-value="(val: number) => onQuantityInput(item, val)"
                  />
                  <Button class="remove" text label="Remove" @click="onRemove(item)" />
                </template>
                <template v-else
                  ><Button icon="pi pi-plus" raised rounded @click="addLabel(item)"
                /></template>
              </div>
            </div>
          </div>
        </div>
      </template>
    </DataView>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import Button from 'primevue/button'
import Chip from 'primevue/chip'
import Chips from 'primevue/chips'
import DataView from 'primevue/dataview'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import OverlayPanel from 'primevue/overlaypanel'

import BadgeDirective from 'primevue/badgedirective'

import { CompositeIngredient, Label } from '@/model'

const vBadge = BadgeDirective

const betterThanBoullionChicken = new CompositeIngredient('Better than Bouillion (Chicken)', [
  'chicken',
  'maltodextrin',
  'salt',
  'sugar',
  'food starch',
  'yeast extract',
  'tumeric'
])

const magicInputOverlay = ref<OverlayPanel | null>(null)

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

const magicInputTextValue = ref('')

const onMagicInputChange = (event: Event) => {
  if (!magicInputOverlay.value) {
    console.warn('magic input overlay not yet mounted')
    return
  }

  if (magicInputTextValue.value.length === 0) {
    magicInputOverlay.value.hide()
  } else {
    magicInputOverlay.value.show(event)
  }
}

type SelectedLabel = {
  quantity: number
  label: Label
}

const selectedLabels = ref([] as SelectedLabel[])

const addLabel = (label: Label) => {
  const currentIndex = selectedLabels.value.findIndex(
    (selectedLabel) => selectedLabel.label.uuid === label.uuid
  )
  if (currentIndex === -1) {
    selectedLabels.value.push({
      quantity: 1,
      label
    })
    return
  }

  const selectedLabel = selectedLabels.value[currentIndex]
  const updatedLabel = {
    quantity: selectedLabel.quantity + 1,
    label
  }

  selectedLabels.value.splice(currentIndex, 1, updatedLabel)
}

const selectedQuantityByUuid = computed(() => {
  return selectedLabels.value.reduce((map, label) => {
    const currentValue = map.get(label.label.uuid) ?? 0

    map.set(label.label.uuid, label.quantity + currentValue)

    return map
  }, new Map<string, number>())
})

const onQuantityInput = (label: Label, quantity: number) => {
  const currentIndex = selectedLabels.value.findIndex(
    (selectedLabel) => selectedLabel.label.uuid === label.uuid
  )

  const updatedLabel = {
    quantity,
    label
  }

  selectedLabels.value.splice(currentIndex, 1, updatedLabel)
}

const onRemove = (label: Label) => {
  const currentIndex = selectedLabels.value.findIndex(
    (selectedLabel) => selectedLabel.label.uuid === label.uuid
  )

  selectedLabels.value.splice(currentIndex, 1)
}

const totalQuantity = computed(() =>
  selectedLabels.value.reduce((sum, selectedLabel) => sum + selectedLabel.quantity, 0)
)
</script>

<style>
html {
  font-size: 16px;

  .quantity-input {
    font-size: 0.8rem;
    width: 50px;

    .p-button {
      padding: 0 1rem 0;
    }
  }

  .p-button.remove {
    font-size: 0.8rem;
    padding: 0;
  }
}
</style>
