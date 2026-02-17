<template>
  <div class="w-full min-h-screen flex flex-col justify-center items-center p-5 lg:p-10">
    <!-- Titles -->
    <div class="flex flex-col gap-3 items-center text-center animate-fadeIn">
      <h1 class="text-5xl lg:text-7xl font-extrabold text-primary drop-shadow-lg">
        {{ $t('logout.title') }}
      </h1>
    </div>

    <!-- Illustration Image -->
    <div class="my-8 w-full flex justify-center animate-bounce">
      <img
        class="w-full max-w-lg h-auto"
        src="@/assets/illustrations/undraw_reading-time_gcvc.svg"
        alt="Logout Illustration"
      />
    </div>

    <!-- Back/Home Button -->
    <button
      class="btn btn-primary text-lg lg:text-xl px-6 py-3 shadow-lg transition-transform duration-300 hover:scale-105 hover:shadow-2xl"
      @click="$router.push('/')"
    >
      {{ $t('logout.confirm') }}
    </button>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
/* Fade-in animation for the title section */
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.8s ease-out forwards;
}

/* Optional: bounce effect for the illustration */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}
.animate-bounce {
  animation: bounce 2s infinite;
}
</style>
