<template>
  <div 
  class="bg-base-100 border border-base-300 
  border-l-2 p-4 flex flex-col gap-3 transition"
  :class="colorBorder"
>

  <!-- HEADER -->
  <div class="flex items-start justify-between">

    <div class="flex flex-col">
      <h3 class="font-semibold text-base-content text-lg leading-tight">
        {{ event.title }}
      </h3>

      <p class="text-sm text-base-content/60 line-clamp-2">
        {{ event.description }}
      </p>
    </div>

    <div class="badge badge-info">
      <p v-if="event.status == 'active'">{{ $t('calendar.status.active') }}</p>
      <p v-if="event.status == 'cancelled'">{{ $t('calendar.status.cancelled') }}</p>
      <p v-if="event.status == 'completed'">{{ $t('calendar.status.completed') }}</p>
    </div>

  </div>


  <!-- DATE BLOCK -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">

    <!-- START -->
    <div class="flex items-center gap-2 bg-base-200 px-3 py-2">

      <font-awesome-icon 
        icon="fa-solid fa-calendar-plus"
        class="text-success"
      />

      <div class="flex flex-col">

        <span class="text-xs text-base-content/50">
          {{ $t('calendar.start') }}
        </span>

        <span class="font-medium">
          {{ event.startDate }}
        </span>

        <span 
          v-if="!event.allDay"
          class="text-xs text-base-content/60"
        >
          {{ event.startTime }}
        </span>

      </div>

    </div>


    <!-- END -->
    <div class="flex items-center gap-2 bg-base-200 px-3 py-2">

      <font-awesome-icon 
        icon="fa-solid fa-calendar-check"
        class="text-error"
      />

      <div class="flex flex-col">

        <span class="text-xs text-base-content/50">
          {{ $t('calendar.end') }}
        </span>

        <span class="font-medium">
          {{ event.endDate }}
        </span>

        <span 
          v-if="!event.allDay"
          class="text-xs text-base-content/60"
        >
          {{ event.endTime }}
        </span>

      </div>

    </div>

  </div>


  <!-- FOOTER -->
  <div class="flex justify-between items-center text-xs text-base-content/60">

    <div v-if="event.allDay" class="flex items-center gap-1">

      <font-awesome-icon 
        icon="fa-solid fa-clock"
        class="text-warning"
      />

      {{ $t('calendar.all_day') }}

    </div>

    <div class="flex items-center gap-2">

      <div 
        class="w-2 h-2 rounded-full"
        :class="colorClass"
      ></div>

      <span class="uppercase tracking-wide">
        <p v-if="event.color == 'primary'">{{ $t('calendar.color.primary') }}</p>
        <p v-if="event.color == 'success'">{{ $t('calendar.color.success') }}</p>
        <p v-if="event.color == 'warning'">{{ $t('calendar.color.warning') }}</p>
        <p v-if="event.color == 'error'">{{ $t('calendar.color.error') }}</p>
      </span>

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
