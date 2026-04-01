<template>
  <LoadingScreen
    v-if="eventsStore.loading || userStore.loading || eventParticipantsStore.loading"
  />

  <div
    v-if="!eventsStore.selectedEvent"
    class="flex-1 flex flex-col w-full h-full p-3 sm:p-5 gap-3"
  >
    <!-- Events list header -->
    <div class="w-full flex flex-col gap-4">
      <div class="w-full flex flex-col lg:flex-row gap-3 lg:items-center">
        <button class="btn btn-success w-full lg:h-full lg:w-auto" @click="openAddEventModal">
          <font-awesome-icon icon="fa-solid fa-calendar-plus" />
          {{ $t('calendar.add_event') }}
        </button>

        <!-- SEARCH -->
        <div
          class="w-full flex flex-col sm:flex-row gap-2 border border-base-300 bg-base-200 p-2 wrap-break-word"
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
            :disabled="eventsStore.searchMode !== 'all' && eventsStore.searchQuery.length < 3"
          >
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>
    </div>

    <!-- EVENTS LIST -->
    <div class="w-full flex flex-col gap-4 bg-base-200 border border-base-300 p-2">
      <!-- EVENTS -->
      <div
        v-for="event in eventsStore.events"
        :key="event.id"
        class="w-full bg-base-100 border border-base-300 p-4 flex flex-col gap-3"
      >
        <!-- TITLE -->
        <div class="flex items-center gap-3 text-lg font-bold text-base-content">
          <font-awesome-icon icon="fa-solid fa-calendar-alt" class="text-primary text-xl" />
          <span class="truncate">{{ event.title }}</span>
        </div>

        <!-- DESCRIPTION -->
        <div
          class="text-sm text-base-content/70 p-2 bg-base-200/50 border border-base-300 wrap-break-word"
        >
          <pre v-if="event.description" class="text-wrap">{{ event.description }}</pre>
          <div
            v-else
            class="flex items-center gap-3 p-4 bg-base-100 border border-base-300 animate-fadeIn"
          >
            <div class="text-warning text-xl animate-pulse">
              <font-awesome-icon icon="fa-solid fa-circle-exclamation" />
            </div>

            <div class="flex flex-col">
              <span class="font-semibold text-base-content">
                {{ $t('calendar.errors.no_description_title') }}
              </span>

              <span class="text-xs text-base-content/60">
                {{ $t('calendar.errors.no_description') }}
              </span>
            </div>
          </div>
        </div>

        <!-- DATE & TIME -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-sm">
          <!-- Start -->
          <div class="flex flex-col gap-1">
            <div class="flex items-center gap-1">
              <font-awesome-icon icon="fa-solid fa-calendar-plus" class="text-success" />
              <span class="font-medium">{{ $t('calendar.start') }}:</span>
              <span>{{ event.startDate }}</span>
            </div>
            <div class="flex items-center gap-1">
              <font-awesome-icon icon="fa-solid fa-clock" class="text-warning" />
              <span v-if="event.startTime">{{ event.startTime }}</span>
              <font-awesome-icon v-else icon="fa-solid fa-xmark" class="text-error" />
            </div>
          </div>

          <!-- End -->
          <div class="flex flex-col gap-1">
            <div class="flex items-center gap-1">
              <font-awesome-icon icon="fa-solid fa-calendar-check" class="text-error" />
              <span class="font-medium">{{ $t('calendar.end') }}:</span>
              <span>{{ event.endDate }}</span>
            </div>
            <div class="flex items-center gap-1">
              <font-awesome-icon icon="fa-solid fa-clock" class="text-warning" />
              <span v-if="event.endTime">{{ event.endTime }}</span>
              <font-awesome-icon v-else icon="fa-solid fa-xmark" class="text-error" />
            </div>
          </div>

          <!-- All day -->
          <div class="flex items-center gap-1">
            <font-awesome-icon icon="fa-solid fa-clock" class="text-info" />
            <span class="font-medium">{{ $t('calendar.all_day') }}:</span>
            <font-awesome-icon
              v-if="event.allDay"
              icon="fa-solid fa-check"
              class="text-success badge badge-neutral rounded-full"
            />
            <font-awesome-icon
              v-else
              icon="fa-solid fa-xmark"
              class="text-error badge badge-neutral rounded-full"
            />
          </div>

          <!-- Status / Color badges -->
          <div class="flex gap-2 flex-wrap">
            <span v-if="event.color === 'primary'" class="badge badge-primary">{{
              $t('calendar.color.primary')
            }}</span>
            <span v-if="event.color === 'success'" class="badge badge-success">{{
              $t('calendar.color.success')
            }}</span>
            <span v-if="event.color === 'warning'" class="badge badge-warning">{{
              $t('calendar.color.warning')
            }}</span>
            <span v-if="event.color === 'error'" class="badge badge-error">{{
              $t('calendar.color.error')
            }}</span>
            <span class="badge badge-info">
              <p v-if="event.status === 'active'">{{ $t('calendar.status.active') }}</p>
              <p v-if="event.status === 'completed'">{{ $t('calendar.status.completed') }}</p>
              <p v-if="event.status === 'cancelled'">{{ $t('calendar.status.cancelled') }}</p>
            </span>
          </div>
        </div>

        <!-- ACTIONS -->
        <div class="flex justify-end gap-2 mt-2">
          <button
            class="btn btn-sm btn-neutral flex items-center gap-1"
            @click="openEditEvent(event)"
          >
            <font-awesome-icon icon="fa-solid fa-link" class="text-primary" />
            <span>{{ $t('calendar.more') }}</span>
          </button>
        </div>
      </div>

      <!-- EMPTY -->
      <div
        v-if="!eventsStore.loading && eventsStore.events.length === 0"
        class="col-span-full p-10 text-center text-base-content/60 flex flex-col items-center justify-center gap-4 animate-pulse"
      >
        <font-awesome-icon
          icon="fa-solid fa-calendar-xmark"
          class="text-5xl text-base-content/40 animate-bounce"
        />
        <progress class="progress w-1/3 progress-neutral" max="100"></progress>
        <p class="text-lg italic">
          {{ $t('calendar.errors.no_events') }}
        </p>
      </div>
    </div>

    <!-- FOOTER -->
    <div
      class="w-full flex flex-col sm:flex-row gap-3 sm:items-center bg-base-200 border border-base-300 wrap-break-word p-3 sm:px-4 sm:py-2"
    >
      <!-- LIMIT -->
      <div>
        <select
          class="select select-bordered w-full sm:w-24"
          v-model="eventsStore.meta.limit"
          @change="eventsStore.setLimit(Number($event.target.value))"
        >
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
        <button
          class="btn w-full md:w-auto btn-neutral"
          @click="eventsStore.prevPage"
          :disabled="eventsStore.meta.page === 0 || eventsStore.meta.page === 1"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-left" />
        </button>

        <button
          class="btn w-full md:w-auto btn-neutral"
          @click="eventsStore.nextPage"
          :disabled="eventsStore.meta.page === eventsStore.meta.total_pages"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-right" />
        </button>
      </div>
    </div>
  </div>

  <!-- Add event modal -->
  <base-dialog
    v-model="addEventModal"
    :title="$t('calendar.modals.create_event.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmAddEvent"
    @cancel="closeAddEventModal"
  >
    <div class="flex flex-col gap-3 w-full">
      <Transition name="error-slide">
        <div v-if="eventError">
          <h1 class="text-error mb-2">{{ eventError }}</h1>
        </div>
      </Transition>
      <label class="label w-full">
        {{ $t('calendar.modals.create_event.name') }}
      </label>
      <input
        class="input w-full"
        :placeholder="$t('calendar.modals.create_event.name_placeholder')"
        v-model="newEvent.title"
      />
      <label class="label w-full">
        {{ $t('calendar.modals.create_event.description') }}
      </label>
      <div class="w-full flex justify-end text-sm opacity-70 pr-1">
        {{ descriptionRemainingChars }} / {{ descriptionMaxLength }}
      </div>
      <textarea
        class="textarea w-full"
        maxlength="1000"
        :placeholder="$t('calendar.modals.create_event.description_placeholder')"
        v-model="newEvent.description"
      ></textarea>
      <label class="label w-full">
        {{ $t('calendar.modals.create_event.time_settings') }}
      </label>
      <div class="grid grid-cols-2 gap-2">
        <input type="date" class="input" v-model="newEvent.startDate" />
        <input type="date" class="input" v-model="newEvent.endDate" />
        <input type="time" class="input" v-model="newEvent.startTime" />
        <input type="time" class="input" v-model="newEvent.endTime" />
      </div>
      <label class="flex gap-2 items-center">
        <input type="checkbox" class="checkbox" v-model="newEvent.allDay" />
        {{ $t('calendar.modals.create_event.all_day') }}
      </label>
      <label class="label w-full">
        {{ $t('calendar.modals.create_event.color') }}
      </label>
      <select class="select w-full" v-model="newEvent.color">
        <option value="primary">{{ $t('calendar.color.primary') }}</option>
        <option value="success">{{ $t('calendar.color.success') }}</option>
        <option value="warning">{{ $t('calendar.color.warning') }}</option>
        <option value="error">{{ $t('calendar.color.error') }}</option>
      </select>
    </div>
  </base-dialog>

  <!-- Update event modal -->
  <base-dialog
    v-model="updateEventModal"
    :title="$t('calendar.modals.update_event.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmUpdateEvent"
    @cancel="closeUpdateEventModal"
  >
    <div class="flex flex-col gap-3 w-full">
      <Transition name="error-slide">
        <div v-if="eventError">
          <h1 class="text-error mb-2">{{ eventError }}</h1>
        </div>
      </Transition>
      <label class="label w-full">{{ $t('calendar.modals.update_event.name') }}</label>
      <input
        class="input w-full"
        :placeholder="$t('calendar.modals.update_event.name_placeholder')"
        v-model="updateEvent.title"
      />
      <label class="label w-full">{{ $t('calendar.modals.update_event.description') }}</label>
      <textarea
        class="textarea w-full"
        maxlength="1000"
        :placeholder="$t('calendar.modals.update_event.description_placeholder')"
        v-model="updateEvent.description"
      ></textarea>
      <label class="label w-full">{{ $t('calendar.modals.update_event.time_settings') }}</label>
      <div class="grid grid-cols-2 gap-2">
        <input type="date" class="input" v-model="updateEvent.startDate" />
        <input type="date" class="input" v-model="updateEvent.endDate" />
        <input type="time" class="input" v-model="updateEvent.startTime" />
        <input type="time" class="input" v-model="updateEvent.endTime" />
      </div>
      <label class="flex gap-2 items-center">
        <input type="checkbox" class="checkbox" v-model="updateEvent.allDay" />
        {{ $t('calendar.modals.update_event.all_day') }}
      </label>
      <label class="label w-full">{{ $t('calendar.modals.update_event.status') }}</label>
      <select class="select w-full" v-model="updateEvent.status">
        <option value="active">{{ $t('calendar.status.active') }}</option>
        <option value="cancelled">{{ $t('calendar.status.cancelled') }}</option>
        <option value="completed">{{ $t('calendar.status.complete') }}</option>
      </select>
      <label class="label w-full">{{ $t('calendar.modals.update_event.color') }}</label>
      <select class="select w-full" v-model="updateEvent.color">
        <option value="primary">{{ $t('calendar.color.primary') }}</option>
        <option value="success">{{ $t('calendar.color.success') }}</option>
        <option value="warning">{{ $t('calendar.color.warning') }}</option>
        <option value="error">{{ $t('calendar.color.error') }}</option>
      </select>
    </div>
  </base-dialog>

  <!-- Delete event modal -->
  <base-dialog
    v-model="deleteEventModal"
    :title="$t('calendar.modals.delete_event.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmDeleteEvent"
    @cancel="closeAddEventModal"
  >
    <div class="flex flex-col gap-3 w-full">
      <Transition name="error-slide">
        <div v-if="eventError">
          <h1 class="text-error mb-2">{{ eventError }}</h1>
        </div>
      </Transition>

      <p>{{ $t('calendar.modals.delete_event.content') }}</p>
    </div>
  </base-dialog>

  <div v-if="eventsStore.selectedEvent" class="p-4 bg-base-100 flex flex-col gap-4">
    <div class="bg-base-200 border border-base-300 p-4 flex flex-col gap-6">
      <!-- Event info -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left column: Title + Description -->
        <div class="flex flex-col gap-3 p-2 border border-base-300 bg-base-100">
          <h1 class="text-3xl font-bold text-base-content ml-2 wrap-break-word">
            {{ eventsStore.selectedEvent.title }}
          </h1>
          <pre
            v-if="eventsStore.selectedEvent.description"
            class="bg-base-200/50 p-4 text-sm border border-base-300 flex-1 text-base-content/70 whitespace-pre-wrap wrap-break-word"
            >{{ eventsStore.selectedEvent.description }}</pre
          >
          <div
            v-else
            class="flex items-center w-full flex-1 gap-3 p-4 bg-base-200 animate-fadeIn border border-base-300"
          >
            <div class="text-warning text-xl animate-pulse">
              <font-awesome-icon icon="fa-solid fa-circle-exclamation" />
            </div>

            <div class="flex flex-col">
              <span class="font-semibold text-base-content">
                {{ $t('calendar.errors.no_description_title') }}
              </span>

              <span class="text-xs text-base-content/60">
                {{ $t('calendar.errors.no_description') }}
              </span>
            </div>
          </div>
        </div>

        <!-- Right column: Details -->
        <div class="flex flex-col gap-3 text-base-content/80 text-lg">
          <div class="flex gap-2 flex-col bg-base-100 p-2 border border-base-300">
            <div class="flex gap-2 items-center">
              <font-awesome-icon icon="fa-solid fa-calendar" class="text-success" />
              <span
                ><strong>{{ $t('calendar.start') }}:</strong>
                {{ eventsStore.selectedEvent.startDate }}</span
              >
            </div>
            <div class="flex gap-2 items-center">
              <font-awesome-icon icon="fa-solid fa-clock" />
              <span v-if="eventsStore.selectedEvent.startTime">{{
                eventsStore.selectedEvent.startTime
              }}</span>
              <font-awesome-icon v-else icon="fa-solid fa-xmark" class="text-error" />
            </div>
          </div>

          <div class="flex gap-2 flex-col bg-base-100 p-2 border border-base-300">
            <div class="flex gap-2 items-center">
              <font-awesome-icon icon="fa-solid fa-calendar" class="text-error" />
              <span
                ><strong>{{ $t('calendar.end') }}:</strong>
                {{ eventsStore.selectedEvent.endDate }}</span
              >
            </div>
            <div class="flex gap-2 items-center">
              <font-awesome-icon icon="fa-solid fa-clock" />
              <span v-if="eventsStore.selectedEvent.endTime">{{
                eventsStore.selectedEvent.endTime
              }}</span>
              <font-awesome-icon v-else icon="fa-solid fa-xmark" class="text-error" />
            </div>
          </div>
          <div class="flex items-center gap-2">
            <font-awesome-icon icon="fa-solid fa-clock" class="text-info" />
            <span>
              <strong>{{ $t('calendar.all_day') }}: </strong>
              <font-awesome-icon
                v-if="eventsStore.selectedEvent.allDay"
                icon="fa-solid fa-check"
                class="text-success badge badge-neutral rounded-full"
              />
              <font-awesome-icon
                v-else
                icon="fa-solid fa-xmark"
                class="text-error badge badge-neutral rounded-full"
              />
            </span>
          </div>
          <div class="flex items-center gap-2">
            <font-awesome-icon icon="fa-solid fa-brush" class="text-primary" />
            <span
              ><strong>{{ $t('calendar.color_text') }}:</strong></span
            >
            <span
              v-if="eventsStore.selectedEvent.color === 'warning'"
              class="badge badge-warning"
              >{{ $t('calendar.color.warning') }}</span
            >
            <span
              v-if="eventsStore.selectedEvent.color === 'success'"
              class="badge badge-success"
              >{{ $t('calendar.color.success') }}</span
            >
            <span
              v-if="eventsStore.selectedEvent.color === 'primary'"
              class="badge badge-primary"
              >{{ $t('calendar.color.primary') }}</span
            >
            <span v-if="eventsStore.selectedEvent.color === 'error'" class="badge badge-error">{{
              $t('calendar.color.error')
            }}</span>
          </div>
          <div class="flex items-center gap-2">
            <font-awesome-icon icon="fa-solid fa-info-circle" class="text-warning" />
            <span
              ><strong>{{ $t('calendar.status_text') }}: </strong>
              <span v-if="eventsStore.selectedEvent.status === 'active'" class="badge badge-info">{{
                $t('calendar.status.active')
              }}</span>
              <span
                v-if="eventsStore.selectedEvent.status === 'completed'"
                class="badge badge-success"
                >{{ $t('calendar.status.completed') }}</span
              >
              <span
                v-if="eventsStore.selectedEvent.status === 'cancelled'"
                class="badge badge-error"
                >{{ $t('calendar.status.cancelled') }}</span
              >
            </span>
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex flex-col sm:flex-row gap-3 justify-end mt-4">
        <button
          class="btn btn-neutral flex-1 sm:flex-none flex items-center justify-center gap-2"
          @click="openUpdateEventModal"
          :disabled="eventsStore.isCreator !== true"
        >
          <font-awesome-icon icon="fa-solid fa-pencil" />
          {{ $t('common.edit') }}
        </button>

        <button
          class="btn btn-error flex-1 sm:flex-none flex items-center justify-center gap-2"
          @click="openDeleteEventModal"
          :disabled="eventsStore.isCreator !== true"
        >
          <font-awesome-icon icon="fa-solid fa-trash" />
          {{ $t('common.delete') }}
        </button>

        <button
          class="btn btn-warning flex-1 sm:flex-none flex items-center justify-center gap-2"
          @click="leaveEvent"
          :disabled="eventsStore.isCreator !== false"
        >
          <font-awesome-icon icon="fa-solid fa-door-open" />
          {{ $t('calendar.leave_event') }}
        </button>

        <button
          class="btn btn-warning flex-1 sm:flex-none flex items-center justify-center gap-2"
          @click="closeEvent"
        >
          <font-awesome-icon icon="fa-solid fa-arrow-left" />
          {{ $t('calendar.back_to_list') }}
        </button>
      </div>
    </div>

    <!-- Event members -->
    <EventMembers v-if="eventsStore.isCreator == true"></EventMembers>
    <!-- Leave event modal -->
    <!-- Add member modal -->
    <base-dialog
      v-model="leaveModal"
      :title="$t('calendar.modals.leave_event.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmLeave"
      @cancel="closeLeaveModal"
    >
      <div class="w-full flex flex-col gap-2">
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <p>{{ $t('calendar.modals.leave_event.content') }}</p>
      </div>
    </base-dialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { useEventsStore } from '@/stores/events'
import { useEventParticipantsStore } from '@/stores/eventParticipants'
import { useUserStore } from '@/stores/user'
import EventMembers from './eventMembers.vue'

export default {
  name: 'EventSpace',

  components: {
    BaseDialog,
    LoadingScreen,
    EventMembers,
  },

  data() {
    return {
      eventsStore: useEventsStore(),
      userStore: useUserStore(),
      eventParticipantsStore: useEventParticipantsStore(),
      descriptionMaxLength: 1000,

      addEventModal: false,
      deleteEventModal: false,
      updateEventModal: false,

      leaveModal: false,
      error: '',

      newEvent: {
        title: '',
        description: '',
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        allDay: false,
        color: 'primary',
        status: 'active',
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
        status: 'active',
      },
    }
  },

  computed: {
    descriptionRemainingChars() {
      return this.descriptionMaxLength - (this.newEvent.description?.length || 0)
    },
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
          creatorEmail: this.userStore.email,
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
          status: 'active',
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
      } catch (e) {}
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
      if (this.updateEvent.title === '') {
        this.updateEvent.title = this.eventsStore.selectedEvent.title
        this.eventsStore.error = 'Title cannot be empty'
        return
      }
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
          creatorEmail: this.userStore.email,
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
          status: 'active',
        }

        this.eventsStore.refresh()

        // get selected event from store, where ids are the same
        for (let i = 0; i < this.eventsStore.events.length; i++) {
          if (this.eventsStore.events[i].id === this.eventsStore.selectedEvent.id) {
            this.eventsStore.selectedEvent = this.eventsStore.events[i]
            break
          }
        }
      } catch (e) {}
    },

    closeUpdateEventModal() {
      this.eventsStore.error = ''
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
        status: 'active',
      }
    },

    openEditEvent(event) {
      this.eventsStore.selectedEvent = event
      this.eventParticipantsStore.selectedEvent = event
      if (this.eventsStore.selectedEvent) {
        this.eventsStore.checkIsCreator()
      }
    },

    closeEvent() {
      this.eventsStore.selectedEvent = null
      this.eventsStore.getAllEvents()
    },
    leaveEvent() {
      this.leaveModal = true
    },
    closeLeaveModal() {
      this.leaveModal = false
    },
    async confirmLeave() {
      await this.eventParticipantsStore.leaveEvent()
      this.eventsStore.selectedEvent = null
      await this.eventsStore.getAllEvents()
    },
  },
}
</script>

<style scoped></style>
