<template>
  <!-- Sidebar link button with icon and optional label -->
  <router-link
    :to="{ name: toName }"
    class="w-full btn h-12 font-bold md:w-12 md:h-12 md:tooltip md:tooltip-right flex items-center justify-center transform transition-all duration-500"
    :data-tip="t(titleKey)"
    :class="[
      isActive ? 'btn-primary' : 'btn-neutral hover:btn-secondary transition-all duration-300',
      isSideBarOpen ? 'opacity-100 left-0' : 'opacity-0 pointer-events-none -left-15',
    ]"
    @click="handleClick"
  >
    <!-- Icon for the sidebar link -->
    <font-awesome-icon :icon="icon" />

    <!-- Label: visible only on mobile -->
    <h2 class="inline md:hidden font-bold ml-2">{{ t(titleKey) }}</h2>
  </router-link>
</template>

<script>
// Import Vue features and composables
import { useRoute } from 'vue-router'
import { useSideBar } from '@/composables/useSideBar'
import { useI18n } from 'vue-i18n'

export default {
  name: 'SidebarLink',

  props: {
    titleKey: {
      type: String,
      required: true, // Translation key for link title
    },
    icon: String,      // Font Awesome icon
    toName: String,    // Vue Router route name
  },

  data() {
    // Initialize composables inside data() for classic Options API
    const { t } = useI18n()
    const currentRoute = useRoute()
    const { isSideBarOpen, toggleSideBar } = useSideBar()

    return {
      t,
      currentRoute,
      isSideBarOpen,
      toggleSideBar,
    }
  },

  computed: {
    // Check if this route is active
    isActive() {
      return this.currentRoute.matched.some(
        (route) => route.name === this.toName
      )
    },
  },

  methods: {
    // Handle click: toggle sidebar on mobile
    handleClick() {
      if (window.innerWidth < 768) {
        this.toggleSideBar()
      }
    },
  },
}
</script>

<style scoped>
/* Scoped styles for SidebarLink (currently empty) */
</style>
