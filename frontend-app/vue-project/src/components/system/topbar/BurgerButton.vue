<template>
  <!-- burger -->
  <button
    class="w-12 h-12 border-0 btn"
    @click="toggleSideBar"
    :class="isSideBarOpen ? 'btn-neutral' : 'btn-primary'"
  >
    <font-awesome-icon icon="bars" />
  </button>
</template>

<script>
import { useSideBar } from '@/composables/useSideBar'

export default {
  name: 'BurgerButton',
  setup() {
    const { toggleSideBar, isSideBarOpen } = useSideBar()

    return {
      toggleSideBar,
      isSideBarOpen,
    }
  },
}
</script>

<style scoped></style>
