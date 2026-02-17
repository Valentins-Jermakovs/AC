<template>
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.logout.title')"
    :confirm-text="$t('common.confirm')"
    :cancel-text="$t('common.cancel')"
    @confirm="confirmLogout"
  >
    {{ $t('modals.logout.content') }}
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'LogoutModal',
  components: { BaseDialog },

  props: {
    modelValue: Boolean,
  },

  emits: ['update:modelValue', 'confirm'],

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
    confirmLogout() {
      this.$emit('confirm')
      this.localModel = false
    },
  },
}
</script>
