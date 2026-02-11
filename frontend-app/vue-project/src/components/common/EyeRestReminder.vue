<template>
  <!-- Eye Rest Reminder -->
  <transition name="fade">
    <div v-if="show" class="fixed bottom-5 right-5 z-50">
      <div
        class="p-5 alert bg-base-100 rounded-box w-80 flex flex-col gap-2 border border-base-300"
      >
        <h3 class="font-semibold text-lg flex items-center gap-2">{{ $t('eyeRest.title') }}</h3>

        <p class="my-5">
          {{ $t('eyeRest.content') }}
        </p>

        <div class="flex justify-end gap-2">
          <button class="btn btn-neutral" @click="later">
            {{ $t('eyeRest.later') }}
          </button>
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
      show: false,
      timer: null
    }
  },

  methods: {
    remind(time) {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.show = true
      }, time)
    },

    close() {
      this.show = false
      this.remind(20 * 60 * 1000) // 20 min
    },

    later() {
      this.show = false
      this.remind(5 * 60 * 1000) // 5 min
    }
  },

  mounted() {
    this.remind(20 * 60 * 1000) // 20 min
  },

  beforeUnmount() {
    if (this.timer) clearTimeout(this.timer)
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
