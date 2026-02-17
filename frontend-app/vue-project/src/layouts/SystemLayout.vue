<template>
  <div class="flex flex-col h-full">
    <!-- Top navigation bar -->
    <div class="w-full">
      <TopBar></TopBar>
    </div>

    <!-- Main content area -->
    <div class="flex-1 flex h-0">
      <!-- Sidebar navigation -->
      <Sidebar></Sidebar>

      <!-- Scrollable area for child pages rendered by router -->
      <div class="flex-1 bg-base-100 overflow-auto">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/ui/sidebar/Sidebar.vue'
import TopBar from '@/components/ui/topbar/TopBar.vue';

export default {
  name: 'SystemLayout',
  components: {
    TopBar, // Top navigation bar
    Sidebar, // Sidebar navigation menu
  },
}
</script>

<style scoped>
/* No custom styles, all layout handled by Tailwind CSS */
</style>
