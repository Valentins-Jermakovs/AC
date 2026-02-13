<template>
  <section class="py-16 bg-base-100">
    <div class="container mx-auto text-center ">
      <h2 class="text-3xl font-bold mb-12">
        {{ $t('landingPage.features.title') }}
      </h2>
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Esošie trīs bloki -->
        <div class="card p-6 md:bg-base-200 md:card-border md:border-base-300">
          <div class="text-4xl mb-4">
            <font-awesome-icon icon="tasks" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t('landingPage.features.tasks') }}
          </h3>
          <p>{{ $t('landingPage.features.tasks_description') }}</p>
        </div>
        <div class="card p-6 md:bg-base-200 md:card-border md:border-base-300">
          <div class="text-4xl mb-4">
            <font-awesome-icon icon="calendar-alt" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t('landingPage.features.events') }}
          </h3>
          <p>{{ $t('landingPage.features.events_description') }}</p>
        </div>
        <div class="card p-6 md:bg-base-200 md:card-border md:border-base-300">
          <div class="text-4xl mb-4">
            <font-awesome-icon icon="chart-bar" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t('landingPage.features.analytics') }}
          </h3>
          <p>{{ $t('landingPage.features.analytics_description') }}</p>
        </div>

        <!-- Jaunie bloki -->
        <div class="card p-6 md:bg-base-200 md:card-border md:border-base-300">
          <div class="text-4xl mb-4">
            <font-awesome-icon icon="wallet" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t('landingPage.features.finances') }}
          </h3>
          <p>{{ $t('landingPage.features.finances_description') }}</p>
        </div>

        <div class="card p-6 md:bg-base-200 md:card-border md:border-base-300">
          <div class="text-4xl mb-4">
            <font-awesome-icon icon="fa-brands fa-google" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t('landingPage.features.google') }}
          </h3>
          <p>{{ $t('landingPage.features.google_description') }}</p>
        </div>

        <div class="card p-6 md:bg-base-200 md:card-border md:border-base-300">
          <div class="text-4xl mb-4">
            <font-awesome-icon icon="leaf" />
          </div>
          <h3 class="text-xl font-semibold mb-2">
            {{ $t('landingPage.features.environment') }}
          </h3>
          <p>{{ $t('landingPage.features.environment_description') }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
