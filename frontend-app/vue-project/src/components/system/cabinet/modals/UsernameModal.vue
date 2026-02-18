<template>
  <!-- Modal dialog for changing username -->
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.modify_user.new_username_title')"
    :confirm-text="$t('common.confirm')"
    :cancel-text="$t('common.cancel')"
    @confirm="submit"
  >
    <div class="flex flex-col w-full gap-5">
      <!-- Error message transition -->
      <Transition name="error-slide">
        <div v-if="error" class="overflow-hidden">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>

      <!-- Username input -->
      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.username') }}</span>
        </label>
        <input
          v-model="username"
          type="text"
          :placeholder="$t('common.new_username')"
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
  name: 'UsernameModal', // Component name

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
      username: '', // Local username input
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
    // Submit username to parent
    submit() {
      if (!this.username) return                // Do nothing if empty
      this.$emit('submit', this.username)      // Emit submit event with username
      this.username = ''                        // Clear input after submit
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
