<template>
  <!-- Eye Rest Reminder popup with fade transition -->
  <transition name="fade">
    <div v-if="show" class="fixed bottom-5 right-5 z-50">
      <div
        class="p-5 shadow alert bg-base-100 rounded-box w-80 flex flex-col gap-2 border border-base-300"
      >
        <!-- Reminder title -->
        <h3 class="font-semibold text-lg flex items-center gap-2">{{ $t('eyeRest.title') }}</h3>

        <!-- Reminder content -->
        <p class="my-5">
          {{ $t('eyeRest.content') }}
        </p>

        <!-- Action buttons -->
        <div class="flex justify-end gap-2">
          <!-- Remind later -->
          <button class="btn btn-neutral" @click="later">
            {{ $t('eyeRest.later') }}
          </button>
          <!-- Close and restart 20-min timer -->
          <button class="btn btn-primary" @click="close">
            {{ $t('eyeRest.close') }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'EyeRestReminder',

  data() {
    return {
      show: false, // controls visibility of the reminder
      timer: null, // stores the timeout ID
    }
  },

  methods: {
    // Start a timer to show the reminder after `time` milliseconds
    remind(time) {
      if (this.timer) clearTimeout(this.timer) // clear previous timer if any
      this.timer = setTimeout(() => {
        this.show = true
      }, time)
    },

    // Close the reminder and set a 20-min timer to remind again
    close() {
      this.show = false
      this.remind(20 * 60 * 1000) // 20 minutes
    },

    // Close the reminder and set a 5-min snooze timer
    later() {
      this.show = false
      this.remind(5 * 60 * 1000) // 5 minutes
    },
  },

  mounted() {
    // Start the initial 20-min timer on mount
    this.remind(20 * 60 * 1000)
  },

  beforeUnmount() {
    // Clear any running timer when component is destroyed
    if (this.timer) clearTimeout(this.timer)
  },
}
</script>

<style scoped>
/* Fade transition for the reminder */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
