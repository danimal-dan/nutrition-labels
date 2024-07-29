<template>
  <InputGroup>
    <InputGroupAddon>
      <i class="pi pi-search" />
    </InputGroupAddon>
    <InputText icon="pi pi-search" ref="magicInputTextInput" v-model="magicInputTextValue"
      placeholder="Start typing a label name..." @input="onMagicInputChange($event)" @focus="onFocus($event)" />
    <InputGroupAddon v-show="magicInputTextValue.length">
      <i class="pi pi-times" @click="magicInputTextValue = ''" />
    </InputGroupAddon>
    <OverlayPanel ref="magicInputOverlay" :pt="{ content: { class: 'p-0' } }">
      <div v-for="label in filteredLabels" :key="label.name" class="label flex flex-column border-top-2 border-200 p-3"
        @click="onLabelClick(label)">
        <strong class="label-name text-primary">{{ label.name }}</strong>
        <small class="overlay-ingredient-list font-italic">{{
          label.ingredients.join(', ')
          }}</small>
      </div>
      <div v-show="magicInputTextValue?.length" class="label create-new-panel border-top-2 border-200 p-3"
        @click="onCreateNewClick">
        <i class="pi pi-plus-circle" /> Create:
        <strong class="text-primary">{{ magicInputTextValue }}</strong>
      </div>
    </OverlayPanel>
  </InputGroup>
</template>

<script lang="ts" setup>
import { computed, ref, type ComponentPublicInstance } from 'vue'

import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import OverlayPanel from 'primevue/overlaypanel'
import { Label } from '@/model'
import { useIngredients } from '@/composables/useIngredients'

const emit = defineEmits<{
  add: [Label]
  create: [Label]
}>()

const magicInputTextInput = ref<ComponentPublicInstance | null>(null)
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

const onFocus = (event: Event) => {
  onMagicInputChange(event)
  magicInputTextInput?.value?.$el.scrollIntoView({ behavior: 'smooth' })
}

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
  new Label('Chicken', [
    'chicken',
    'onion powder',
    'garlic powder',
    'rosemary',
    'salt',
    'pepper',
    'avocado oil'
  ]),
  new Label('Pork Chop', [
    'pork',
    'onion powder',
    'garlic powder',
    'rosemary',
    'salt',
    'pepper',
    'avocado oil'
  ]),
  new Label('Blueberry Muffin', [
    'flour',
    'blueberry',
    'lemon',
    'apple sauce',
    'whole milk',
    'vegan butter',
    'sugar',
    'baking powder',
    'vanilla',
    'salt'
  ]),
  new Label('Pancakes', [
    'flour',
    'apple sauce',
    'milk',
    'avocado oil',
    'sugar',
    'baking powder',
    'vanilla',
    'salt'
  ]),
  new Label('Green Beans', [
    'green beans',
    'chicken stock',
    'salt',
    'pepper',
    'garlic powder',
    'onion powder',
    'apple cider vinegar'
  ]),
  new Label('Corn', ['corn', 'chicken stock', 'salt', 'pepper', 'garlic powder', 'onion powder']),
  new Label('Tater Tot Casserole', [
    'potatoes',
    'breakfast sausage',
    'Ripple milk',
    'flax seed',
    'salt',
    'pepper',
    'avocado oil'
  ]),
  new Label('Turkey Burger', ['turkey', 'salt', 'pepper', 'mushroom powder', 'avocado oil']),
  new Label('Boiled Potatoes', ['potato', 'salt', 'pepper']),
  new Label('Blueberry Pancakes', [
    'flour',
    'blueberry',
    'buttermilk',
    'butter',
    'baking powder',
    'baking soda',
    'salt'
  ]),
  new Label('Pork Tenderloin', ['pork', 'garlic', 'oregano', 'beef broth', 'chili powder', 'onion powder', 'brown sugar', 'butter']),
  new Label('Quinoa', ['quinoa', 'chicken broth', 'salt', 'pepper']),
  new Label('Black Beans', ['black beans', 'onion powder', 'garlic powder', 'salt', 'pepper']),
  new Label('Chicken - Italian Marinade)', ['chicken', 'olive oil', 'balsamic vinegar', 'parmesan cheese', 'romano cheese'])
] as Label[])

const filteredLabels = computed(() => {
  const searchTerm = magicInputTextValue.value?.toLocaleLowerCase() ?? ''
  if (!searchTerm.length) {
    return labels.value
  }

  return labels.value.filter((label: Label) => {
    const labelName = label.name.toLocaleLowerCase()

    return labelName.includes(searchTerm)
  })
})

const onLabelClick = (label: Label) => {
  emit('add', label)

  reset()
}

const onCreateNewClick = () => {
  const newLabel = new Label(magicInputTextValue.value)

  emit('create', newLabel)

  reset()
}

const reset = () => {
  magicInputOverlay.value?.hide()
  magicInputTextValue.value = ''
}
</script>

<style>
.label {
  cursor: pointer;
}

.label:hover .label-name {
  text-decoration: underline;
}

.label .overlay-ingredient-list {
  display: inline-block;
  max-width: 70vw;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
