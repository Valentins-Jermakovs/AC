<template>
  <div class="flex flex-col p-5 w-full h-full gap-2">
    <!-- KPI cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
      <kpiCard v-for="(item, index) in kpis" :key="index" :title="item.title" :value="item.value" :desc="item.desc"
        :colorClass="item.colorClass">
      </kpiCard>
    </div>
    <!-- Progress cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      <UserProgressCard v-for="(item, index) in progressItems" :key="index" v-bind="item">
      </UserProgressCard>
    </div>
    <TasksTable></TasksTable>
  </div>
</template>

<script>
import TasksTable from './dashboard/tasksTable.vue'
import kpiCard from '@/components/common/kpiCard.vue';
import UserProgressCard from './UserProgressCard.vue';
import { usePrivateTasksStore } from '@/stores/privateTasks'
import { useUserStore } from '@/stores/user'

export default {
  name: 'DashboardPage',
  components: {
    TasksTable,
    kpiCard,
    UserProgressCard
  },

  data() {
    return {
      kpis: [
        {
          title: 'Finance',
          value: '1200€',
          desc: 'incoming',
          colorClass: 'text-success',
        },
        {
          title: 'Projects',
          value: 12,
          desc: 'Completed',
          colorClass: 'text-info',
        },
        {
          title: 'Articles',
          value: '4',
          desc: 'Completed',
          colorClass: 'text-primary',
        },
        {
          title: 'Files',
          value: '20',
          desc: 'Completed',
          colorClass: 'text-warning',
        },
      ],
      taskStore: usePrivateTasksStore(),
      userStore: useUserStore(),
    }
  },
  computed: {
    progressItems() {
      return [
        {
          title: this.$t('cabinet.profile.kpi.tasks'),
          value: this.taskStore.tasksKpi.totalCompletedTasks,
          max: this.taskStore.tasksKpi.totalTasks,
          percent: Math.round(
            (this.taskStore.tasksKpi.totalCompletedTasks / this.taskStore.tasksKpi.totalTasks) *
            100,
          ),
          colorClass: 'text-success',
          progressClass: 'progress-success',
        },
        {
          title: this.$t('cabinet.profile.kpi.month_tasks'),
          value: this.taskStore.tasksKpi.totalInMonthCompleted,
          max: this.taskStore.tasksKpi.totalInMonth,
          percent: Math.round(
            (this.taskStore.tasksKpi.totalInMonthCompleted / this.taskStore.tasksKpi.totalInMonth) *
            100,
          ),
          colorClass: 'text-primary',
          progressClass: 'progress-primary',
        },
      ]
    },
  },
  // Fetch current user on mount
  async mounted() {
    if (!this.userStore.user) {
      await this.userStore.fetchMe()
    }

    await this.taskStore.fetchTasksAll()
    await this.taskStore.fetchTasksAllCompleted()
    await this.taskStore.fetchTasksAllInMonth()
    await this.taskStore.fetchTasksAllCompletedInMonth()
  },
}
</script>

<style scoped></style>
