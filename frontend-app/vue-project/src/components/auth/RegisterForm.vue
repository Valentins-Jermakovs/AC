<template>
    <!-- register form -->
    <h1 class="text-red-500">
        {{ error }}
    </h1>
    <div class="divider"></div>
    <form action="" class="flex flex-col gap-5">
        <div class="form-control flex flex-col gap-2">
            <label class="label">
                <span class="label-text">{{ $t('common.email') }}</span>
            </label>
            <input v-model="email" type="email" placeholder="test@example.com"
                class="required input input-bordered w-full" />
        </div>
        <div class="form-control flex flex-col gap-2">
            <label class="label">
                <span class="label-text">{{ $t('common.username') }}</span>
            </label>
            <input v-model="username" type="text" placeholder="testuser" class="input input-bordered w-full" />
        </div>
        <div class="form-control flex flex-col gap-2">
            <label class="label">
                <span class="label-text">{{ $t('common.password') }}</span>
            </label>
            <input v-model="password" type="password" :placeholder="$t('common.password')"
                class="input input-bordered w-full" />
        </div>
        <div class="form-control flex flex-col gap-2">
            <label class="label">
                <span class="label-text">{{ $t('common.confirm_password') }}</span>
            </label>
            <input v-model="confirmPassword" type="password" :placeholder="$t('common.password')"
                class="input input-bordered w-full" />
        </div>
    </form>
    <div class="flex mt-6">
        <button class="btn btn-primary flex-1" @click="register">{{ $t('common.register') }}</button>
    </div>
    <!-- google auth button -->
    <div class="flex mt-6">
        <button class="btn btn-neutral flex-1" @click="loginGoogle">
            <font-awesome-icon icon="fa-brands fa-google" />
        </button>
    </div>
    <div class="divider"></div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
    setup() {
        const username = ref('');
        const password = ref('');
        const confirmPassword = ref('');
        const email = ref('');
        const authStore = useAuthStore();
        const router = useRouter();
        const error = ref('');
        const route = useRoute();

        onMounted(() => {
            const access = route.query.access_token
            const refresh = route.query.refresh_token

            if (access && refresh) {
                authStore.accessToken = access
                authStore.refreshToken = refresh
                authStore.isAuthenticated = true

                localStorage.setItem('accessToken', access)
                localStorage.setItem('refreshToken', refresh)

                axios.defaults.headers.common.Authorization = `Bearer ${access}`

                // noņem tokenus no URL
                router.replace('/')

            }
        })

        async function register() {
            error.value = '' // reset

            if (!username.value || !password.value || !confirmPassword.value || !email.value) {
                error.value = 'All fields are required';
                return;
            }
            if (password.value !== confirmPassword.value) {
                error.value = 'Passwords do not match';
                return;
            }

            try {
                await authStore.register(username.value, email.value, password.value);
                router.push('/');
            } catch (err) {
                console.error(err)

                if (err.response?.data?.detail) {
                    error.value = err.response.data.detail
                }
                else if (typeof err === 'string') {
                    error.value = err
                }
                else {
                    error.value = 'Registration failed'
                }
            }
        }

        return {
            username,
            password,
            email,
            confirmPassword,
            error,
            register,
        }
    },
    methods: {
        loginGoogle() {
            window.location.href = 'http://localhost:8080/auth/google/login'
        }
    }
}
</script>

<style scoped></style>