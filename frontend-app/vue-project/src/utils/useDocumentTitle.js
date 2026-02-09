import { watch } from 'vue'
import { useI18n } from 'vue-i18n'

export function useDocumentTitle() {
  const { t, locale } = useI18n()

  const updateTitle = () => {
    document.title = t('appTitle')
  }

  updateTitle()

  watch(locale, () => {
    updateTitle()
  })
}
