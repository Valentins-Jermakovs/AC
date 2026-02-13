<template>
  <div
    class="flex w-full h-full bg-base-200 items-center justify-between py-2 pr-2 pl-1 border border-base-300"
  >
    <!-- LEFT: burger + logo -->
    <div class="flex items-center gap-4 pl-1">
      <burger-button></burger-button>
      <logo></logo>
    </div>

    <!-- Date & Time -->
    <div class="hidden lg:flex gap-3 rounded-field bg-base-200 font-semibold">
      <h1>{{ date }}</h1>
      <h1>{{ time }}</h1>
    </div>

    <!-- RIGHT: buttons -->
    <div class="flex">
      <top-button
        v-for="(item, index) in navigation"
        :key="index"
        :icon="item.icon"
        @click="item.modal && openModal(item.modal)"
      ></top-button>
    </div>

    <!-- Email Modal -->
    <EmailModal v-model="emailModal"></EmailModal>

    <!-- Language Modal -->
    <BaseDialog
      v-model="languageModal"
      :title="$t('modals.languages.title')"
      :cancel-text="$t('common.cancel')"
    >
      <div class="w-full flex-col flex">
        <button
          class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500 mb-2"
          @click="changeLocale('en')"
        >
          {{ $t('modals.languages.english') }}
        </button>
        <button
          class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500 mb-2"
          @click="changeLocale('lv')"
        >
          {{ $t('modals.languages.latvian') }}
        </button>
        <button
          class="btn btn-neutral hover:btn-secondary btn-md w-full transition-all duration-500"
          @click="changeLocale('ru')"
        >
          {{ $t('modals.languages.russian') }}
        </button>
      </div>
    </BaseDialog>

    <!-- Support Modal -->
    <BaseDialog
      v-model="supportModal"
      :title="$t('common.support')"
      :cancel-text="$t('common.cancel')"
    >
      <div class="flex flex-col gap-2 w-full">
        <button
          v-for="(doc, index) in documents"
          :key="index"
          @click="openDocument(doc.link)"
          class="flex-1 flex flex-col btn btn-neutral p-5 hover:btn-secondary transition-all duration-500"
        >
          {{ doc.title }}
        </button>
      </div>
    </BaseDialog>

    <!-- Logout Modal -->
    <BaseDialog
      v-model="logoutModal"
      :title="$t('modals.logout.title')"
      :confirm-text="$t('common.confirm')"
      :cancel-text="$t('common.cancel')"
      @confirm="handleLogout"
    >
      {{ $t('modals.logout.content') }}
    </BaseDialog>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

import BurgerButton from './BurgerButton.vue'
import Logo from './ProjectLogo.vue'
import TopButton from './TopButton.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'
import ContactForm from '@/components/common/ContactForm.vue'
import EmailModal from '@/components/common/EmailModal.vue'

export default {
  name: 'TopBar',
  components: {
    BurgerButton,
    Logo,
    TopButton,
    BaseDialog,
    ContactForm,
    EmailModal,
  },
  data() {
    return {
      // Modals
      emailModal: false,
      languageModal: false,
      supportModal: false,
      logoutModal: false,

      // Date & Time
      date: new Date().toLocaleDateString(),
      time: '',

      // Navigation buttons
      navigation: [
        { icon: 'fa-solid fa-envelope', modal: 'email' },
        { icon: 'fa-solid fa-globe', modal: 'language' },
        { icon: 'fa-solid fa-question-circle', modal: 'support' },
        { icon: 'fa-solid fa-circle-xmark', modal: 'logout' },
      ],

      // Documents for support
      documents: [
        { link: 'http://localhost:5173/documents/user_manual.pdf', title: 'User Manual' },
        { link: 'http://localhost:5173/documents/license.pdf', title: 'License' },
        { link: 'http://localhost:5173/documents/policy.pdf', title: 'Privacy Policy' },
      ],

      // Timer ID
      timerId: null,
    }
  },
  setup() {
    const { locale } = useI18n({ useScope: 'global' })
    const router = useRouter()
    const authStore = useAuthStore()
    return { locale, router, authStore }
  },
  methods: {
    openModal(modalName) {
      if (modalName === 'email') this.emailModal = true
      else if (modalName === 'language') this.languageModal = true
      else if (modalName === 'support') this.supportModal = true
      else if (modalName === 'logout') this.logoutModal = true
    },
    openDocument(link) {
      window.open(link, '_blank')
    },
    async handleLogout() {
      try {
        await this.authStore.logout()

        const userStore = useUserStore()
        const authStore = useAuthStore()

        userStore.$reset()
        authStore.$reset()
      } finally {
        this.logoutModal = false
        this.router.push({ name: 'logout' })
      }
    },
    changeLocale(code) {
      this.$i18n.locale = code
      this.languageModal = false
    },
    updateTime() {
      this.time = new Date().toLocaleTimeString().slice(0, -3) // Remove seconds
    },
  },
  mounted() {
    this.updateTime() // initial time
    this.timerId = setInterval(() => {
      this.updateTime()
    }, 1000)
  },
  beforeUnmount() {
    if (this.timerId) clearInterval(this.timerId)
  },
}
</script>

<style scoped></style>
