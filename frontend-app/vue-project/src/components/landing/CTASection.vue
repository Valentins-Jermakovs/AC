<template>
  <section class="py-16 bg-base-200 text-center">
    <div class="container mx-auto">
      <h2 class="text-3xl font-bold mb-4">{{ $t('landingPage.CTA.title') }}</h2>
      <p class="mb-8 px-2">
        {{ $t('landingPage.CTA.description') }}
      </p>
      <div class="flex justify-center gap-4">
        <RouterLink to="/login">
          <button class="btn btn-primary btn-lg">{{ $t('common.login') }}</button>
        </RouterLink>
        <RouterLink to="/register">
          <button class="btn btn-neutral btn-lg">{{ $t('common.register') }}</button>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script></script>

<style scoped></style>
