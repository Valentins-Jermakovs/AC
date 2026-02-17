<template>
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.modify_user.new_password_title')"
    :confirm-text="$t('common.confirm')"
    :cancel-text="$t('common.cancel')"
    @confirm="submit"
  >
    <div class="flex flex-col w-full gap-5">
      <Transition name="error-slide">
        <div v-if="error">
          <h1 class="text-error mb-2">{{ error }}</h1>
        </div>
      </Transition>

      <p class="opacity-50">* {{ $t('common.if_google') }}</p>

      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.old_password') }}</span>
        </label>
        <input
          v-model="oldPassword"
          type="password"
          class="input input-bordered w-full"
        />
      </div>

      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.new_password') }}</span>
        </label>
        <input
          v-model="newPassword"
          type="password"
          class="input input-bordered w-full"
        />
      </div>
    </div>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'PasswordChangeModal',
  components: { BaseDialog },

  props: {
    modelValue: Boolean,
    error: String,
  },

  emits: ['update:modelValue', 'submit'],

  data() {
    return {
      oldPassword: '',
      newPassword: '',
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
      this.$emit('submit', {
        oldPassword: this.oldPassword,
        newPassword: this.newPassword,
      })
      this.oldPassword = ''
      this.newPassword = ''
    },
  },
}
</script>

<style scoped></style>