<template>
  <button
    class="w-12 h-12 border-0 btn btn-neutral hover:bg-secondary tooltip tooltip-bottom"
    @click="$emit('click')"
  >
    <font-awesome-icon :icon="icon" />
  </button>
</template>

<script>
export default {
  name: 'IconButton',
  props: {
    icon: { type: String, required: true },
  },
  emits: ['click'],
}
</script>

<style scoped></style>
