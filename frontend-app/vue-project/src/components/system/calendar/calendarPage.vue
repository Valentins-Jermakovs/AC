<template>
  <div class="flex flex-col gap-5 p-5">
    <div class="bg-base-200 border border-base-300 p-3 overflow-x-auto">
      <CalendarHeader
        :year="currentYear"
        :month="currentMonth"
        :months="months"
        @prev="prevMonth"
        @next="nextMonth"
      >
      </CalendarHeader>

      <CalendarGrid
        :days="calendarDays"
        :isToday="isToday"
        :events="eventsStore.events"
        :currentMonth="currentMonth"
        :currentYear="currentYear"
      >
      </CalendarGrid>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 bg-base-200 p-3 border border-base-300">
      <EventCard v-for="event in eventsStore.events" :key="event.id" :event="event"></EventCard>
    </div>
  </div>
</template>

<script>
import EventCard from '@/components/common/EventCard.vue'
import CalendarHeader from '@/components/common/CalendarHeader.vue'
import CalendarGrid from '@/components/common/CalendarGrid.vue'
import { useEventsStore } from '@/stores/events'

export default {
  components: {
    EventCard,
    CalendarHeader,
    CalendarGrid,
  },

  data() {
    return {
      eventsStore: useEventsStore(),
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),

    }
  },

  async mounted() {
    await this.eventsStore.getEventsByMonth(this.currentMonth + 1, this.currentYear)
  },

  methods: {
    isToday(day) {
      if (!day) return false
      const today = new Date()
      return (
        day === today.getDate() &&
        this.currentMonth === today.getMonth() &&
        this.currentYear === today.getFullYear()
      )
    },

    prevMonth() {
      if (this.currentMonth === 0) {
        this.currentMonth = 11
        this.currentYear -= 1
      } else {
        this.currentMonth -= 1
      }
      this.eventsStore.getEventsByMonth(this.currentMonth + 1, this.currentYear)
    },

    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentMonth = 0
        this.currentYear += 1
      } else {
        this.currentMonth += 1
      }
      this.eventsStore.getEventsByMonth(this.currentMonth + 1, this.currentYear)
    },
  },

  computed: {
    calendarDays() {
      const firstDay = new Date(this.currentYear, this.currentMonth, 1)
      let startDay = firstDay.getDay() - 1
      if (startDay < 0) startDay = 6

      const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate()

      const days = []
      for (let i = 0; i < startDay; i++) days.push(null)
      for (let d = 1; d <= daysInMonth; d++) days.push(d)
      while (days.length % 7 !== 0) days.push(null)

      return days
    },

    months() {
      return [
        this.$t('calendar.month.january'),
        this.$t('calendar.month.february'),
        this.$t('calendar.month.march'),
        this.$t('calendar.month.april'),
        this.$t('calendar.month.may'),
        this.$t('calendar.month.june'),
        this.$t('calendar.month.july'),
        this.$t('calendar.month.august'),
        this.$t('calendar.month.september'),
        this.$t('calendar.month.october'),
        this.$t('calendar.month.november'),
        this.$t('calendar.month.december'),
      ]
    }
  },
}
</script>
