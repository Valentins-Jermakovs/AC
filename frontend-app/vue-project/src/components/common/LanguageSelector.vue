<template>
  <!-- Language Selector button -->
  <!-- Fixed position in the bottom-right corner -->
  <div class="fab">
    <!-- a focusable div with tabindex is necessary to work on all browsers. role="button" is necessary for accessibility -->
    <div tabindex="0" role="button" class="btn btn-lg btn-circle btn-primary">
      <font-awesome-icon icon="globe" />
    </div>

    <!-- buttons that show up when FAB is open -->
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
import { useI18n } from 'vue-i18n'

export default {
  setup() {
    const { locale } = useI18n({ useScope: 'global' })

    const languages = [
      { code: 'ru', label: 'RU' },
      { code: 'lv', label: 'LV' },
      { code: 'en', label: 'EN' }
    ]

    const changeLocale = (code) => {
      locale.value = code
    }

    return {
      locale,
      languages,
      changeLocale
    }
  }
}
</script>

<style scoped></style>