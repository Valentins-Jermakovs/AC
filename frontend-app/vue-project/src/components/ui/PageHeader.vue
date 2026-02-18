<template>
  <!-- Hero section with background image and title -->
  <div
    class="w-full h-40 sm:h-48 md:h-56 bg-base-200 
    flex items-end justify-start p-4 sm:p-5 bg-cover bg-center"
    :style="{ backgroundImage: `url(${imageUrl})` }"
  >
    <!-- Page title overlaid on the image -->
    <h1
      class="text-3xl text-white sm:text-4xl md:text-5xl 
      lg:text-6xl font-light ml-4 sm:ml-6 md:ml-10 lg:ml-25"
    >
      {{ title }}
    </h1>
  </div>
</template>

<script>
export default {
  name: 'PageHero',

  props: {
    // Title text displayed over the hero image
    title: {
      type: String,
      default: '',
    },
    // URL of the background image
    imageUrl: {
      type: String,
      default: '',
    },
  },
}
</script>

<style scoped></style>
