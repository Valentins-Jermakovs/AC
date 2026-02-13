<template>
  <div class="w-full min-h-screen flex flex-col justify-center items-center p-5 lg:p-10">
    
    <!-- Main 404 -->
    <div class="flex flex-col items-center gap-6 text-center animate-fadeIn">
      <h1 class="text-6xl lg:text-9xl font-extrabold text-error drop-shadow-lg">
        404
      </h1>

      <!-- Subtitle / message -->
      <div class="flex flex-col gap-2 items-center max-w-lg">
        <h2 class="text-xl lg:text-3xl font-semibold opacity-55">
          {{ $t('errors.404') }}
        </h2>
      </div>

      <!-- Optional decorative icon -->
      <div class="text-6xl mt-5 animate-bounce">
        <font-awesome-icon icon="question-circle" />
      </div>
    </div>

    <!-- Button -->
    <button 
      class="btn btn-primary btn-lg mt-10 hover:scale-105 transition-transform duration-300 shadow-lg"
      @click="goBack"
    >
      {{ $t('common.back') }}
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    goBack() {
      this.$router.go(-1)
    },
  },
}
</script>

<style scoped>
/* Simple fade-in animation */
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(-20px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.8s ease-out forwards;
}
</style>
