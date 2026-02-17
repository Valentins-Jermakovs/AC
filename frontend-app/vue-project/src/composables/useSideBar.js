import { ref } from 'vue'

// Reactive variable to track if the sidebar is open or closed
const isSideBarOpen = ref(true)

// Function to toggle sidebar state
const toggleSideBar = () => {
  isSideBarOpen.value = !isSideBarOpen.value
}

// Composable function to use sidebar state and toggle function
export function useSideBar() {
  return { isSideBarOpen, toggleSideBar }
}
