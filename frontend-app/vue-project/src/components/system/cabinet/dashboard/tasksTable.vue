<template>
  <div class="bg-base-200 border border-base-300">
    <!-- Header -->
    <div class="p-5 border-b border-base-300 flex items-center gap-2">
      <h1 class="text-xl font-semibold">{{ $t('cabinet.profile.kpi.month_tasks') }}</h1>

      <!-- Loader -->
      <font-awesome-icon v-if="loading" icon="fa-solid fa-spinner" class="animate-spin text-base-content/60 ml-2" />
    </div>

    <!-- CONTENT -->
    <div v-if="loading" class="p-5 flex justify-center">
      <p class="text-base-content/60 italic flex items-center gap-2">
        <font-awesome-icon icon="fa-solid fa-hourglass-half" />
      </p>
    </div>

    <div v-else>
      <!-- NO TASKS -->
      <div v-if="privateTasksStore.privateTasks.length === 0" class="p-10 text-center flex flex-col items-center gap-3">
        <font-awesome-icon icon="fa-solid fa-calendar-xmark" class="text-5xl text-base-content/40" />
        <p class="text-base-content/60 italic">
          {{ $t('cabinet.profile.kpi.no_tasks') }}
        </p>
      </div>

      <!-- TASKS -->
      <div v-else>
        <!-- DESKTOP TABLE -->
        <div class="hidden md:block overflow-x-auto">
          <table class="table w-full">
            <thead class="bg-base-300">
              <tr>
                <th>{{ $t('widgets.month_tasks.table.title') }}</th>
                <th>{{ $t('widgets.month_tasks.table.description') }}</th>
                <th>{{ $t('widgets.month_tasks.table.created') }}</th>
                <th>{{ $t('widgets.month_tasks.table.due_date') }}</th>
                <th>{{ $t('widgets.month_tasks.table.status') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in privateTasksStore.privateTasks" :key="task.id" class="hover">
                <td class="font-medium">{{ task.title }}</td>
                <td class="max-w-xs truncate">{{ task.description }}</td>
                <td>{{ task.createdAt }}</td>
                <td>{{ task.dueDate }}</td>
                <td>
                  <div class="badge" :class="task.completed ? 'badge-success' : 'badge-warning'">
                    {{ task.completed ? $t('widgets.month_tasks.status.complete') :
                      $t('widgets.month_tasks.status.pending') }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- MOBILE CARDS -->
        <div class="flex flex-col gap-3 md:hidden p-4">
          <div v-for="task in privateTasksStore.privateTasks" :key="task.id"
            class="bg-base-100 border border-base-300 p-4 rounded-box flex flex-col gap-2">
            <div class="flex justify-between">
              <h2 class="font-semibold">{{ task.title }}</h2>
              <div class="badge" :class="task.completed ? 'badge-success' : 'badge-warning'">
                {{ task.completed ? $t('widgets.month_tasks.status.complete') : $t('widgets.month_tasks.status.pending') }}
              </div>
            </div>
            <p class="text-sm opacity-70">{{ task.description }}</p>
          </div>
        </div>
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
      loading: true,
    }
  },

  async mounted() {
    this.privateTasksStore.meta.page = 1
    this.privateTasksStore.meta.limit = 10
    const currentMonth = new Date().getMonth() + 1
    this.privateTasksStore.searchQuery = currentMonth

    this.loading = true
    await this.privateTasksStore.findPrivateTasksByMonth()
    this.loading = false
  },
}
</script>