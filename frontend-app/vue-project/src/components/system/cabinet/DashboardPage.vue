<template>
  <div class="flex flex-col p-5 w-full h-full">
    <TasksTable></TasksTable>
  </div>
</template>

<script>
import TasksTable from './dashboard/tasksTable.vue'

export default {
  name: 'DashboardPage',
  components: {
    TasksTable,
  },
}
</script>

<style scoped></style>
