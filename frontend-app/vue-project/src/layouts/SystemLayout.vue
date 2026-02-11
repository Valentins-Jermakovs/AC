<template>
  <div class="flex flex-col h-full">
    <div class="w-full">
      <TopBar></TopBar>
    </div>
    <div class="flex-1 flex h-0">
      <Sidebar></Sidebar>
      <!-- Scrollable child pages -->
      <div class="flex-1 bg-base-100 overflow-auto">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/system/sidebar/Sidebar.vue'
import TopBar from '@/components/system/topbar/TopBar.vue'

export default {
  name: 'SystemLayout',
  components: {
    TopBar,
    Sidebar,
  },
}
</script>

<style scoped></style>
