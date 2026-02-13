<template>
  <section
    class="h-screen flex flex-col justify-center items-center bg-[url('@/assets/images/mate-szalontay-nzUh6sEtTsU-unsplash.jpg')] bg-cover bg-center"
  >
    <div class="flex flex-col gap-4 items-center justify-center w-full">
      <div class="p-5 lg:bg-base-200 lg:w-1/3 h-52 rounded-box lg:border-base-300">
        <h1 class="text-4xl lg:text-5xl font-bold mb-4 text-center text-white lg:text-base-content">
          {{ $t('landingPage.hero_title') }}
        </h1>
        <p class="text-lg lg:text-xl mb-8 text-center max-w-xl text-white lg:text-base-content">
          {{ $t('landingPage.hero_subtitle') }}
        </p>
      </div>
      <div class="flex gap-4">
        <RouterLink to="/login">
          <button class="btn btn-primary btn-lg">
            {{ $t('common.login') }}
          </button>
        </RouterLink>
        <RouterLink to="/register">
          <button class="btn btn-neutral btn-lg">
            {{ $t('common.register') }}
          </button>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script></script>

<style scoped></style>
