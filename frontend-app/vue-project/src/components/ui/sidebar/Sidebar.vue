<template>
  <!-- Sidebar container -->
  <div
    class="h-full bg-base-200 border-base-300 flex transform transition-all duration-500"
    :class="isSideBarOpen
      ? 'w-full md:w-16 border-r'
      : 'w-0 border-0'
    "
  >
    <!-- Menu items -->
    <ul class="menu menu-compact w-full overflow-visible items-center">
      <!-- Render each sidebar item -->
      <SidebarItem
        v-for="(item, index) in menu"
        :key="index"
        :titleKey="item.titleKey"
        :icon="item.icon"
        :toName="item.routeName"
      >
      </SidebarItem>
    </ul>
  </div>
</template>

<script>
// Import composable for sidebar state
import { useSideBar } from '@/composables/useSideBar'

// Import individual sidebar item component
import SidebarItem from './SidebarItem.vue'

export default {
  name: 'Sidebar', // Component name

  components: {
    SidebarItem,
  },

  data() {
    // Sidebar menu and reactive sidebar state
    const { isSideBarOpen } = useSideBar() // Composable for sidebar open/close state

    return {
      // Reactive boolean: sidebar open or closed
      isSideBarOpen,

      // Sidebar menu configuration
      menu: [
        { titleKey: 'sidebar.cabinet', icon: 'fa-solid fa-cube', routeName: 'cabinet' },
        { titleKey: 'sidebar.news', icon: 'fa-solid fa-newspaper', routeName: 'news' },
        { titleKey: 'sidebar.calendar', icon: 'fa-solid fa-calendar', routeName: 'calendar' },
        { titleKey: 'sidebar.work', icon: 'fa-solid fa-check-to-slot', routeName: 'work' },
        { titleKey: 'sidebar.notifications', icon: 'fa-solid fa-bell', routeName: 'notifications' },
        { titleKey: 'sidebar.pomodoro', icon: 'fa-solid fa-clock', routeName: 'pomodoro' },
        { titleKey: 'sidebar.analytics', icon: 'fa-solid fa-chart-pie', routeName: 'data-analyzer' },
      ],
    }
  },
}
</script>

<style scoped>
/* Scoped styles for Sidebar component (currently empty) */
</style>
