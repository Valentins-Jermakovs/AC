<template>
  <!-- OUTER SCROLL CONTAINER -->
  <div
    class="w-full h-16 bg-base-200 border-y border-base-300 overflow-x-auto overflow-y-hidden relative"
    style="-webkit-overflow-scrolling: touch"
  >
    <!-- INNER FLEX ROW FOR BUTTONS -->
    <div class="flex flex-nowrap h-full min-w-max px-2 md:px-0 md:pl-20">
      <!-- Render each button -->
      <button
        v-for="(item, index) in buttons"
        :key="index"
        @click="setActive(item.key)"
        :class="[
          'h-full px-6 border-t-4 whitespace-nowrap transition-colors',
          // Active button styles
          activeKey === item.key
            ? 'border-primary bg-neutral text-neutral-content'
            // Inactive button styles
            : 'border-transparent bg-base-200 hover:bg-base-300 hover:cursor-pointer',
        ]"
      >
        {{ item.title }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScrollableTabBar',

  props: {
    buttons: {
      type: Array,
      required: true,
      // Example: [{ title: 'Home', key: 'home' }, { title: 'Analytics', key: 'analytics' }]
    },
    modelValue: {
      type: String,
      default: '',
      // Tracks the currently active tab externally
    },
  },

  data() {
    return {
      // Set the active tab, default to first button if modelValue is empty
      activeKey: this.modelValue || (this.buttons.length ? this.buttons[0].key : ''),
    }
  },

  watch: {
    // Update internal activeKey if parent changes modelValue
    modelValue(val) {
      if (val) {
        this.activeKey = val
      }
    },
  },

  methods: {
    // Set a new active tab and emit update to parent
    setActive(key) {
      this.activeKey = key
      this.$emit('update:modelValue', key)
    },
  },
}
</script>

<style scoped></style>
