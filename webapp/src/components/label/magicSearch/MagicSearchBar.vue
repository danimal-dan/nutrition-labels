<template>
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
    <InputGroupAddon v-show="magicInputTextValue.length">
      <i class="pi pi-times" @click="magicInputTextValue = ''" />
    </InputGroupAddon>
    <OverlayPanel ref="magicInputOverlay">
      Search results will go here as well as a [CREATE NEW] button
    </OverlayPanel>
  </InputGroup>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import OverlayPanel from 'primevue/overlaypanel'

const magicInputOverlay = ref<OverlayPanel | null>(null)

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
</script>
