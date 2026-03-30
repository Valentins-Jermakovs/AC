<template>
  <LoadingScreen v-if="eventsStore.isLoading" />

  <div v-if="!eventsStore.selectedEvent" class="flex-1 flex flex-col w-full h-full p-3 sm:p-5 gap-3">
    <!-- Events list header -->
    <div class="w-full flex flex-col gap-4">
      <div class="w-full flex flex-col lg:flex-row gap-3 lg:items-center">
        <button class="btn btn-success w-full lg:h-full lg:w-auto" @click="openAddEventModal">
          <font-awesome-icon icon="fa-solid fa-calendar-plus" />
          Add event
        </button>

        <!-- SEARCH -->
        <div class="w-full flex flex-col sm:flex-row gap-2 border border-base-300 bg-base-100 p-2 wrap-break-word">
          <input type="text" class="input w-full" :placeholder="$t('common.search')" v-model="eventsStore.searchQuery"
            @keyup.enter="searchEvents" :disabled="eventsStore.searchType === 'all'" />

          <select class="bg-neutral text-neutral-content select select-bordered w-full sm:w-40"
            v-model="eventsStore.searchMode">
            <option value="all">{{ $t('filters.all') }}</option>
            <option value="title">{{ $t('filters.by_title') }}</option>
          </select>

          <button class="btn btn-primary w-full sm:w-auto" @click="searchEvents"
            :disabled="eventsStore.searchMode !== 'all' && !eventsStore.searchQuery.trim()">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>
    </div>

    <!-- EVENTS LIST -->
    <div class="w-full flex flex-col gap-4 bg-base-200 border border-base-300 p-2">
      <div v-for="event in eventsStore.events" :key="event.id"
        class="w-full bg-base-100 border border-base-300 p-4 flex flex-col gap-3">
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
            <span class="badge" :class="`badge-${event.color}`">{{ event.color }}</span>
            <span class="badge badge-info">{{ event.status }}</span>
          </div>
        </div>

        <!-- ACTIONS -->
        <div class="flex justify-end gap-1">
          <button class="btn btn-neutral" @click="openEditEvent(event)">
            <font-awesome-icon icon="fa-solid fa-pen-to-square" class="mr-1" />
            Edit
          </button>
        </div>
      </div>
      <!-- EMPTY -->
      <div v-if="
        !eventsStore.loading &&
        eventsStore.events.length === 0
      " class="p-4 text-center text-base-content/60 flex items-center justify-center gap-2">
        <font-awesome-icon icon="fa-solid fa-users" class="text-3xl" />
        Error, empty events
      </div>
    </div>

    <!-- FOOTER -->
    <div
      class="w-full flex flex-col sm:flex-row gap-3 sm:items-center bg-base-200 border border-base-300 wrap-break-word p-3 sm:px-4 sm:py-2">
      <!-- LIMIT -->
      <div>
        <select class="select select-bordered w-full sm:w-24" v-model="eventsStore.meta.limit"
          @change="eventsStore.setLimit(Number($event.target.value))">
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="30">30</option>
        </select>
      </div>

      <!-- META -->
      <div class="flex flex-col sm:flex-row gap-1 sm:gap-4 items-center md:items-start text-sm">

        <p>
          {{ $t('cabinet.admin.table_footer.total') }}
          <span class="font-semibold">
            {{ eventsStore.meta.total_events }}
          </span>
        </p>

        <p>
          {{ $t('cabinet.admin.table_footer.page') }}
          <span class="font-semibold">
            {{ eventsStore.meta.page }}/{{ eventsStore.meta.total_pages }}
          </span>
        </p>

      </div>

      <!-- PAGINATION -->
      <div class="flex flex-col md:flex-row gap-2 sm:ml-auto">

        <button class="btn w-full md:w-auto btn-neutral" @click="eventsStore.prevPage"
          :disabled="eventsStore.meta.page === 0 || eventsStore.meta.page === 1">
          <font-awesome-icon icon="fa-solid fa-arrow-left" />
        </button>

        <button class="btn w-full md:w-auto btn-neutral" @click="eventsStore.nextPage"
          :disabled="eventsStore.meta.page === eventsStore.meta.total_pages">
          <font-awesome-icon icon="fa-solid fa-arrow-right" />
        </button>

      </div>

    </div>
  </div>

  <!-- Add event modal -->
  <base-dialog v-model="addEventModal" title="Add event" confirmText="Create" cancelText="Cancel"
    @confirm="confirmAddEvent" @cancel="closeAddEventModal">

    <div class="flex flex-col gap-3 w-full">

      <Transition name="error-slide">
        <div v-if="eventError">
          <h1 class="text-error mb-2">{{ eventError }}</h1>
        </div>
      </Transition>

      <input class="input w-full" placeholder="Title" v-model="newEvent.title" />

      <textarea class="textarea w-full min-h-52" placeholder="Description" v-model="newEvent.description"></textarea>

      <div class="grid grid-cols-2 gap-2">

        <input type="date" class="input" v-model="newEvent.startDate" />

        <input type="date" class="input" v-model="newEvent.endDate" />

        <input type="time" class="input" v-model="newEvent.startTime" />

        <input type="time" class="input" v-model="newEvent.endTime" />

      </div>

      <label class="flex gap-2 items-center">

        <input type="checkbox" class="checkbox" v-model="newEvent.allDay" />

        All day

      </label>

      <select class="select w-full" v-model="newEvent.color">

        <option value="primary">Primary</option>
        <option value="success">Success</option>
        <option value="warning">Warning</option>
        <option value="error">Error</option>

      </select>

    </div>

  </base-dialog>


  <!-- Update event modal -->
  <base-dialog v-model="updateEventModal" title="Update event" confirmText="Update" cancelText="Cancel"
    @confirm="confirmUpdateEvent" @cancel="closeUpdateEventModal">

    <div class="flex flex-col gap-3 w-full">

      <Transition name="error-slide">
        <div v-if="eventError">
          <h1 class="text-error mb-2">{{ eventError }}</h1>
        </div>
      </Transition>

      <input class="input w-full" placeholder="Title" v-model="updateEvent.title" />

      <textarea class="textarea w-full min-h-52" placeholder="Description" v-model="updateEvent.description"></textarea>

      <div class="grid grid-cols-2 gap-2">

        <input type="date" class="input" v-model="updateEvent.startDate" />

        <input type="date" class="input" v-model="updateEvent.endDate" />

        <input type="time" class="input" v-model="updateEvent.startTime" />

        <input type="time" class="input" v-model="updateEvent.endTime" />

      </div>

      <label class="flex gap-2 items-center">

        <input type="checkbox" class="checkbox" v-model="updateEvent.allDay" />

        All day

      </label>

      <select class="select w-full" v-model="updateEvent.status">

        <option value="active">Active</option>
        <option value="cancelled">Cancelled</option>
        <option value="completed">Completed</option>

      </select>

      <select class="select w-full" v-model="updateEvent.color">

        <option value="primary">Primary</option>
        <option value="success">Success</option>
        <option value="warning">Warning</option>
        <option value="error">Error</option>

      </select>

    </div>

  </base-dialog>

  <!-- Delete event modal -->
  <base-dialog v-model="deleteEventModal" title="Delete event" confirmText="Delete" cancelText="Cancel"
    @confirm="confirmDeleteEvent" @cancel="closeAddEventModal">

    <div class="flex flex-col gap-3 w-full">

      <Transition name="error-slide">
        <div v-if="eventError">
          <h1 class="text-error mb-2">{{ eventError }}</h1>
        </div>
      </Transition>

      <p>Are you sure you want to delete this event?</p>

    </div>

  </base-dialog>

  <div v-if="eventsStore.selectedEvent"
    class=" p-4 bg-base-100 border border-base-300  flex flex-col gap-4">

    <!-- Event info -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Left column: Title + Description -->
      <div class="flex flex-col gap-2">
        <h1 class="text-3xl font-bold text-base-content">{{ eventsStore.selectedEvent.title }}</h1>
        <p class="text-base-content/70">{{ eventsStore.selectedEvent.description }}</p>
      </div>

      <!-- Right column: Details -->
      <div class="flex flex-col gap-2 text-sm text-base-content/80">
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-calendar" />
          <span>Start: {{ eventsStore.selectedEvent.startDate }} {{ eventsStore.selectedEvent.startTime }}</span>
        </div>
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-calendar-check" />
          <span>End: {{ eventsStore.selectedEvent.endDate }} {{ eventsStore.selectedEvent.endTime }}</span>
        </div>
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-clock" />
          <span>All day: {{ eventsStore.selectedEvent.allDay ? 'Yes' : 'No' }}</span>
        </div>
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-palette" />
          <span>Color:</span>
          <span :class="`badge badge-${eventsStore.selectedEvent.color}`">{{ eventsStore.selectedEvent.color }}</span>
        </div>
        <div class="flex items-center gap-2">
          <font-awesome-icon icon="fa-solid fa-info-circle" />
          <span>Status: {{ eventsStore.selectedEvent.status }}</span>
        </div>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="flex flex-col sm:flex-row gap-2 justify-end mt-4">
      <button class="btn btn-neutral flex-1 sm:flex-none" @click="openUpdateEventModal"
        :disabled="eventsStore.isCreator !== true">
        <font-awesome-icon icon="fa-solid fa-pencil" class="mr-2" />
        Update
      </button>

      <button class="btn btn-error flex-1 sm:flex-none" @click="openDeleteEventModal"
        :disabled="eventsStore.isCreator !== true">
        <font-awesome-icon icon="fa-solid fa-trash" class="mr-2" />
        Delete
      </button>

      <button class="btn btn-warning flex-1 sm:flex-none" @click="leaveEvent"
        :disabled="eventsStore.isCreator !== false">
        <font-awesome-icon icon="fa-solid fa-door-open" class="mr-2" />
        Leave Event
      </button>

      <button class="btn btn-warning flex-1 sm:flex-none" @click="closeEvent">
        <font-awesome-icon icon="fa-solid fa-arrow-left" class="mr-2" />
        Back to List
      </button>
    </div>

  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useEventsStore } from '@/stores/events'
import { useUserStore } from '@/stores/user';


export default {

  name: 'EventSpace',

  components: {
    BaseDialog,
    LoadingScreen
  },

  data() {
    return {
      eventsStore: useEventsStore(),
      userStore: useUserStore(),

      addEventModal: false,
      deleteEventModal: false,
      updateEventModal: false,

      newEvent: {
        title: '',
        description: '',
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        allDay: false,
        color: 'primary',
        status: 'active'
      },

      updateEvent: {
        title: '',
        description: '',
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        allDay: false,
        color: 'primary',
        status: 'active'
      }
    }
  },

  computed: {
    eventError() {
      return this.eventsStore.error
    },
  },

  async mounted() {
    await this.eventsStore.getAllEvents()
    await this.userStore.fetchMe()
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

    openAddEventModal() {
      this.addEventModal = true
      this.eventsStore.clearError()
    },

    closeAddEventModal() {
      this.addEventModal = false
    },

    async confirmAddEvent() {

      try {

        const event = {
          title: this.newEvent.title,
          description: this.newEvent.description,
          startDate: this.newEvent.startDate,
          endDate: this.newEvent.endDate,
          startTime: this.newEvent.startTime,
          endTime: this.newEvent.endTime,
          allDay: this.newEvent.allDay,
          color: this.newEvent.color,
          status: this.newEvent.status,
          creatorEmail: this.userStore.email
        }

        await this.eventsStore.createEvent(event)

        this.addEventModal = false

        // reset form
        this.newEvent = {
          eventId: '',
          title: '',
          description: '',
          startDate: '',
          endDate: '',
          startTime: '',
          endTime: '',
          allDay: false,
          color: 'primary',
          status: 'active'
        }

      } catch (e) {
        // error jau store
      }

    },

    openDeleteEventModal() {
      this.deleteEventModal = true
    },
    async confirmDeleteEvent() {
      try {
        await this.eventsStore.removeEvent(this.eventsStore.selectedEvent.id)
        this.deleteEventModal = false
        this.eventsStore.selectedEvent = null
      } catch (e) {

      }
    },
    closeDeleteEventModal() {
      this.deleteEventModal = false
    },
    openUpdateEventModal() {
      this.updateEventModal = true

      this.updateEvent.eventId = this.eventsStore.selectedEvent.id
      this.updateEvent.title = this.eventsStore.selectedEvent.title
      this.updateEvent.description = this.eventsStore.selectedEvent.description
      this.updateEvent.startDate = this.eventsStore.selectedEvent.startDate
      this.updateEvent.endDate = this.eventsStore.selectedEvent.endDate
      this.updateEvent.startTime = this.eventsStore.selectedEvent.startTime
      this.updateEvent.endTime = this.eventsStore.selectedEvent.endTime
      this.updateEvent.allDay = this.eventsStore.selectedEvent.allDay
      this.updateEvent.color = this.eventsStore.selectedEvent.color
      this.updateEvent.status = this.eventsStore.selectedEvent.status
    },

    async confirmUpdateEvent() {
      try {

        const event = {
          eventId: this.updateEvent.eventId,
          title: this.updateEvent.title,
          description: this.updateEvent.description,
          startDate: this.updateEvent.startDate,
          endDate: this.updateEvent.endDate,
          startTime: this.updateEvent.startTime,
          endTime: this.updateEvent.endTime,
          allDay: this.updateEvent.allDay,
          color: this.updateEvent.color,
          status: this.updateEvent.status,
          creatorEmail: this.userStore.email
        }

        await this.eventsStore.updateEvent(event)

        this.updateEventModal = false

        // reset form
        this.updateEvent = {
          eventId: '',
          title: '',
          description: '',
          startDate: '',
          endDate: '',
          startTime: '',
          endTime: '',
          allDay: false,
          color: 'primary',
          status: 'active'
        }

      } catch (e) {

      }
    },

    closeUpdateEventModal() {
      this.updateEventModal = false

      // reset form
      this.updateEvent = {
        eventId: '',
        title: '',
        description: '',
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        allDay: false,
        color: 'primary',
        status: 'active'
      }
    },

    openEditEvent(event) {
      this.eventsStore.selectedEvent = event
      if (this.eventsStore.selectedEvent) {
        this.eventsStore.checkIsCreator()
      }
    },

    closeEvent() {
      this.eventsStore.selectedEvent = null
    }
  },
}
</script>

<style scoped></style>
