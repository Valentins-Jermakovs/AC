<template>
  <!-- Progress cards -->
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
    <!-- Active Days Card -->
    <div class="card bg-base-200 border border-base-300 rounded-none p-4 flex flex-col items-center justify-center">
      <div class="text-sm">Active Days</div>
      <div class="text-2xl font-bold mt-2">
        <template v-if="visitsStore.visits && visitsStore.visits.active_days !== undefined">
          {{ visitsStore.visits.active_days }}
        </template>
        <template v-else>
          <i class="fas fa-spinner animate-spin mr-1"></i>
          Loading...
        </template>
      </div>
    </div>

    <!-- Total Visits Card -->
    <div class="card bg-base-200 border border-base-300 rounded-none p-4 flex flex-col items-center justify-center">
      <div class="text-sm">Total Visits</div>
      <div class="text-2xl font-bold mt-2">
        <template v-if="visitsStore.visits && visitsStore.visits.total_visits !== undefined">
          {{ visitsStore.visits.total_visits }}
        </template>
        <template v-else>
          <i class="fas fa-circle-notch animate-spin mr-1"></i>
          Loading...
        </template>
      </div>
    </div>

    <!-- Total Time Card -->
    <div class="card bg-base-200 border border-base-300 rounded-none p-4 flex flex-col items-center justify-center">
      <div class="text-sm">Total Time</div>
      <div class="text-2xl font-bold mt-2">
        <template v-if="visitsStore.visits && visitsStore.visits.total_time !== undefined">
          {{ formatTime(visitsStore.visits.total_time) }}
        </template>
        <template v-else>
          <i class="fas fa-clock animate-ping mr-1 text-gray-400"></i>
          Loading...
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { useVisitsStore } from '@/stores/visits'

export default {
  name: 'VisitStatsCards',

  data() {
    return {
      visitsStore: useVisitsStore()
    }
  },

  mounted() {
    this.visitsStore.getWeekStats().catch(console.error)
  },

  methods: {
    formatTime(totalSeconds) {
      if (!totalSeconds) return '00:00'
      const hours = Math.floor(totalSeconds / 3600)
      const minutes = Math.floor((totalSeconds % 3600) / 60)
      return `${hours.toString().padStart(2,'0')}:${minutes.toString().padStart(2,'0')}`
    }
  }
}
</script>

<style scoped>
/* Tailwind + Font Awesome animācijas izmanto animate-spin un animate-ping */
</style>