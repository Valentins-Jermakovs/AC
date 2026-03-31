<template>
  <!-- Card container -->
  <div class="bg-base-200 border border-base-300 p-5">
    <!-- Title and percentage row -->
    <div class="flex justify-between items-center gap-2">
      <!-- Card title -->
      <h3 class="text-lg font-semibold">{{ title }}</h3>

      <!-- Percentage value with dynamic color or no-data -->
      <span v-if="value && max" :class="['text-xl font-bold', colorClass]"> {{ percent }}% </span>
      <span v-else class="flex items-center gap-1 text-base-content/50 italic animate-pulse">
        <font-awesome-icon icon="fa-solid fa-circle-exclamation" />
        {{ $t('cabinet.profile.kpi.no_tasks') }}
      </span>
    </div>

    <!-- Progress bar -->
    <progress
      v-if="value && max"
      :class="['progress', progressClass, 'w-full']"
      :value="value"
      :max="max"
    ></progress>
    <progress v-else class="progress w-full"></progress>

    <!-- Numeric value display -->
    <div class="text-sm text-base-content/70 text-right">
      <span v-if="value && max">{{ value }} / {{ max }}</span>
      <span v-else>{{ $t('cabinet.profile.kpi.no_tasks') }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressCard',
  props: {
    title: String,
    value: Number,
    max: Number,
    percent: Number,
    colorClass: {
      type: String,
      default: 'text-success',
    },
    progressClass: {
      type: String,
      default: 'progress-success',
    },
  },
}
</script>

<style scoped></style>
