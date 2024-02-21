<template>
  <header class="flex m-3 align-items-center">
    <h1 class="flex-auto">Nutrition Labels</h1>
    <i v-badge="totalQuantity" class="pi pi-tags p-overlay-badge" style="font-size: 2rem" />
  </header>
  <section>
    <div class="flex flex-auto my-3">
      <MagicSearchBar />
    </div>
    <DataView :value="labels" data-key="uuid" :rows="5" paginator>
      <template #list="slotProps">
        <div class="grid grid-nogutter">
          <div v-for="(item, index) in slotProps.items" :key="item.uuid" class="col-12">
            <div class="flex" :class="{ 'border-top-1 surface-border': index !== 0 }">
              <div class="flex-auto flex-column p-4 gap-3 flex-grow">
                <LabelEditForm v-if="item.uuid === editModeLabelUuid" :label="item" />
                <LabelView v-else :label="item" @edit="onBeginEdit(item)" />
              </div>
              <div class="flex flex-column align-items-center justify-content-center gap-3 m-3">
                <template v-if="item.uuid === editModeLabelUuid">
                  <Button icon="pi pi-check" raised rounded @click="onEditComplete(item)" />
                </template>
                <template v-else>
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
                </template>
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
import DataView from 'primevue/dataview'
import InputNumber from 'primevue/inputnumber'
import LabelEditForm from '@/components/label/LabelEditForm.vue'
import LabelView from '@/components/label/LabelView.vue'
import MagicSearchBar from './components/label/magicSearch/MagicSearchBar.vue'

import { useIngredients } from '@/composables/useIngredients'

import BadgeDirective from 'primevue/badgedirective'

import { Label } from '@/model'

const vBadge = BadgeDirective

const { betterThanBoullionChicken } = useIngredients()

const labels = ref([
  new Label('Roasted Carrots', ['carrot', 'salt', 'pepper', 'avocado oil']),
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

type SelectedLabel = {
  quantity: number
  label: Label
}

const selectedLabels = ref([] as SelectedLabel[])

const editModeLabelUuid = ref(undefined as undefined | string)

const onBeginEdit = (label: Label) => {
  editModeLabelUuid.value = label.uuid
}

const onEditComplete = (label: Label) => {
  console.info('edit complete', label)
  editModeLabelUuid.value = undefined
}

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
