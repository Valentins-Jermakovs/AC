<template>
  <BaseDialog
    v-model="localModel"
    :title="$t('common.support')"
    :cancel-text="$t('common.cancel')"
  >
    <div class="flex flex-col gap-2 w-full">
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
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'SupportModal',
  components: { BaseDialog },

  props: {
    modelValue: Boolean,
  },

  emits: ['update:modelValue'],

  data() {
    return {
      documents: [
        { link: 'http://localhost:5173/documents/user_manual.pdf', title: 'User Manual' },
        { link: 'http://localhost:5173/documents/license.pdf', title: 'License' },
        { link: 'http://localhost:5173/documents/policy.pdf', title: 'Privacy Policy' },
      ],
    }
  },

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
    openDocument(link) {
      window.open(link, '_blank')
      this.localModel = false
    },
  },
}
</script>
