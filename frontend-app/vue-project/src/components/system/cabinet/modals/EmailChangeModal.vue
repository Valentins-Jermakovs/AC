<template>
  <!-- Modal dialog for changing user email -->
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.modify_user.new_email_title')"
    :confirm-text="$t('common.confirm')"
    :cancel-text="$t('common.cancel')"
    @confirm="submit"
  >
    <div class="flex flex-col w-full gap-5">
      <!-- Error message transition -->
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>

      <!-- Email input field -->
      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.email') }}</span>
        </label>
        <input
          v-model="email"
          type="email"
          :placeholder="$t('common.new_email')"
          class="input input-bordered w-full"
        />
      </div>
    </div>
  </BaseDialog>
</template>

<script>
// Import base modal dialog component
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'EmailChangeModal', // Component name

  components: { BaseDialog },

  // Props: receive v-model and error message from parent
  props: {
    modelValue: Boolean,
    error: String,
  },

  // Emit events to parent
  emits: ['update:modelValue', 'submit'],

  data() {
    return {
      email: '', // Local email input
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
    // Submit new email to parent
    submit() {
      if (!this.email) return           // Do nothing if empty
      this.$emit('submit', this.email)  // Emit submit event with email
      this.email = ''                   // Clear input after submit
    },
  },
}
</script>

<style scoped>
.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 100px;
}
</style>
