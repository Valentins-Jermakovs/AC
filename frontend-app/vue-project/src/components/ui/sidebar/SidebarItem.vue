<template>
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
    <font-awesome-icon :icon="icon" />
    <h2 class="inline md:hidden font-bold ml-2">{{ t(titleKey) }}</h2>
  </router-link>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSideBar } from '@/composables/useSideBar'
import { useI18n } from 'vue-i18n'

export default {
  name: 'SidebarLink',
  props: {
    titleKey: {
      type: String,
      required: true,
    },
    icon: String,
    toName: String,
  },
  setup(props) {
    const { t } = useI18n()
    const currentRoute = useRoute()
    const { isSideBarOpen, toggleSideBar } = useSideBar()

    const isActive = computed(() =>
      currentRoute.matched.some((route) => route.name === props.toName),
    )

    const handleClick = () => {
      if (window.innerWidth < 768) {
        toggleSideBar()
      }
    }

    return {
      t,
      isSideBarOpen,
      isActive,
      handleClick,
    }
  },
}
</script>

<style scoped></style>
