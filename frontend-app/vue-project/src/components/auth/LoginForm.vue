<template>
  <!-- login form -->
  <div class="divider"></div>
  <form action="" class="flex flex-col gap-5">
    <div class="form-control flex flex-col gap-2">
      <label class="label">
        <span class="label-text">{{ $t('common.username') }}</span>
      </label>
      <input v-model="username" placeholder="testuser" class="input input-bordered w-full" />
    </div>
    <div class="form-control flex flex-col gap-2">
      <label class="label">
        <span class="label-text">{{ $t('common.password') }}</span>
      </label>
      <input
        v-model="password"
        type="password"
        :placeholder="$t('common.password')"
        class="input input-bordered w-full"
      />
    </div>
  </form>
  <div class="flex mt-6">
    <button class="btn btn-primary flex-1"
      @click="login">
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

<script>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const authStore = useAuthStore();
    const router = useRouter();

    async function login() {
      try {
        await authStore.login(username.value, password.value);
        router.push('/');
      } catch (error) {
        console.error(error);
      }
    }

    return {
      username,
      password,
      login,
    }
  },
};

</script>

<style scoped></style>