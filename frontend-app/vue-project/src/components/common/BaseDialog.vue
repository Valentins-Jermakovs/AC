<template>
  <dialog class="modal" :open="modelValue">
    <div class="modal-box flex flex-col gap-3">
      <!-- Title -->
      <h3 v-if="title" class="text-lg font-bold text-start">
        {{ title }}
      </h3>
      <!-- Content -->
      <div class="modal-content flex justify-start">
        <slot></slot>
      </div>
      <!-- Actions -->
      <div class="modal-action">
        <slot name="actions">
          <!-- default buttons -->
          <button v-if="confirmText" class="btn btn-primary" @click="confirm">
            {{ confirmText }}
          </button>
          <button v-if="cancelText" class="btn btn-neutral" @click="close">
            {{ cancelText }}
          </button>
        </slot>
      </div>
    </div>
  </dialog>
</template>

<script>
export default {
  name: 'ModalDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    confirmText: {
      type: String,
      default: ''
    },
    cancelText: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'confirm', 'cancel'],
  methods: {
    close() {
      this.$emit('update:modelValue', false)
      this.$emit('cancel')
    },
    confirm() {
      this.$emit('confirm')
    }
  }
}
</script>

<style scoped></style>
