<template>
  <!-- login form -->
  <div class="divider"></div>
  <form action="" class="flex flex-col gap-5">
    <div class="form-control flex flex-col gap-2">
      <label class="label">
        <span class="label-text">{{ $t('common.email') }}</span>
      </label>
      <input type="email" :placeholder="$t('common.email')" class="input input-bordered w-full" />
    </div>
    <div class="form-control flex flex-col gap-2">
      <label class="label">
        <span class="label-text">{{ $t('common.password') }}</span>
      </label>
      <input
        type="password"
        :placeholder="$t('common.password')"
        class="input input-bordered w-full"
      />
    </div>
  </form>
  <div class="flex mt-6">
    <button class="btn btn-primary flex-1">
      {{ $t('common.login') }}
    </button>
  </div>
  <!-- google auth button -->
  <div class="flex mt-6">
    <button class="btn btn-neutral flex-1">
      <font-awesome-icon icon="fa-brands fa-google" />
    </button>
  </div>
  <div class="divider"></div>
</template>

<script setup>


</script>

<style scoped></style>