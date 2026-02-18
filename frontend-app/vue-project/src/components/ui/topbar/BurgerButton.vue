<template>
  <!-- Burger button to open/close sidebar -->
  <button
    class="w-12 h-12 border-0 btn"

    @click="toggleSideBar"

    :class="isSideBarOpen
      ? 'btn-neutral hover:btn-secondary'
      : 'btn-primary'
    "
  >
    <!-- Font Awesome burger icon -->
    <font-awesome-icon icon="bars" />
  </button>
</template>

<script>
// Import composable that controls sidebar state
import { useSideBar } from '@/composables/useSideBar'

export default {
  name: 'BurgerButton',

  setup() {
    // Get sidebar state and toggle function
    const { toggleSideBar, isSideBarOpen } = useSideBar()

    // Return values so they can be used in template
    return {
      toggleSideBar,
      isSideBarOpen,
    }
  },
}
</script>

<style scoped>
/* Scoped styles for this component (currently empty) */
</style>
