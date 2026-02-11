<template>
  <button class="border-0 btn btn-neutral hover:btn-primary btn-square" @click="$emit('click')">
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
