<template>
  <div class="w-full min-h-screen flex flex-col justify-around items-center p-5 lg:p-10">
    <div class="flex flex-col items-center gap-5">
      <h1 class="text-5xl lg:text-8xl font-extrabold">404</h1>

      <!-- Titles -->
      <div class="flex flex-col gap-2 items-center mt-5">
        <h2 class="text-lg lg:text-xl opacity-70">
          {{ $t('errors.404') }}
        </h2>
      </div>
    </div>

    <!-- Button -->
    <button class="btn btn-primary btn-lg" @click="goBack">
      <font-awesome-icon icon="arrow-left" />
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
