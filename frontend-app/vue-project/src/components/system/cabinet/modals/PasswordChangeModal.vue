<template>
  <!-- Modal dialog for changing user password -->
  <BaseDialog v-model="localModel" :title="$t('modals.modify_user.new_password_title')"
    :confirm-text="$t('common.confirm')" :cancel-text="$t('common.cancel')" @confirm="submit">
    <div class="flex flex-col w-full gap-5">
      <!-- Error message transition -->
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>

      <!-- Info for Google users -->
      <p class="opacity-50">* {{ $t('common.if_google') }}</p>

      <!-- Old password input -->
      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.old_password') }}</span>
        </label>
        <input v-model="oldPassword" type="password" class="input input-bordered w-full" />
      </div>

      <!-- New password input -->
      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.new_password') }}</span>
        </label>
        <input v-model="newPassword" type="password" class="input input-bordered w-full" />
      </div>
    </div>
  </BaseDialog>
</template>

<script>
// Import base modal dialog component
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'PasswordChangeModal', // Component name

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
      oldPassword: '',  // Local input for old password
      newPassword: '',  // Local input for new password
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
    // Submit passwords to parent
    submit() {
      this.$emit('submit', {
        oldPassword: this.oldPassword,
        newPassword: this.newPassword,
      })
      // Clear inputs after submit
      this.oldPassword = ''
      this.newPassword = ''
    },
  },
}
</script>

<style scoped>
/* Transition animation for error message */
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
