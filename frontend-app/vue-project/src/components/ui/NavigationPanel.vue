<template>
  <!-- OUTER SCROLL CONTAINER -->
  <div
    class="w-full h-16 bg-base-200 border-y border-base-300 overflow-x-auto overflow-y-hidden relative"
    style="-webkit-overflow-scrolling: touch"
  >
    <!-- INNER FLEX ROW -->
    <div class="flex flex-nowrap h-full min-w-max px-2 md:px-0 md:pl-20">
      <button
        v-for="(item, index) in buttons"
        :key="index"
        @click="setActive(item.key)"
        :class="[
          'h-full px-6 border-t-4 whitespace-nowrap transition-colors',
          activeKey === item.key
            ? 'border-primary bg-neutral text-neutral-content'
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
  props: {
    buttons: {
      type: Array,
      required: true,
      // Sample: [{ title: 'Home', key: 'home' }, { title: 'Analytics', key: 'analytics' }]
    },
    modelValue: {
      type: String,
      default: '',
    },
  },

  data() {
    return {
      activeKey: this.modelValue || (this.buttons.length ? this.buttons[0].key : ''),
    }
  },

  watch: {
    modelValue(val) {
      if (val) {
        this.activeKey = val
      }
    },
  },

  methods: {
    setActive(key) {
      this.activeKey = key
      this.$emit('update:modelValue', key)
    },
  },
}
</script>

<style scoped></style>
