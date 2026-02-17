<template>
  <div
    class="w-full min-h-screen flex flex-col justify-center items-center 
    p-5 lg:p-10 bg-linear-to-b from-base-200 via-base-100 to-base-200"
  >
    <!-- Main Titles Section -->
    <div class="flex flex-col gap-3 items-center text-center animate-fadeIn">
      <!-- Big headline -->
      <h1 class="text-5xl lg:text-6xl font-extrabold text-primary drop-shadow-lg">
        {{ $t('modals.email.received') }}
      </h1>
      <!-- Supporting subheadline -->
      <h2 class="text-2xl lg:text-3xl font-semibold text-base-content opacity-80">
        {{ $t('modals.email.received_content') }}
      </h2>
    </div>

    <!-- Illustration -->
    <div class="my-10 w-full flex justify-center animate-bounce">
      <img
        class="w-full max-w-md h-auto rounded-lg shadow-xl"
        src="@/assets/illustrations/undraw_idea_hz8b.svg"
        alt="Email received illustration"
      />
    </div>

    <!-- Back Button -->
    <button
      class="btn btn-primary text-lg 
      lg:text-xl px-8 py-3 shadow-lg transform 
      transition-transform duration-300 hover:scale-105 hover:shadow-2xl"
      @click="goBack"
    >
      {{ $t('common.back') }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'EmailReceivedView', // Component name

  methods: {
    // Navigate back to the previous page in history
    goBack() {
      this.$router.go(-1)
    },
  },
}
</script>

<style scoped>
/* Fade-in effect for titles */
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

/* Bounce effect for illustration */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
.animate-bounce {
  animation: bounce 2s infinite;
}
</style>
