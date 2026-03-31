<template>
  <!-- LOADING -->
  <div v-if="!loaded" class="w-full bg-base-200 border border-base-300 flex flex-col">
    <div class="skeleton w-full h-56"></div>

    <div class="p-5 flex flex-col gap-5">
      <div class="flex gap-3 bg-base-100 border border-base-300 p-4">
        <div class="skeleton w-6 h-6"></div>

        <div class="flex flex-col gap-2 w-full">
          <div class="skeleton h-4 w-32"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-5/6"></div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-base-100 border border-base-300 p-4 flex gap-3">
          <div class="skeleton w-6 h-6"></div>

          <div class="flex flex-col gap-2 w-full">
            <div class="skeleton h-4 w-20"></div>
            <div class="skeleton h-4 w-32"></div>
            <div class="skeleton h-4 w-24"></div>
          </div>
        </div>

        <div class="bg-base-100 border border-base-300 p-4 flex gap-3">
          <div class="skeleton w-6 h-6"></div>

          <div class="flex flex-col gap-2 w-full">
            <div class="skeleton h-4 w-20"></div>
            <div class="skeleton h-4 w-32"></div>
            <div class="skeleton h-4 w-24"></div>
          </div>
        </div>
      </div>

      <div class="bg-base-100 border border-base-300 p-4 flex gap-3">
        <div class="skeleton w-6 h-6"></div>

        <div class="flex flex-col gap-2 w-full">
          <div class="skeleton h-4 w-24"></div>
          <div class="skeleton h-4 w-40"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- EVENT EXISTS -->
  <div v-else-if="closestEvent" class="w-full bg-base-200 border border-base-300 flex flex-col">
    <!-- HEADER -->
    <div class="w-full h-56 bg-base-10000 relative">
      <div v-if="!loaded" class="skeleton absolute inset-0"></div>

      <img
        src="@/assets/images/aaron-burden-n3OZeX6bR0g-unsplash.jpg"
        class="w-full h-full object-cover transition-opacity duration-700"
        :class="loaded ? 'opacity-100' : 'opacity-0'"
      />

      <div class="absolute inset-0 bg-black/50 flex flex-col justify-end p-5 gap-2">
        <h1 class="text-3xl font-bold text-white flex items-center gap-3">
          <font-awesome-icon icon="fa-solid fa-calendar-days" />
          {{ closestEvent.title }}
        </h1>

        <div class="flex gap-2">
          <span :class="`badge badge-${closestEvent.color}`">
            <font-awesome-icon icon="fa-solid fa-brush" class="mr-1" />
            <p v-if="closestEvent.color == 'primary'">{{ $t('calendar.color.primary') }}</p>
            <p v-if="closestEvent.color == 'success'">{{ $t('calendar.color.success') }}</p>
            <p v-if="closestEvent.color == 'warning'">{{ $t('calendar.color.warning') }}</p>
            <p v-if="closestEvent.color == 'error'">{{ $t('calendar.color.error') }}</p>
          </span>

          <span class="badge badge-info">
            <font-awesome-icon icon="fa-solid fa-circle-info" class="mr-1" />
            <p v-if="closestEvent.status == 'active'">{{ $t('calendar.status.active') }}</p>
            <p v-if="closestEvent.status == 'cancelled'">{{ $t('calendar.status.cancelled') }}</p>
            <p v-if="closestEvent.status == 'completed'">{{ $t('calendar.status.completed') }}</p>
          </span>
        </div>
      </div>
    </div>

    <!-- BODY -->
    <div class="p-5 flex flex-col gap-5">
      <!-- DESCRIPTION -->
      <div class="flex gap-3 bg-base-100 border border-base-300 p-4">
        <font-awesome-icon icon="fa-regular fa-bookmark" class="text-xl text-primary mt-1" />

        <div class="flex flex-col gap-1">
          <span class="text-sm text-base-content/60">
            {{ $t('calendar.description') }}
          </span>

          <pre class="text-base-content/80">{{ closestEvent.description }}</pre>
        </div>
      </div>

      <!-- DATE INFO -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- START -->
        <div class="flex gap-3 bg-base-100 border border-base-300 p-4">
          <font-awesome-icon icon="fa-solid fa-calendar-plus" class="text-success text-xl mt-1" />

          <div class="flex flex-col">
            <span class="text-sm text-base-content/60">
              {{ $t('calendar.start') }}
            </span>

            <span class="font-semibold">
              {{ closestEvent.startDate }}
            </span>

            <span class="text-sm text-base-content/70">
              <font-awesome-icon icon="fa-solid fa-clock" class="mr-1" />
              {{ closestEvent.startTime }}
            </span>
          </div>
        </div>

        <!-- END -->
        <div class="flex gap-3 bg-base-100 border border-base-300 p-4">
          <font-awesome-icon icon="fa-solid fa-calendar-check" class="text-error text-xl mt-1" />

          <div class="flex flex-col">
            <span class="text-sm text-base-content/60">
              {{ $t('calendar.end') }}
            </span>

            <span class="font-semibold">
              {{ closestEvent.endDate }}
            </span>

            <span class="text-sm text-base-content/70">
              <font-awesome-icon icon="fa-solid fa-clock" class="mr-1" />
              {{ closestEvent.endTime }}
            </span>
          </div>
        </div>
      </div>

      <!-- EXTRA -->
      <div class="flex gap-3 bg-base-100 border border-base-300 p-4">
        <font-awesome-icon icon="fa-solid fa-clock" class="text-warning text-xl" />

        <div class="flex flex-col">
          <span class="text-sm text-base-content/60">
            {{ $t('calendar.duration') }}
          </span>

          <span class="font-semibold">
            {{ closestEvent.allDay ? $t('calendar.allDay') : $t('calendar.timed_event') }}
          </span>
        </div>
      </div>
    </div>
  </div>

  <!-- NO EVENTS IN MONTH -->
  <div
    v-else
    class="w-full bg-base-200 border border-base-300 p-10 flex flex-col items-center justify-center gap-4 text-center"
  >
    <font-awesome-icon icon="fa-solid fa-calendar-xmark" class="text-5xl text-base-content/40 animate-bounce" />
    <progress class="progress w-1/3 progress-neutral" max="100"></progress>
    <div class="flex flex-col gap-1">
      <h2 class="text-xl font-semibold">
        {{ $t('calendar.no_events_in_month') }}
      </h2>

      <p class="text-base-content/60">
        {{ $t('calendar.no_events_in_month_description') }}
      </p>
    </div>
  </div>
</template>

<script>
import { useEventsStore } from '@/stores/events'

export default {
  name: 'EventWidget',

  data() {
    return {
      eventsStore: useEventsStore(),
      loaded: false,
    }
  },

  computed: {
    closestEvent() {
      if (!this.eventsStore.events.length) return null

      return [...this.eventsStore.events].sort(
        (a, b) => new Date(a.startDate) - new Date(b.startDate),
      )[0]
    },
  },

  async mounted() {
    this.loaded = false
    const now = new Date()
    await this.eventsStore.getEventsByMonth(now.getMonth() + 1, now.getFullYear())
    this.loaded = true
  },
}
</script>

<style scoped></style>
