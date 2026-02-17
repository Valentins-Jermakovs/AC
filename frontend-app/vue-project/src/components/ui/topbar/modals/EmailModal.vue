<template>
  <!-- Modal wrapper using BaseDialog -->
  <BaseDialog
    :modelValue="localModel"
    :title="$t('modals.email.title')"
    :cancel-text="$t('common.cancel')"
    @confirm="submitEmailForm"
  >
    <!-- Email form without its own submit button -->
    <form
      ref="emailForm"
      action="https://api.web3forms.com/submit"
      method="POST"
      class="flex flex-col flex-1 gap-4"
    >
      <!-- Hidden inputs for Web3Forms -->
      <input type="hidden" name="access_key" value="f5c7a756-f35d-487b-b41c-d15805c7fec7" />
      <input type="hidden" name="redirect" value="http://localhost:5173/email-redirect" />

      <!-- Name field -->
      <div class="form-control flex flex-col gap-1">
        <label for="name" class="label">
          <span class="label-text">{{ $t('modals.email.form_username') }}</span>
        </label>
        <input
          id="name"
          name="name"
          type="text"
          required
          :placeholder="$t('modals.email.username_placeholder')"
          class="input input-bordered w-full"
        />
      </div>

      <!-- Email and Phone fields side by side -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <!-- Email -->
        <div class="form-control flex flex-col gap-1">
          <label for="email" class="label">
            <span class="label-text">{{ $t('modals.email.form_email') }}</span>
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            maxlength="254"
            :placeholder="$t('modals.email.email_placeholder')"
            class="input input-bordered w-full"
          />
        </div>

        <!-- Phone -->
        <div class="form-control flex flex-col gap-1">
          <label for="phone" class="label">
            <span class="label-text">{{ $t('modals.email.form_phone') }}</span>
          </label>
          <input
            id="phone"
            name="phone"
            type="tel"
            required
            minlength="10"
            maxlength="15"
            :placeholder="$t('modals.email.phone_placeholder')"
            class="input input-bordered w-full"
          />
        </div>
      </div>

      <!-- Subject field -->
      <div class="form-control flex flex-col gap-1">
        <label for="subject" class="label">
          <span class="label-text">{{ $t('modals.email.form_title') }}</span>
        </label>
        <input
          id="subject"
          name="subject"
          type="text"
          maxlength="78"
          required
          :placeholder="$t('modals.email.title_placeholder')"
          class="input input-bordered w-full"
        />
      </div>

      <!-- Character counter for message -->
      <div class="w-full flex justify-end text-sm opacity-70 pr-1">
        {{ remainingChars }} / {{ maxLength }}
      </div>

      <!-- Message textarea -->
      <div class="form-control flex flex-col gap-1">
        <label for="message" class="label">
          <span class="label-text">{{ $t('modals.email.form_content') }}</span>
        </label>
        <textarea
          id="message"
          name="message"
          v-model="message"
          :maxlength="maxLength"
          required
          :placeholder="$t('modals.email.content_placeholder')"
          class="textarea textarea-bordered w-full resize-none h-56"
        ></textarea>
      </div>
    </form>

    <!-- Actions slot for modal buttons -->
    <template #actions>
      <!-- Confirm button triggers form submit -->
      <button class="btn btn-primary" @click="submitEmailForm">
        {{ $t('common.confirm') }}
      </button>
      <!-- Cancel button closes modal -->
      <button class="btn btn-neutral" @click="$emit('update:modelValue', false)">
        {{ $t('common.cancel') }}
      </button>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'EmailModal',
  components: { BaseDialog },
  props: {
    // Control visibility of the modal
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      // Two-way bound message content
      message: '',
      // Maximum allowed characters in the message
      maxLength: 2000,
    }
  },
  computed: {
    // Remaining characters for the textarea
    remainingChars() {
      return this.maxLength - this.message.length
    },
    // Local computed property to simplify v-model handling
    localModel: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      },
    },
  },
  methods: {
    // Submit the form programmatically
    submitEmailForm() {
      const form = this.$refs.emailForm
      if (form.checkValidity()) {
        form.submit() // submit form to Web3Forms
        this.localModel = false // close the modal
      } else {
        form.reportValidity() // show validation errors
      }
    },
  },
}
</script>

<style scoped></style>
