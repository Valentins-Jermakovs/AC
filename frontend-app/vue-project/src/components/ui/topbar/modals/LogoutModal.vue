<template>
  <!-- Modal dialog for confirming logout -->
  <BaseDialog
    v-model="localModel"                     
    :title="$t('modals.logout.title')"       
    :confirm-text="$t('common.confirm')"     
    :cancel-text="$t('common.cancel')"       
    @confirm="confirmLogout"                 
  >
    <!-- Modal content / message -->
    {{ $t('modals.logout.content') }}
  </BaseDialog>
</template>

<script>
// Import base modal dialog component
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'LogoutModal', // Component name

  components: { BaseDialog },

  // Props: receive v-model value from parent
  props: {
    modelValue: Boolean,
  },

  // Emits events: update v-model and confirm logout
  emits: ['update:modelValue', 'confirm'],

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
    // Handle user confirming logout
    confirmLogout() {
      this.$emit('confirm')  // Tell parent to logout
      this.localModel = false // Close modal
    },
  },
}
</script>

<style scoped>
/* Scoped styles for this component (currently empty) */
</style>
