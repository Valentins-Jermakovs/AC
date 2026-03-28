<template>
  <div class="flex items-center justify-between mb-3">
    <h2 class="text-xl font-semibold">
      {{ months[month] }} {{ year }}
    </h2>

    <div class="flex gap-2">
      <button class="btn btn-neutral" @click="$emit('prev')">
        ‹
      </button>

      <button class="btn btn-neutral" @click="$emit('next')">
        ›
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CalendarHeader',

  props: {
    year: Number,
    month: Number,
    months: Array,
  },

  emits: ['prev', 'next'],
}
</script>