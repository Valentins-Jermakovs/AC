<template>
  <div class="card rounded-none bg-base-100 border border-base-300 border-l-2" :class="colorBorder">
    <div class="card-body gap-2">
      <!-- Title -->
      <h3 class="card-title text-lg">
        {{ event.title }}
      </h3>

      <!-- Description -->
      <p class="text-sm text-base-content/70">
        {{ event.description }}
      </p>

      <!-- Date info -->
      <div class="flex flex-col text-sm text-base-content/70 mt-2 gap-1">
        <span>
          <font-awesome-icon icon="fa-solid fa-calendar" class="mr-1" />
          <b>Start:</b>
          {{ event.startDate }}
          <span v-if="!event.allDay">
            <font-awesome-icon icon="fa-solid fa-clock" class="mr-1" />
            {{ event.startTime }}
          </span>
        </span>

        <span>
          <font-awesome-icon icon="fa-solid fa-calendar" class="mr-1" />
          <b>End:</b>
          {{ event.endDate }}
          <span v-if="!event.allDay">
            <font-awesome-icon icon="fa-solid fa-clock" class="mr-1" />
            {{ event.endTime }}
          </span>
        </span>

        <span v-if="event.allDay" class="italic">
          <font-awesome-icon icon="fa-solid fa-clock" class="mr-1" />
          All day event
        </span>
      </div>

      <!-- Status -->
      <div class="flex justify-between items-center mt-3">
        <div class="badge badge-outline">
          {{ event.status }}
        </div>

        <div class="w-3 h-3" :class="colorClass"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventCard',

  props: {
    event: {
      type: Object,
      required: true,
    },
  },

  computed: {
    colorClass() {
      const colors = {
        primary: 'bg-primary',
        secondary: 'bg-secondary',
        accent: 'bg-accent',
        success: 'bg-success',
        warning: 'bg-warning',
        error: 'bg-error',
        info: 'bg-info',
      }

      return colors[this.event.color] || 'bg-base-300'
    },

    colorBorder() {
      const colors = {
        primary: 'border-l-primary',
        secondary: 'border-l-secondary',
        accent: 'border-l-accent',
        success: 'border-l-success',
        warning: 'border-l-warning',
        error: 'border-l-error',
        info: 'border-l-info',
      }

      return colors[this.event.color] || 'border-l-base-300'
    },
  },
}
</script>
