<template>
  <!-- Modal dialog component -->
  <dialog class="modal" :open="modelValue">
    <div class="modal-box flex flex-col gap-3">
      
      <!-- Title section (optional) -->
      <h3 v-if="title" class="text-lg font-bold text-start">
        {{ title }}
      </h3>
      
      <!-- Main content slot -->
      <div class="modal-content flex justify-start">
        <slot></slot>
      </div>
      
      <!-- Actions section -->
      <div class="modal-action">
        <slot name="actions">
          <!-- Default buttons if no custom actions are provided -->
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
    // Controls whether the modal is open
    modelValue: {
      type: Boolean,
      required: true,
    },
    // Optional title text
    title: {
      type: String,
      default: '',
    },
    // Optional text for the confirm button
    confirmText: {
      type: String,
      default: '',
    },
    // Optional text for the cancel button
    cancelText: {
      type: String,
      default: '',
    },
  },
  emits: [
    'update:modelValue', // Emits when modal is closed
    'confirm',           // Emits when confirm button is clicked
    'cancel',            // Emits when cancel button is clicked
  ],
  methods: {
    // Close the modal and emit cancel event
    close() {
      this.$emit('update:modelValue', false)
      this.$emit('cancel')
    },
    // Emit confirm event
    confirm() {
      this.$emit('confirm')
    },
  },
}
</script>

<style scoped></style>
