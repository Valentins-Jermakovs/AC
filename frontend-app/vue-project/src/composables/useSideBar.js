import { ref, watch } from 'vue'

// Reactive variable to track if the sidebar is open or closed
const storedState = localStorage.getItem('isSideBarOpen')
const isSideBarOpen = ref(storedState ? JSON.parse(storedState) : false)

// Function to toggle sidebar state
const toggleSideBar = () => {
  isSideBarOpen.value = !isSideBarOpen.value
}

// Watcher to save state to localStorage whenever it changes
watch(isSideBarOpen, (newValue) => {
  localStorage.setItem('isSideBarOpen', JSON.stringify(newValue))
})

export function useSideBar() {
  return { isSideBarOpen, toggleSideBar }
}
