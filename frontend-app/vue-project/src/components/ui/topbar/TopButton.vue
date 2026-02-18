<template>
  <!-- Button with an icon, emits a click event when pressed -->
  <button
    class="w-12 h-12 border-0 btn btn-neutral hover:bg-secondary tooltip tooltip-bottom"
    @click="$emit('click')"
  >
    <!-- Font Awesome icon passed via prop -->
    <font-awesome-icon :icon="icon" />
  </button>
</template>

<script>
export default {
  name: 'IconButton', // Component name

  // Props: parent must provide an icon
  props: {
    icon: { type: String, required: true },
  },

  // Emits: click event for parent to listen to
  emits: ['click'],
}
</script>

<style scoped>
/* Scoped styles for this component (currently empty) */
</style>
