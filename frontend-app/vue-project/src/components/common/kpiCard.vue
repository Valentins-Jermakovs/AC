<template>
  <div class="flex-1 flex flex-col gap-2 bg-base-200 border border-base-300 p-5">
    <div class="stat-title">{{ title }}</div>
    <div :class="['stat-value', colorClass]">
      <span v-if="value === 0 || value === '0'">
        {{ $t('work.projects.errors.no_data') }}
      </span>
      <span v-else>{{ value }}</span>
    </div>
    <div class="stat-desc">{{ desc }}</div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',

  props: {
    title: {
      type: String,
      required: false,
    },

    value: {
      type: [String, Number],
      required: false,
    },

    desc: {
      type: String,
      required: false,
    },

    colorClass: {
      type: String,
      default: 'text-base-content',
    },
  },
}
</script>

<style scoped></style>