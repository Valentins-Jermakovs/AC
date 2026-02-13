<template>
  <div class="bg-base-200 border border-base-300 rounded-box p-5 flex flex-col gap-3">
    <h3 class="text-lg font-semibold mb-2">
      {{ $t('cabinet.profile.actions.title') }}
    </h3>
    <button
      v-for="(action, index) in actions"
      :key="index"
      class="btn btn-neutral w-full justify-start"
      @click="$emit('action-click', action.key)"
    >
      {{ action.title }}
    </button>
  </div>
</template>

<script>
export default {
  props: {
    actions: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style scoped></style>
