<template>
  <header class="flex m-3 align-items-center">
    <h1 class="flex-auto">Nutrition Labels</h1>
    <Button
      class="text-white text-xl"
      icon="pi pi-cog"
      :pt="{ icon: { style: 'font-size: 1.5rem' } }"
      text
      rounded
      @click="onShowSettingsDialog"
    />
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
                    :input-props="{ inputmode: 'numeric' }"
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
      <Button class="text-white font-bold" rounded @click="onShowPrintDialog">Print Labels</Button>
    </div>
    <Dialog v-model:visible="printDialog.visible" modal header="Print Dialog">
      <Card
        class="print-preview mb-3 p-0"
        style="font-size: 0.8em"
        :pt="{ body: { class: 'p-1' }, content: { class: 'p-0' } }"
      >
        <template #header>
          <h3>Preview</h3>
        </template>
        <template #content>
          <ul>
            <li v-for="selectedLabel in selectedLabels" :key="selectedLabel.label.uuid">
              {{ selectedLabel.quantity }} - {{ selectedLabel.label.name }}
            </li>
          </ul>
        </template>
      </Card>
      <div class="flex flex-column mb-3">
        <label class="text-sm text-uppercase mb-1" for="childName">Child Name</label>
        <InputText id="childName" v-model="printDialog.childName" placeholder="Child Name" />
      </div>
      <div class="flex flex-column">
        <label class="text-sm text-uppercase mb-1" for="emptySlots">Empty Slots</label>
        <InputNumber
          id="emptySlots"
          v-model="printDialog.emptySlots"
          :input-props="{ inputmode: 'numeric' }"
          show-buttons
          :min="0"
          :max="16"
        />
      </div>
      <template #footer>
        <Button text @click="onCancelPrint">Cancel</Button>
        <Button
          class="text-white font-bold"
          primary
          :loading="printDialog.printing"
          @click="onPrint"
          >Print</Button
        >
      </template>
    </Dialog>
    <Dialog v-model:visible="settingsDialog.visible" modal header="Settings">
      <div class="flex flex-column mb-3">
        <label class="text-sm text-uppercase mb-1" for="settings-childName">Child Name</label>
        <InputText
          id="settings-childName"
          v-model="settingsDialog.childName"
          placeholder="Child Name"
        />
      </div>
      <div class="flex flex-column">
        <label class="text-sm text-uppercase mb-1" for="averyTemplate">Avery Template</label>
        <Dropdown
          id="averyTemplate"
          v-model="settingsDialog.averyTemplate"
          :options="settings.getAveryTemplateOptions()"
        />
      </div>
      <template #footer>
        <Button text @click="onCancelSettings">Cancel</Button>
        <Button class="text-white font-bold" primary @click="onSaveSettings">Save</Button>
      </template>
    </Dialog>
    <Toast />
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { useSettings } from '@/composables/useSettings'
import { useToast } from 'primevue/usetoast'

import Button from 'primevue/button'
import Card from 'primevue/card'
import DataView from 'primevue/dataview'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import LabelEditForm from '@/components/label/LabelEditForm.vue'
import LabelView from '@/components/label/LabelView.vue'
import MagicSearchBar from './components/label/magicSearch/MagicSearchBar.vue'
import Toast from 'primevue/toast'

import axios from 'axios'

import { Label } from '@/model'

const settings = useSettings()
const toast = useToast()

type SelectedLabel = {
  quantity: number
  label: Label
}

const selectedLabels = ref([] as SelectedLabel[])
const printDialog = ref({
  visible: false,
  childName: settings.getChildName(),
  emptySlots: 0,
  printing: false
})

const settingsDialog = ref({
  visible: false,
  childName: settings.getChildName(),
  averyTemplate: settings.getAveryTemplate()
})

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

const onShowPrintDialog = () => {
  printDialog.value.childName = settings.getChildName()
  printDialog.value.visible = true
}

const onPrint = async () => {
  const payload = {
    template: settings.getAveryTemplate(),
    headerLine: `${printDialog.value.childName} ${new Date().toLocaleDateString('en-US')}`.trim(),
    emptySlotCount: printDialog.value.emptySlots,
    labels: selectedLabels.value
  }

  if (printDialog.value.childName) {
    settings.setChildName(printDialog.value.childName)
  }

  // open window early to workaround popup-blocker for Safari on iOS
  const pdfViewer = window.open()
  try {
    printDialog.value.printing = true
    const response = await axios.post('/api/generate-pdf', payload)

    var file = new Blob([response.data], { type: 'application/pdf' })
    var fileURL = URL.createObjectURL(file)
    if (pdfViewer) {
      pdfViewer.location.href = fileURL
    } else {
      window.open(fileURL)
    }
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'PDF Generated',
      life: 3000
    })
  } catch (e: any) {
    console.error('failed to generate pdf', e)
    toast.add({
      severity: 'error',
      summary: 'Error - Failed to Generate PDF',
      detail: `${e?.message} - ${e?.response?.data}`,
      life: 3000
    })
    if (pdfViewer) {
      pdfViewer.close()
    }
  } finally {
    printDialog.value.printing = false
  }
}

const onCancelPrint = () => {
  printDialog.value.emptySlots = 0
  printDialog.value.visible = false
}

const onShowSettingsDialog = () => {
  settingsDialog.value.childName = settings.getChildName()
  settingsDialog.value.visible = true
}

const onSaveSettings = () => {
  settings.setChildName(settingsDialog.value.childName)
  settings.setAveryTemplate(settingsDialog.value.averyTemplate)
  settingsDialog.value.visible = false
}

const onCancelSettings = () => {
  settingsDialog.value.averyTemplate = settings.getAveryTemplate()
  settingsDialog.value.childName = settings.getChildName()
  settingsDialog.value.visible = false
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
@/composables/useSettings
