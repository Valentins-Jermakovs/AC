<template>
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.languages.title')"
    :cancel-text="$t('common.cancel')"
  >
    <div class="w-full flex flex-col">
      <button
        class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500 mb-2"
        @click="changeLocale('en')"
      >
        {{ $t('modals.languages.english') }}
      </button>

      <button
        class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500 mb-2"
        @click="changeLocale('lv')"
      >
        {{ $t('modals.languages.latvian') }}
      </button>

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
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'LanguageModal',
  components: { BaseDialog },

  props: {
    modelValue: Boolean,
  },

  emits: ['update:modelValue'],

  computed: {
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
    changeLocale(code) {
      this.$i18n.locale = code
      this.localModel = false
    },
  },
}
</script>

<style scoped></style>