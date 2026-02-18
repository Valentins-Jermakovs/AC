<template>
  <div class="flex flex-col lg:flex-row p-5 gap-5">
    <!-- Card One -->
    <div class="w-full lg:w-1/2 bg-base-200 rounded-box border border-base-300 min-h-50 p-6 lg:p-10 flex flex-col justify-around">
      <h1 class="text-2xl lg:text-3xl">{{ $t('cabinet.admin.cards.card_one.title') }}</h1>
      <p class="text-base lg:text-lg">{{ $t('cabinet.admin.cards.card_one.content') }}</p>
    </div>

    <!-- Card Two -->
    <div class="w-full lg:w-1/2 bg-base-200 rounded-box border border-base-300 min-h-50 p-6 lg:p-10 flex flex-col justify-center gap-3">
      <h2 class="text-lg lg:text-xl">{{ $t('cabinet.admin.cards.card_two.title') }}</h2>
      <ul class="list-disc pl-5 text-sm lg:text-base">
        <li>{{ $t('cabinet.admin.cards.card_two.content[0]') }}</li>
        <li>{{ $t('cabinet.admin.cards.card_two.content[1]') }}</li>
        <li>{{ $t('cabinet.admin.cards.card_two.content[2]') }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminCards',
}
</script>

<style scoped></style>