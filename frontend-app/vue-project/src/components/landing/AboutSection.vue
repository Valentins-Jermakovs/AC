<template>
  <section class="py-10 bg-base-200">
    <div class="container mx-auto flex flex-col md:flex-row items-stretch gap-8">
      <!-- Image + Skeleton -->
      <div class="md:w-1/2 relative">
        <!-- Skeleton -->
        <div v-if="!loaded" class="skeleton w-full h-full rounded-box absolute inset-0"></div>

        <!-- Image -->
        <img
          src="@/assets/illustrations/11669206_20945802.jpg"
          alt="About"
          class="rounded-box transition-opacity duration-1000 w-full h-full object-cover"
          :class="{ 'opacity-0': !loaded, 'opacity-100': loaded }"
          @load="loaded = true"
          loading="lazy"
        />
      </div>

      <!-- Text -->
      <div class="md:w-1/2 p-5 lg:p-10">
        <h2 class="text-5xl font-bold mb-4 text-base-content">
          {{ $t('landingPage.about_title') }}
        </h2>
        <p class="mb-4 text-base-content text-xl">
          {{ $t('landingPage.about_content') }}
        </p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      loaded: false,
    }
  },
}
</script>
