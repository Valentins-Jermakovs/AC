<template>
  <LoadingScreen v-if="eventsStore.isLoading" />

  <div class="flex-1 flex flex-col w-full h-full p-3 sm:p-5 gap-3">
    <!-- Events list header -->
    <div class="w-full flex flex-col gap-4">
      <div class="w-full flex flex-col lg:flex-row gap-3 lg:items-center">
        <button class="btn btn-success w-full lg:h-full lg:w-auto" @click="openAddEventModal">
          <font-awesome-icon icon="fa-solid fa-calendar-plus" />
          Add event
        </button>

        <!-- SEARCH -->
        <div
          class="w-full flex flex-col sm:flex-row gap-2 border border-base-300 bg-base-100 p-2 wrap-break-word"
        >
          <input
            type="text"
            class="input w-full"
            :placeholder="$t('common.search')"
            v-model="eventsStore.searchQuery"
            @keyup.enter="searchEvents"
            :disabled="eventsStore.searchType === 'all'"
          />

          <select
            class="bg-neutral text-neutral-content select select-bordered w-full sm:w-40"
            v-model="eventsStore.searchMode"
          >
            <option value="all">{{ $t('filters.all') }}</option>
            <option value="title">{{ $t('filters.by_title') }}</option>
          </select>

          <button
            class="btn btn-primary w-full sm:w-auto"
            @click="searchEvents"
            :disabled="eventsStore.searchMode !== 'all' && !eventsStore.searchQuery.trim()"
          >
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>
    </div>

    <!-- EVENTS LIST -->
    <div class="w-full flex flex-col gap-4 bg-base-200 border border-base-300 p-2">
      <div
        v-for="event in eventsStore.events"
        :key="event.id"
        class="w-full bg-base-100 border border-base-300 p-4 flex flex-col gap-3"
      >
        <!-- TITLE -->
        <div class="flex items-center gap-2 text-lg font-bold text-base-content">
          <font-awesome-icon icon="fa-solid fa-calendar" />
          {{ event.title }}
        </div>

        <!-- DESCRIPTION -->
        <div class="text-sm text-base-content/70 wrap-break-word p-2 bg-base-200">
          {{ event.description }}
        </div>

        <!-- DATE & TIME -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm text-base-content/60">
          <div class="flex gap-1 flex-col">
            <div>
              <font-awesome-icon icon="fa-solid fa-calendar" />
              Start: {{ event.startDate }}
            </div>
            <div>
              <font-awesome-icon icon="fa-solid fa-clock" />
              {{ event.startTime }}
            </div>
          </div>
          <div class="flex flex-col gap-1">
            <div>
              <font-awesome-icon icon="fa-solid fa-clock" />
              End: {{ event.endDate }}
            </div>
            <div>
              <font-awesome-icon icon="fa-solid fa-clock" />
              {{ event.endTime }}
            </div>
          </div>
          <div>All Day: {{ event.allDay ? 'Yes' : 'No' }}</div>
          <div class="flex gap-1 flex-wrap">
            <span class="badge" :class="'badge-' + event.color">{{ event.color }}</span>
            <span class="badge badge-info">{{ event.status }}</span>
          </div>
        </div>

        <!-- ACTIONS -->
        <div class="flex justify-end mt-2">
          <button class="btn btn-info">
            <font-awesome-icon icon="fa-solid fa-link" />
            Enter
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useEventsStore } from '@/stores/events'

export default {
  name: 'EventSpace',
  components: { BaseDialog, LoadingScreen },

  data() {
    return {
      eventsStore: useEventsStore(),
    }
  },

  computed: {
    eventError() {
      return this.eventsStore.error
    },
  },

  async mounted() {
    await this.eventsStore.getAllEvents()
  },

  methods: {
    openAddEventModal() {
      // šobrīd tikai loga atvēršana
      this.addEventModal = true
      this.eventsStore.clearError()
    },

    async searchEvents() {
      this.eventsStore.meta.page = 1

      if (this.eventsStore.searchMode === 'all') {
        await this.eventsStore.getAllEvents()
      } else if (this.eventsStore.searchMode === 'title') {
        if (this.eventsStore.searchQuery.trim()) {
          await this.eventsStore.getEventsByTitle()
        }
      }
    },

    async changeLimit(limit) {
      await this.eventsStore.setLimit(Number(limit))
    },
  },
}
</script>

<style scoped></style>
