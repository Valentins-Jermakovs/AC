<template>
  <!--
    Call-to-Action (CTA) Section:
    - Encourages users to take action (login or register)
    - Centered layout with title, description, and buttons
  -->
  <section class="py-16 bg-base-200 text-center">
    <div class="container mx-auto">
      
      <!-- Section title -->
      <h2 class="text-3xl font-bold mb-4">
        {{ $t('landingPage.CTA.title') }} <!-- Translated CTA title -->
      </h2>

      <!-- Section description -->
      <p class="mb-8 px-2">
        {{ $t('landingPage.CTA.description') }} <!-- Translated CTA description -->
      </p>

      <!-- Action buttons -->
      <div class="flex justify-center gap-4">
        <!-- Login button linking to /login -->
        <RouterLink to="/login">
          <button class="btn btn-primary btn-lg">
            {{ $t('common.login') }}
          </button>
        </RouterLink>

        <!-- Register button linking to /register -->
        <RouterLink to="/register">
          <button class="btn btn-neutral btn-lg">
            {{ $t('common.register') }}
          </button>
        </RouterLink>
      </div>

    </div>
  </section>
</template>

<script>
/* Empty script section: no reactive state or methods needed */
export default {
  name: 'CTASection', /* Component name */
}
</script>

<style scoped>
/* Empty style section: all styling is handled via Tailwind CSS */
</style>
