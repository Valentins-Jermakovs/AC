<template>
  <div
    class="w-full h-16 flex items-center p-2 border border-base-300 bg-base-200 hover:bg-base-300 hover:cursor-pointer hover:border-2 hover:border-info rounded-box duration-300 transition-all"
    @click="selectTask"
  >
    <div class="flex flex-col flex-1 px-4">
      <h1 class="font-medium text-md">{{ shortTitle }}</h1>
      <p class="text-xs text-base-content/60">{{ shortDescription }}</p>
    </div>
    <div class="pr-4 text-xs text-info">
      {{ $t('work.task_detail.due_date') }}: {{ task.dueDate }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskListItem',
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
  methods: {
    selectTask() {
      this.$emit('select', this.task)
    },
  },
  computed: {
    shortTitle() {
      if (!this.task.title) return ''
      return this.task.title.length > 20 ? this.task.title.slice(0, 20) + '...' : this.task.title
    },

    shortDescription() {
      if (!this.task.description) return ''
      return this.task.description.length > 30
        ? this.task.description.slice(0, 30) + '...'
        : this.task.description
    },
  },
}
</script>
