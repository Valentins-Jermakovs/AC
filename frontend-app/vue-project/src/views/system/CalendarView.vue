<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>

  <CalendarPage v-if="activePage === 'calendar'"></CalendarPage>
  <EventsPage v-if="activePage === 'events'"></EventsPage>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue'
import headerImage from '@/assets/images/rinat-aidarkhan-4UubN0f3PYc-unsplash.jpg'

// for testing only
import { useEventsStore } from '@/stores/events'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'
import CalendarPage from '@/components/system/calendar/calendarPage.vue'
import EventsPage from '@/components/system/calendar/eventsPage.vue'

export default {
  name: 'CalendarView',
  components: {
    PageHeader,
    NavigationPanel,
    CalendarPage,
    EventsPage,
  },
  data() {
    return {
      image: headerImage,

      eventsStore: useEventsStore(),

      // Currently active page
      activePage: 'calendar',
    }
  },

  async mounted() {
    //await this.eventsStore.getAllEvents();
    await this.eventsStore.getEventsByMonth(3, 2026)
  },

  computed: {
    title() {
      return this.$t('calendar.titles.calendar')
    },
    navButtons() {
      // Basic navigation buttons
      let navButtons = [
        {
          key: 'calendar',
          title: this.$t('calendar.titles.calendar'),
        },
        {
          key: 'events',
          title: this.$t('calendar.titles.events'),
        },
      ]

      return navButtons
    },
  },
}
</script>

<style scoped></style>
