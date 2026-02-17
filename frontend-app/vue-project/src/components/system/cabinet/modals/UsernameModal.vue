<template>
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.modify_user.new_username_title')"
    :confirm-text="$t('common.confirm')"
    :cancel-text="$t('common.cancel')"
    @confirm="submit"
  >
    <div class="flex flex-col w-full gap-5">
      <!-- Error message -->
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
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'UsernameModal',
  components: { BaseDialog },

  props: {
    modelValue: Boolean,
    error: String,
  },

  emits: ['update:modelValue', 'submit'],

  data() {
    return {
      username: '',
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
    submit() {
      if (!this.username) return
      this.$emit('submit', this.username)
      this.username = ''
    },
  },
}
</script>

<style scoped></style>