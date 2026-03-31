<template>
  <div
    class="w-full flex flex-col gap-2 flex-1 bg-base-100 overflow-y-scroll border border-base-300 p-2"
  >
    <TaskItem
      v-if="tasks.length > 0"
      v-for="task in tasks"
      :key="task.id || task.title"
      :task="task"
      :selectedTask="selectedTask"
      @select="onSelectTask"
    />
    <!-- Empty state -->
    <div v-else class="flex flex-col items-center justify-center flex-1 gap-4 text-base-content/60">
      <!-- Icon -->
      <font-awesome-icon icon="fa-solid fa-list-check" class="text-5xl text-base-content/30" />

      <!-- Text -->
      <p class="text-lg font-medium">
        {{ $t('work.errors.task_not_found') }}
      </p>

      <!-- Animated progress -->
      <progress class="progress progress-primary w-40"></progress>

      <!-- Small hint -->
      <p class="text-sm text-base-content/40">
        {{ $t('work.errors.not_found_description') }}
      </p>
    </div>
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
