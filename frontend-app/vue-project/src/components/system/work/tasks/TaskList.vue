<template>
  <div
    class="w-full flex flex-col gap-2 flex-1 bg-base-100 overflow-y-scroll rounded-box border border-base-300 p-2"
  >
    <TaskItem
      v-for="task in tasks"
      :key="task.id || task.title"
      :task="task"
      :selectedTask="selectedTask"
      @select="onSelectTask"
    />
  </div>
</template>

<script>
import TaskItem from './TaskItem.vue'

export default {
  name: 'TaskList',
  components: {
    TaskItem,
  },
  props: {
    tasks: {
      type: Array,
      required: true,
    },
    selectedTask: {
      type: Object,
      default: null,
    },
  },
  methods: {
    onSelectTask(task) {
      this.$emit('select-task', task)
    },
  },
}
</script>
