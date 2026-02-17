<template>
  <!-- Language Selector button -->
  <!-- Fixed position in the bottom-right corner -->
  <div class="fab">
    <!-- Main FAB button -->
    <!-- tabindex="0" makes it focusable, role="button" is for accessibility -->
    <div tabindex="0" role="button" class="btn btn-lg btn-circle btn-primary">
      <font-awesome-icon icon="globe" />
    </div>

    <!-- Buttons that appear when FAB is open -->
    <button
      v-for="language in languages"
      :key="language.code"
      class="btn btn-secondary btn-lg btn-circle"
      @click="changeLocale(language.code)"
    >
      {{ language.label }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'LanguageSelector', // Component name

  data() {
    return {
      // List of available languages
      languages: [
        { code: 'ru', label: 'RU' },
        { code: 'lv', label: 'LV' },
        { code: 'en', label: 'EN' },
      ],
    }
  },

  methods: {
    // Function to change the current locale
    changeLocale(code) {
      // Access the global i18n instance via this.$i18n
      this.$i18n.locale = code
    },
  },
}
</script>


<style scoped>
/* Styling is handled via Tailwind CSS, no extra CSS needed */
</style>
