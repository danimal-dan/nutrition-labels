<template>
  <div class="label-view">
    <h3 class="mt-0">
      {{ label.name }}
      <Button
        icon="pi pi-pencil"
        style="width: 1.5rem; height: 1.5rem"
        rounded
        text
        @click="() => emit('edit', label)"
      />
    </h3>
    <div class="flex flex-wrap gap-1">
      <Chip
        style="font-size: 0.8em"
        v-for="ingredient in label.ingredients"
        :key="ingredient.name"
        :label="ingredient.name"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { toRefs } from 'vue'

import Button from 'primevue/button'
import Chip from 'primevue/chip'

import { Label } from '@/model'

const props = defineProps({
  label: {
    type: Label,
    required: true
  }
})

const { label } = toRefs(props)

const emit = defineEmits<{
  edit: [Label]
}>()
</script>
