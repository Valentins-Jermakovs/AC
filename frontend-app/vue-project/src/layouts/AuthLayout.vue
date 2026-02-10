<template>
  <div class="flex h-full">
    <!-- Form section -->
    <div class="flex flex-col w-full md:w-1/3 lg:w-1/5 xl:w-1/4 p-5">
      <slot></slot>
    </div>
    <!-- Image section -->
    <div
      class="hidden md:block flex-1 bg-[url('@/assets/images/cader_-JiV-8Zf8FfU-unsplash.jpg')] bg-cover bg-center"
    ></div>
  </div>
</template>

<script setup></script>

<style scoped></style>