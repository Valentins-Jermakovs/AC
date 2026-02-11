<template>
  <!-- burger -->
  <button
    class="btn-square border-0 btn-neutral btn"
    @click="toggleSideBar"
    :class="isSideBarOpen ? ' hover:btn-primary' : 'btn-primary'"
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
