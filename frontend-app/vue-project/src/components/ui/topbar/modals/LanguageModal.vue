<template>
  <!-- Modal dialog for selecting language -->
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.languages.title')"
    :cancel-text="$t('common.cancel')"
  >
    <div class="w-full flex flex-col">
      <!-- Button to switch to English -->
      <button
        class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500 mb-2"
        @click="changeLocale('en')"
      >
        {{ $t('modals.languages.english') }}
      </button>

      <!-- Button to switch to Latvian -->
      <button
        class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500 mb-2"
        @click="changeLocale('lv')"
      >
        {{ $t('modals.languages.latvian') }}
      </button>

      <!-- Button to switch to Russian -->
      <button
        class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500"
        @click="changeLocale('ru')"
      >
        {{ $t('modals.languages.russian') }}
      </button>
    </div>
  </BaseDialog>
</template>

<script>
// Import base modal dialog component
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'LanguageModal', // Component name

  components: { BaseDialog },

  // Props: receive v-model value from parent
  props: {
    modelValue: Boolean,
  },

  // Emit event when v-model changes
  emits: ['update:modelValue'],

  computed: {
    // Local proxy for v-model
    localModel: {
      get() {
        return this.modelValue
      },
      set(val) {
        this.$emit('update:modelValue', val)
      },
    },
  },

  methods: {
    // Change app language and close modal
    changeLocale(code) {
      this.$i18n.locale = code
      this.localModel = false
    },
  },
}
</script>

<style scoped>
/* Scoped styles for this component (currently empty) */
</style>
