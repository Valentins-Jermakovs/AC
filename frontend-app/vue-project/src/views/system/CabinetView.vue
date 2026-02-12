<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons"></NavigationPanel>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue';
import headerImage from '@/assets/images/milad-fakurian-G5fdwRVoi4Q-unsplash.jpg'
import NavigationPanel from '@/components/ui/NavigationPanel.vue';

export default {
  name: 'CabinetView',
  components: { 
    PageHeader,
    NavigationPanel
  },

  data() {
    return {
      image: headerImage,
    }
  },

  computed: {
    title() {
      return this.$t('cabinet.title');
    },
    navButtons() {
      let navButtons = [
        { key: 'dashboard', title: this.$t('cabinet.nav_bar.dashboard') },
        { key: 'profile', title: this.$t('cabinet.nav_bar.profile') },
      ]

      return navButtons
    }
  }
};
</script>

<style scoped></style>
