<template>
<BaseDialog
  :modelValue="localModel"
  :title="$t('modals.email.title')"
  :cancel-text="$t('common.cancel')"
  @confirm="submitEmailForm"
>
    <!-- Forma bez pogas -->
    <form
      ref="emailForm"
      action="https://api.web3forms.com/submit"
      method="POST"
      class="flex flex-col flex-1 gap-4"
    >
      <!-- Access Key -->
      <input type="hidden" name="access_key" value="f5c7a756-f35d-487b-b41c-d15805c7fec7" />
      <input type="hidden" name="redirect" value="http://localhost:5173/email-redirect" />

      <!-- Name -->
      <div class="form-control flex flex-col gap-1">
        <label for="name" class="label">
          <span class="label-text">{{ $t('modals.email.form_username') }}</span>
        </label>
        <input id="name" name="name" type="text" required
          :placeholder="$t('modals.email.username_placeholder')"
          class="input input-bordered w-full" />
      </div>

      <!-- Email + Phone -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div class="form-control flex flex-col gap-1">
          <label for="email" class="label">
            <span class="label-text">{{ $t('modals.email.form_email') }}</span>
          </label>
          <input id="email" name="email" type="email" required maxlength="254"
            :placeholder="$t('modals.email.email_placeholder')"
            class="input input-bordered w-full" />
        </div>

        <div class="form-control flex flex-col gap-1">
          <label for="phone" class="label">
            <span class="label-text">{{ $t('modals.email.form_phone') }}</span>
          </label>
          <input id="phone" name="phone" type="tel" required minlength="10" maxlength="15"
            :placeholder="$t('modals.email.phone_placeholder')"
            class="input input-bordered w-full" />
        </div>
      </div>

      <!-- Subject -->
      <div class="form-control flex flex-col gap-1">
        <label for="subject" class="label">
          <span class="label-text">{{ $t('modals.email.form_title') }}</span>
        </label>
        <input id="subject" name="subject" type="text" maxlength="78" required
          :placeholder="$t('modals.email.title_placeholder')"
          class="input input-bordered w-full" />
      </div>

      <!-- Counter ABOVE textarea -->
      <div class="w-full flex justify-end text-sm opacity-70 pr-1">
        {{ remainingChars }} / {{ maxLength }}
      </div>

      <!-- Message -->
      <div class="form-control flex flex-col gap-1">
        <label for="message" class="label">
          <span class="label-text">{{ $t('modals.email.form_content') }}</span>
        </label>
        <textarea id="message" name="message" v-model="message" :maxlength="maxLength" required
          :placeholder="$t('modals.email.content_placeholder')"
          class="textarea textarea-bordered w-full resize-none h-56"></textarea>
      </div>
    </form>

    <!-- Actions slot (pogas) -->
    <template #actions>
      <button class="btn btn-primary" @click="submitEmailForm">
        {{ $t('common.confirm') }}
      </button>
      <button class="btn btn-neutral" @click="$emit('update:modelValue', false)">
        {{ $t('common.cancel') }}
      </button>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from './BaseDialog.vue'

export default {
  name: 'EmailModal',
  components: { BaseDialog },
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      message: '',
      maxLength: 2000
    }
  },
  computed: {
    remainingChars() {
      return this.maxLength - this.message.length
    },
    localModel: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  methods: {
    submitEmailForm() {
      const form = this.$refs.emailForm
      if (form.checkValidity()) {
        form.submit()
        this.localModel = false // aizver dialogu caur setter
      } else {
        form.reportValidity()
      }
    }
  }
}

</script>

<style scoped></style>
