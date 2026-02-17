<template>
  <div class="flex w-full h-full bg-base-200 items-center justify-between py-2 pr-2 pl-1 border border-base-300">
    
    <!-- LEFT -->
    <div class="flex items-center gap-4 pl-1">
      <BurgerButton />
      <Logo />
    </div>

    <!-- Date & Time -->
    <div class="hidden lg:flex gap-3 rounded-field bg-base-200 font-semibold">
      <h1>{{ date }}</h1>
      <h1>{{ time }}</h1>
    </div>

    <!-- RIGHT -->
    <div class="flex">
      <TopButton
        v-for="(item, index) in navigation"
        :key="index"
        :icon="item.icon"
        @click="openModal(item.modal)"
      />
    </div>

    <!-- MODALS -->

    <EmailModal
      :modelValue="activeModal === 'email'"
      @update:modelValue="activeModal = null"
    />

    <LanguageModal
      :modelValue="activeModal === 'language'"
      @update:modelValue="activeModal = null"
    />

    <SupportModal
      :modelValue="activeModal === 'support'"
      @update:modelValue="activeModal = null"
    />

    <LogoutModal
      :modelValue="activeModal === 'logout'"
      @update:modelValue="activeModal = null"
      @confirm="handleLogout"
    />

  </div>
</template>


<script>
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useAdminStore } from '@/stores/admin'

import BurgerButton from './BurgerButton.vue'
import Logo from './ProjectLogo.vue'
import TopButton from './TopButton.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'


import EmailModal from './modals/EmailModal.vue'
import LanguageModal from './modals/LanguageModal.vue'
import SupportModal from './modals/SupportModal.vue'
import LogoutModal from './modals/LogoutModal.vue'

export default {
  name: 'TopBar',
  components: {
    BurgerButton,
    Logo,
    TopButton,
    BaseDialog,
    EmailModal,
    LanguageModal,
    SupportModal,
    LogoutModal
  },
  data() {
    return {
      activeModal: null,

      date: new Date().toLocaleDateString(),
      time: '',

      navigation: [
        { icon: 'fa-solid fa-envelope', modal: 'email' },
        { icon: 'fa-solid fa-globe', modal: 'language' },
        { icon: 'fa-solid fa-question-circle', modal: 'support' },
        { icon: 'fa-solid fa-circle-xmark', modal: 'logout' },
      ],

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
      this.activeModal = modalName
    },

    async handleLogout() {
      try {
        await this.authStore.logout()

        const userStore = useUserStore()
        const authStore = useAuthStore()
        const adminStore = useAdminStore()

        userStore.$reset()
        authStore.$reset()
        adminStore.$reset()
      } finally {
        this.activeModal = null
        this.router.push({ name: 'logout' })
      }
    },

    updateTime() {
      this.time = new Date().toLocaleTimeString().slice(0, -3)
    },
  },

  mounted() {
    this.updateTime()
    this.timerId = setInterval(this.updateTime, 1000)
  },

  beforeUnmount() {
    if (this.timerId) clearInterval(this.timerId)
  },
}
</script>

<style scoped></style>
