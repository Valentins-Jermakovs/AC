<template>
  <!-- Card container -->
  <div class="bg-base-200 border border-base-300 p-5 rounded-box">
    
    <!-- Title and percentage row -->
    <div class="flex justify-between items-center gap-2">
      <!-- Card title -->
      <h3 class="text-lg font-semibold">{{ title }}</h3>

      <!-- Percentage value with dynamic color -->
      <span :class="['text-xl font-bold', colorClass]">
        {{ percent }}%
      </span>
    </div>

    <!-- Progress bar -->
    <progress
      :class="['progress', progressClass, 'w-full']"
      :value="value"
      :max="max"
    ></progress>

    <!-- Numeric value display -->
    <div class="text-sm text-base-content/70 text-right">
      {{ value }} / {{ max }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressCard',

  props: {
    // Title shown at the top of the card
    title: String,

    // Current value of progress
    value: Number,

    // Maximum value of progress
    max: Number,

    // Percentage value (displayed on the right)
    percent: Number,

    // Text color class for percentage
    colorClass: {
      type: String,
      default: 'text-success',
    },

    // Progress bar color class
    progressClass: {
      type: String,
      default: 'progress-success',
    },
  },
}
</script>

<style scoped></style>
