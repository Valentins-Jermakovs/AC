<template>
  <!-- Modal dialog for support documents -->
  <BaseDialog
    v-model="localModel"
    :title="$t('common.support')"
    :cancel-text="$t('common.cancel')"
  >
    <div class="flex flex-col gap-2 w-full">
      <!-- List of support documents -->
      <button
        v-for="(doc, index) in documents"
        :key="index"
        @click="openDocument(doc.link)"
        class="flex-1 flex flex-col btn btn-neutral p-5 hover:btn-secondary transition-all duration-500"
      >
        {{ doc.title }}
      </button>
    </div>
  </BaseDialog>
</template>

<script>
// Import base modal dialog component
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'SupportModal', // Component name

  components: { BaseDialog },

  // Props: receive v-model value from parent
  props: {
    modelValue: Boolean,
  },

  // Emit event when v-model changes
  emits: ['update:modelValue'],

  data() {
    return {
      // List of support documents (title + link)
      documents: [
        { link: 'http://localhost:5173/documents/user_manual.pdf', title: 'User Manual' },
        { link: 'http://localhost:5173/documents/license.pdf', title: 'License' },
        { link: 'http://localhost:5173/documents/policy.pdf', title: 'Privacy Policy' },
      ],
    }
  },

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
    // Open document link in a new browser tab and close modal
    openDocument(link) {
      window.open(link, '_blank')
      this.localModel = false
    },
  },
}
</script>

<style scoped>
/* Scoped styles for this component (currently empty) */
</style>
