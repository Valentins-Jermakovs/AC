<template>
  <!--
    Hero Section:
    - Full-screen banner for the landing page
    - Shows a background image
    - Contains main title, subtitle, and login/register buttons
  -->
  <section class="h-screen flex flex-col justify-center 
    items-center bg-[url('@/assets/images/mate-szalontay-nzUh6sEtTsU-unsplash.jpg')] 
    bg-cover bg-center">
    <!-- Wrapper for centering content -->
    <div class="flex flex-col gap-4 
    items-center justify-center w-full">

      <!-- Text container with optional background on large screens -->
      <div class="p-5 lg:bg-base-200 lg:w-1/3 h-52 
      rounded-box lg:border-base-300">
        <!-- Main title -->
        <h1 class="text-4xl lg:text-5xl font-bold 
        mb-4 text-center text-white lg:text-base-content">
          {{ $t('landingPage.hero_title') }} <!-- Translated hero title -->
        </h1>

        <!-- Subtitle / description -->
        <p class="text-lg lg:text-xl mb-8 text-center 
        max-w-xl text-white lg:text-base-content">
          {{ $t('landingPage.hero_subtitle') }} <!-- Translated hero subtitle -->
        </p>
      </div>

      <!-- Action buttons -->
      <div class="flex gap-4">
        <!-- Login button linking to /login -->
        <RouterLink to="/login">
          <button class="btn btn-primary btn-lg">
            {{ $t('common.login') }} <!-- Translated login text -->
          </button>
        </RouterLink>

        <!-- Register button linking to /register -->
        <RouterLink to="/register">
          <button class="btn btn-neutral btn-lg">
            {{ $t('common.register') }} <!-- Translated register text -->
          </button>
        </RouterLink>
      </div>

    </div>
  </section>
</template>

<script>
// Empty script section: no reactive state or methods needed
</script>

<style scoped>
/* Empty style section: all styles are applied via Tailwind CSS */
</style>
