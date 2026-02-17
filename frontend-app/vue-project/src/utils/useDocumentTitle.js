// Import Vue's watch function to react to reactive changes
import { watch } from 'vue'

// Import internationalization composable
import { useI18n } from 'vue-i18n'

// Custom composable function
// This function automatically updates the browser tab title
// when the language (locale) changes
export function useDocumentTitle() {

  // Get translation function (t)
  // and current active locale
  const { t, locale } = useI18n()

  // Function that updates the document title
  const updateTitle = () => {
    // Set browser tab title using translated value
    document.title = t('appTitle')
  }

  // Set title immediately when composable is used
  updateTitle()

  // Watch for language changes
  // When locale changes, update the title again
  watch(locale, () => {
    updateTitle()
  })
}
