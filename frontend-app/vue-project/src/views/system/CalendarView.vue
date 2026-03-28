<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>

  <CalendarPage v-if="activePage === 'calendar'"></CalendarPage>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue';
import headerImage from '@/assets/images/claudio-guglieri-Qj8haLTfHzs-unsplash.jpg'

// for testing only
import { useEventsStore } from '@/stores/events';
import NavigationPanel from '@/components/ui/NavigationPanel.vue';
import CalendarPage from '@/components/system/calendar/calendarPage.vue';

export default {
  name: 'CalendarView',
  components: {
    PageHeader,
    NavigationPanel,
    CalendarPage
  },
  data() {
    return {
      title: 'Calendar',
      image: headerImage,

      eventsStore: useEventsStore(),

      // Currently active page
      activePage: 'calendar',
    }
  },

  async mounted() {
    //await this.eventsStore.getAllEvents();
    await this.eventsStore.getEventsByMonth(3, 2026);
  },

  computed: {
    navButtons() {
      // Basic navigation buttons
      let navButtons = [
        {
          key: 'calendar',
          title: "Calendar",
        },
        {
          key: 'events',
          title: "Events",
        },
        {
          key: 'participants',
          title: "Participants",
        },
      ]

      return navButtons
    },
  }
}

</script>

<style scoped></style>
