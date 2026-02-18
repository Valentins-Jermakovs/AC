<template>
  <div class="flex h-full">
    <!-- Left section for form content (slot allows dynamic content) -->
    <div class="flex flex-col w-full md:w-1/3 lg:w-1/5 xl:w-1/4 p-5">
      <slot></slot>
    </div>

    <!-- Right section for an illustration image (hidden on small screens) -->
    <div
      class="hidden md:block flex-1 
      bg-[url('@/assets/images/mahdi-naserinejad-JSfGnItLmt8-unsplash.jpg')] 
      bg-cover bg-center"
    ></div>
  </div>
</template>

<script setup>
/* Empty script setup: this layout is purely presentational */
</script>

<style scoped>
/* No additional styles; layout handled via Tailwind CSS */
</style>
