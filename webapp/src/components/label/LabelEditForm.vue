<template>
  <div class="label-edit-form">
    <InputText v-model="label.name" />
    <AutoComplete
      v-model="label.ingredients"
      :suggestions="suggestions"
      complete-on-focus
      multiple
      data-key="name"
      option-label="name"
      @complete="(val) => (autocompleteVal = val.query)"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, toRefs } from 'vue'

import { useIngredients } from '@/composables/useIngredients'

import AutoComplete from 'primevue/autocomplete'
import InputText from 'primevue/inputtext'

import { Ingredient, Label } from '@/model'

import escapeRegExp from 'lodash/escapeRegExp'

const props = defineProps({
  label: {
    type: Label,
    required: true
  }
})

const { label } = toRefs(props)

const { suggestionBank } = useIngredients()

const autocompleteVal = ref('')

const suggestions = computed(() => {
  if (autocompleteVal.value.length === 0) {
    return suggestionBank.value
  }

  const searchRegex = new RegExp(escapeRegExp(autocompleteVal.value), 'i')

  const filteredSuggestions = suggestionBank.value.filter((suggestion) =>
    suggestion.name.match(searchRegex)
  )

  const currentAutocompleteValueOption = new Ingredient(autocompleteVal.value)

  if (
    filteredSuggestions.some(
      (suggestion) =>
        suggestion.name.toLocaleLowerCase() ===
        currentAutocompleteValueOption.name.toLocaleLowerCase()
    )
  ) {
    // if there is an exact match, don't add the current autocomplete value
    return filteredSuggestions
  }

  return [currentAutocompleteValueOption, ...filteredSuggestions]
})
</script>
