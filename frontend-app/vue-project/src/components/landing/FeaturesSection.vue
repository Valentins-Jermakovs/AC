<template>
  <section class="py-16 bg-base-100">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-bold mb-12">
        {{ $t('landingPage.features.title') }}
      </h2>

      <div class="grid md:grid-cols-3 gap-8">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="card p-6 md:bg-base-200 md:card-border md:border-base-300"
        >
          <div class="text-4xl mb-4">
            <font-awesome-icon :icon="feature.icon" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t(feature.title) }}
          </h3>
          <p>{{ $t(feature.description) }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'LandingFeatures',
  data() {
    return {
      features: [
        {
          icon: 'tasks',
          title: 'landingPage.features.tasks',
          description: 'landingPage.features.tasks_description',
        },
        {
          icon: 'calendar-alt',
          title: 'landingPage.features.events',
          description: 'landingPage.features.events_description',
        },
        {
          icon: 'chart-bar',
          title: 'landingPage.features.analytics',
          description: 'landingPage.features.analytics_description',
        },
        {
          icon: 'wallet',
          title: 'landingPage.features.finances',
          description: 'landingPage.features.finances_description',
        },
        {
          icon: ['fab', 'google'],
          title: 'landingPage.features.google',
          description: 'landingPage.features.google_description',
        },
        {
          icon: 'leaf',
          title: 'landingPage.features.environment',
          description: 'landingPage.features.environment_description',
        },
      ],
    }
  },
}
</script>

<style scoped></style>
