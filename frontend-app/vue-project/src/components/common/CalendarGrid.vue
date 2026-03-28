<template>
    <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 text-xs sm:text-sm gap-1">
        <div v-for="(day, index) in days" :key="index" class="h-24 border border-base-content/10 p-2 flex flex-col gap-1 overflow-hidden
      bg-base-100" :class="{
        'bg-base-300 font-bold': day && isToday(day),
    }">
            <!-- Day number -->
            <span v-if="day" class="font-semibold">
                {{ day }}
            </span>

            <!-- Events -->
            <div v-for="event in getEventsForDay(day)" :key="event.id"
                class="text-xs px-1 py-0.5 mb-0.5 truncate text-white" :class="colorClass(event.color)">
                {{ event.title }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CalendarGrid',

    props: {
        days: {
            type: Array,
            required: true,
        },

        isToday: {
            type: Function,
            required: true,
        },

        events: {
            type: Array,
            required: true,
        },

        currentMonth: {
            type: Number,
            required: true,
        },

        currentYear: {
            type: Number,
            required: true,
        },
    },

    methods: {

        getEventsForDay(day) {
  if (!day) return []

  const currentDate = { 
    year: this.currentYear, 
    month: this.currentMonth, 
    day 
  }

  return this.events.filter(event => {
    const start = new Date(event.startDate)
    const end = new Date(event.endDate)

    // salīdzinām tikai gads/mēnesis/diena
    const startDate = { year: start.getFullYear(), month: start.getMonth(), day: start.getDate() }
    const endDate = { year: end.getFullYear(), month: end.getMonth(), day: end.getDate() }

    const afterStart =
      currentDate.year > startDate.year ||
      (currentDate.year === startDate.year &&
        (currentDate.month > startDate.month ||
          (currentDate.month === startDate.month && currentDate.day >= startDate.day)))

    const beforeEnd =
      currentDate.year < endDate.year ||
      (currentDate.year === endDate.year &&
        (currentDate.month < endDate.month ||
          (currentDate.month === endDate.month && currentDate.day <= endDate.day)))

    return afterStart && beforeEnd
  })
},

        colorClass(color) {
            const colors = {
                primary: 'bg-primary',
                secondary: 'bg-secondary',
                success: 'bg-success',
                warning: 'bg-warning',
                error: 'bg-error',
                info: 'bg-info',
            }

            return colors[color] || 'bg-neutral'
        }

    }
}
</script>