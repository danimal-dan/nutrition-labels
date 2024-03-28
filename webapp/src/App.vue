<template>
  <header class="flex m-3 align-items-center">
    <h1 class="flex-auto">Nutrition Labels</h1>
    <i class="pi pi-cog" style="font-size: 1.5rem" />
  </header>
  <section>
    <div class="flex flex-auto my-3">
      <MagicSearchBar @add="onAddLabel" @create="onCreateLabel" />
    </div>
    <DataView :value="selectedLabels" data-key="uuid">
      <template #list="slotProps">
        <div class="grid grid-nogutter">
          <div v-for="(item, index) in slotProps.items" :key="item.uuid" class="col-12">
            <div class="flex" :class="{ 'border-top-1 surface-border': index !== 0 }">
              <div class="flex-auto flex-column p-4 gap-3 flex-grow">
                <LabelEditForm v-if="item.label.uuid === editModeLabelUuid" :label="item.label" />
                <LabelView v-else :label="item.label" @edit="onBeginEdit(item.label)" />
              </div>
              <div class="flex flex-column align-items-center justify-content-center gap-3 m-3">
                <template v-if="item.label.uuid === editModeLabelUuid">
                  <Button icon="pi pi-check" raised rounded @click="onEditComplete(item.label)" />
                </template>
                <template v-else>
                  <InputNumber
                    class="quantity-input"
                    show-buttons
                    v-model="item.quantity"
                    button-layout="vertical"
                    :min="1"
                  />
                  <Button class="remove" text label="Remove" @click="onRemove(item)" />
                </template>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template #empty>
        <p class="p-3 font-italic text-400">No labels selected</p>
      </template>
    </DataView>
    <div
      v-if="selectedLabels.length"
      class="action-bar surface-section border-top-2 surface-border fixed flex justify-content-center bottom-0 left-0 p-2 w-full"
    >
      <Button class="text-white" rounded @click="onPrint"><strong>Print Labels</strong></Button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import Button from 'primevue/button'
import DataView from 'primevue/dataview'
import InputNumber from 'primevue/inputnumber'
import LabelEditForm from '@/components/label/LabelEditForm.vue'
import LabelView from '@/components/label/LabelView.vue'
import MagicSearchBar from './components/label/magicSearch/MagicSearchBar.vue'

import axios from 'axios'

import { Label } from '@/model'

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

const onAddLabel = (label: Label) => {
  const currentIndex = selectedLabels.value.findIndex(
    (selectedLabel) => selectedLabel.label.uuid === label.uuid
  )
  if (currentIndex === -1) {
    selectedLabels.value.unshift({
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

const onCreateLabel = (label: Label) => {
  onAddLabel(label)
  editModeLabelUuid.value = label.uuid
}

const onRemove = (label: Label) => {
  const currentIndex = selectedLabels.value.findIndex(
    (selectedLabel) => selectedLabel.label.uuid === label.uuid
  )

  selectedLabels.value.splice(currentIndex, 1)
}

const onPrint = async () => {
  const payload = {
    template: 4224,
    emptySlotCount: 0,
    labels: selectedLabels.value
  }

  const response = await axios.post('/api/generate-pdf', payload)

  console.info('response', response)

  var file = new Blob([response.data], { type: 'application/pdf' })
  var fileURL = URL.createObjectURL(file)
  window.open(fileURL)
}
</script>

<style>
html {
  font-size: 16px;
  padding-bottom: 70px;

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
