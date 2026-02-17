<template>
  <!--
    Footer Section:
    - Appears at the bottom of the page
    - Contains copyright, social links, and document links
  -->
  <footer class="py-6 bg-base-100 border-t border-base-300 text-center text-sm">
    
    <!-- Copyright text -->
    <p class="mb-2">
      {{ $t('landingPage.footer.copyright') }}
    </p>

    <div class="flex flex-col justify-center gap-4">

      <!-- Social media links -->
      <div class="flex items-center justify-center gap-4 text-2xl">
        <!-- GitHub link -->
        <a href="https://github.com/Valentins-Jermakovs/AC" aria-label="GitHub">
          <font-awesome-icon icon="fa-brands fa-github" />
        </a>

        <!-- Twitter link (placeholder) -->
        <a href="#" aria-label="Twitter">
          <font-awesome-icon icon="fa-brands fa-twitter" />
        </a>

        <!-- Email link -->
        <a href="mailto:jermakovsvalentins@gmail.com" aria-label="Email">
          <font-awesome-icon icon="fa-envelope" />
        </a>
      </div>

      <!-- Footer document links -->
      <div class="flex flex-col md:flex-row items-center justify-center gap-4
      underline text-primary">
        <!-- Privacy policy -->
        <a
          href="/documents/policy.pdf"
          target="_blank"
          rel="noopener noreferrer"
          class="hover:underline"
        >
          {{ $t('landingPage.footer.privacy') }}
        </a>

        <!-- License / terms -->
        <a
          href="/documents/license.pdf"
          target="_blank"
          rel="noopener noreferrer"
          class="hover:underline"
        >
          {{ $t('landingPage.footer.terms') }}
        </a>
      </div>

    </div>
  </footer>
</template>

<script>
/* Empty script section: no reactive state or methods needed */
export default {
  name: 'FooterSection', /* Component name */
}
</script>

<style scoped>
/* Empty style section: all styling is handled via Tailwind CSS */
</style>
