<template>
  <div class="flex flex-col p-5 w-full h-full gap-2">
    <!-- KPI cards -->
    <div class="grid grid-cols-1 sm:grid-cols-4 gap-2">
      <div class="col-span-1 sm:col-span-4">
        <NewsWidget></NewsWidget>
      </div>
      <div class="col-span-1 sm:col-span-4">
        <EventWidget></EventWidget>
      </div>
      <div
        class="flex-1 flex flex-col gap-3 bg-base-200 border border-base-300 p-5 items-center justify-center text-center"
      >
        <template v-if="selectedProjectStore.selectedProject">
          <h2 class="text-2xl font-semibold text-base-content/80">
            {{ selectedProjectStore.selectedProject.workspaceTitle }}
          </h2>
        </template>
        <template v-else>
          <font-awesome-icon
            icon="fa-solid fa-folder-open"
            class="text-4xl text-base-content/40 mb-2 animate-pulse"
          />
          <h2 class="text-lg font-semibold text-base-content/60">
            {{ $t('work.projects.errors.project_not_selected') }}
          </h2>
        </template>
      </div>
      <kpiCard
        v-for="(item, index) in projectKpis"
        :key="index"
        :title="item.title"
        :value="item.value"
        :desc="item.desc"
        :colorClass="item.colorClass"
      >
      </kpiCard>
      <!-- Project Dates Card -->
      <!-- Project Dates Card -->
      <div class="flex-1 flex flex-col gap-3 bg-base-200 border border-base-300 p-5">
        <h2 class="text-2xl font-semibold text-base-content/80">
          {{ $t('cabinet.profile.kpi.project_dates.title') }}
        </h2>

        <!-- Start Date -->
        <div class="flex items-center gap-3">
          <font-awesome-icon
            :icon="
              selectedProjectStore.selectedProjectDates?.startDate
                ? 'fa-solid fa-calendar'
                : 'fa-solid fa-circle-exclamation'
            "
            :class="
              selectedProjectStore.selectedProjectDates?.startDate
                ? 'text-primary text-lg'
                : 'text-base-content/40 text-lg animate-pulse'
            "
          />
          <p class="text-base text-base-content/70">
            {{
              selectedProjectStore.selectedProjectDates?.startDate ||
              $t('work.projects.errors.no_data_for_project')
            }}
          </p>
        </div>

        <!-- End Date -->
        <div class="flex items-center gap-3">
          <font-awesome-icon
            :icon="
              selectedProjectStore.selectedProjectDates?.endDate
                ? 'fa-solid fa-clock'
                : 'fa-solid fa-circle-exclamation'
            "
            :class="
              selectedProjectStore.selectedProjectDates?.endDate
                ? 'text-warning text-lg'
                : 'text-base-content/40 text-lg animate-pulse'
            "
          />
          <p class="text-base text-base-content/70">
            {{
              selectedProjectStore.selectedProjectDates?.endDate ||
              $t('work.projects.errors.no_data_for_project')
            }}
          </p>
        </div>
      </div>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
      <kpiCard
        v-for="(item, index) in kpis"
        :key="index"
        :title="item.title"
        :value="item.value"
        :desc="item.desc"
        :colorClass="item.colorClass"
      >
      </kpiCard>
    </div>
    <!-- Progress cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      <UserProgressCard v-for="(item, index) in progressItems" :key="index" v-bind="item">
      </UserProgressCard>
    </div>
    <TasksTable></TasksTable>
  </div>
  <LoadingScreen
    v-if="taskStore.loading || userStore.loading || selectedProjectStore.loading"
  ></LoadingScreen>
</template>

<script>
import TasksTable from './dashboard/tasksTable.vue'
import kpiCard from '@/components/common/kpiCard.vue'
import UserProgressCard from './UserProgressCard.vue'
import { usePrivateTasksStore } from '@/stores/privateTasks'
import { useUserStore } from '@/stores/user'
import { useSelectedProjectStore } from '@/stores/selectedProject'
import EventWidget from '@/components/common/EventWidget.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import NewsWidget from './dashboard/NewsWidget.vue'

export default {
  name: 'DashboardPage',
  components: {
    TasksTable,
    kpiCard,
    UserProgressCard,
    EventWidget,
    LoadingScreen,
    NewsWidget,
  },

  data() {
    return {
      taskStore: usePrivateTasksStore(),
      userStore: useUserStore(),
      selectedProjectStore: useSelectedProjectStore(),
    }
  },
  computed: {
    kpis() {
      return [
        {
          title: this.$t('cabinet.profile.kpi.total_tasks.title'),
          value: this.selectedProjectStore.selectedProjectTasks.totalTasks || 0,
          desc: this.$t('cabinet.profile.kpi.total_tasks.description'),
          colorClass: 'text-info',
        },
        {
          title: this.$t('cabinet.profile.kpi.todo_tasks.title'),
          value: this.selectedProjectStore.selectedProjectTasks.todo,
          desc: this.$t('cabinet.profile.kpi.todo_tasks.description'),
          colorClass: 'text-error',
        },
        {
          title: this.$t('cabinet.profile.kpi.in_progress_tasks.title'),
          value: this.selectedProjectStore.selectedProjectTasks.inProgress,
          desc: this.$t('cabinet.profile.kpi.in_progress_tasks.description'),
          colorClass: 'text-warning',
        },
        {
          title: this.$t('cabinet.profile.kpi.done_tasks.title'),
          value: this.selectedProjectStore.selectedProjectTasks.done,
          desc: this.$t('cabinet.profile.kpi.done_tasks.description'),
          colorClass: 'text-success',
        },
      ]
    },
    projectKpis() {
      return [
        {
          title: this.$t('cabinet.profile.kpi.projects_total.title'),
          value: this.selectedProjectStore.totalProjects,
          desc: this.$t('cabinet.profile.kpi.projects_total.description'),
          colorClass: 'text-info',
        },
        {
          title: this.$t('cabinet.profile.kpi.project_stages.title'),
          value: this.selectedProjectStore.selectedProjectStagesCount,
          desc: this.$t('cabinet.profile.kpi.project_stages.description'),
          colorClass: 'text-info',
        },
      ]
    },
    progressItems() {
      return [
        {
          title: this.$t('cabinet.profile.kpi.tasks'),
          value: this.taskStore.tasksKpi.totalCompletedTasks || 0,
          max: this.taskStore.tasksKpi.totalTasks || 0,
          percent: Math.round(
            (this.taskStore.tasksKpi.totalCompletedTasks / this.taskStore.tasksKpi.totalTasks) *
              100 || 0,
          ),
          colorClass: 'text-success',
          progressClass: 'progress-success',
        },
        {
          title: this.$t('cabinet.profile.kpi.month_tasks'),
          value: this.taskStore.tasksKpi.totalInMonthCompleted || 0,
          max: this.taskStore.tasksKpi.totalInMonth || 0,
          percent: Math.round(
            (this.taskStore.tasksKpi.totalInMonthCompleted / this.taskStore.tasksKpi.totalInMonth) *
              100 || 0,
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

    await this.selectedProjectStore.getSelectedProjectData()
    await this.selectedProjectStore.getSelectedProjectStagesCount()
    await this.selectedProjectStore.getSelectedProjectDateRange()
    await this.selectedProjectStore.getSelectedProjectTasksCount()
    await this.selectedProjectStore.getProjectsCount()
  },
}
</script>

<style scoped></style>
