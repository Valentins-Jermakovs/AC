<template>
  <div class="bg-base-200 border border-base-300 rounded-box">
    <!-- Header -->
    <div class="p-5 border-b border-base-300">
      <h1 class="text-xl font-semibold">Šī mēneša uzdevumi</h1>
    </div>

    <!-- Desktop table -->
    <div class="hidden md:block overflow-x-auto">
      <table class="table w-full">
        <thead class="bg-base-300">
          <tr>
            <th>Title</th>
            <th>Description</th>
            <th>Created</th>
            <th>Due date</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="task in privateTasksStore.privateTasks" :key="task.id" class="hover">
            <td class="font-medium">
              {{ task.title }}
            </td>

            <td class="max-w-xs truncate">
              {{ task.description }}
            </td>

            <td>
              {{ task.createdAt }}
            </td>

            <td>
              {{ task.dueDate }}
            </td>

            <td>
              <div class="badge" :class="task.completed ? 'badge-success' : 'badge-warning'">
                {{ task.completed ? 'Completed' : 'Active' }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile -->
    <div class="flex flex-col gap-3 md:hidden p-4">
      <div
        v-for="task in privateTasksStore.privateTasks"
        :key="task.id"
        class="bg-base-100 border border-base-300 p-4 rounded-box flex flex-col gap-2"
      >
        <div class="flex justify-between">
          <h2 class="font-semibold">
            {{ task.title }}
          </h2>

          <div class="badge" :class="task.completed ? 'badge-success' : 'badge-warning'">
            {{ task.completed ? 'Done' : 'Active' }}
          </div>
        </div>

        <p class="text-sm opacity-70">
          {{ task.description }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { usePrivateTasksStore } from '@/stores/privateTasks'

export default {
  data() {
    return {
      privateTasksStore: usePrivateTasksStore(),
    }
  },

  async mounted() {
    this.privateTasksStore.meta.page = 1
    this.privateTasksStore.meta.limit = 10

    const currentMonth = new Date().getMonth() + 1

    this.privateTasksStore.searchQuery = currentMonth

    await this.privateTasksStore.findPrivateTasksByMonth()
  },
}
</script>
