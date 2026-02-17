<template>
  <BaseDialog
    v-model="localModel"
    :title="$t('modals.modify_user.new_email_title')"
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
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'EmailChangeModal',
  components: { BaseDialog },

  props: {
    modelValue: Boolean,
    error: String,
  },

  emits: ['update:modelValue', 'submit'],

  data() {
    return {
      email: '',
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
      if (!this.email) return
      this.$emit('submit', this.email)
      this.email = ''
    },
  },
}
</script>

<style scoped></style>