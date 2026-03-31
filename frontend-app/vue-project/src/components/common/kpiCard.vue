<template>
  <div class="flex-1 flex flex-col gap-2 bg-base-200 border border-base-300 p-5">
    <div class="stat-title">{{ title }}</div>

    <div :class="['stat-value', colorClass, 'flex items-center gap-2']">
      <template v-if="value === 0 || value === '0'">
        <font-awesome-icon
          icon="fa-solid fa-spinner"
          class="animate-spin text-xl text-base-content/60"
        />
        <span class="text-2xl text-base-content/60">
          {{ $t('work.projects.errors.no_data') }}
        </span>
      </template>

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
