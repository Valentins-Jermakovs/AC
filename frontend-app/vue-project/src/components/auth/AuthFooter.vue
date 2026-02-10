<template>
    <!-- Navigation links to registration and login -->
    <!-- if login: link to register -->
    <div v-if="isLogin">
        <h3>
            {{ $t('common.switch_to_register') }}
            <router-link to="/register" class="link link-hover link-primary underline">
                {{ $t('common.register') }}
            </router-link>
        </h3>
    </div>
    <!-- if register: link to login -->
    <div v-if="isRegister">
        <h3>
            {{ $t('common.switch_to_login') }}
            <router-link to="/login" class="link link-hover link-primary underline">
                {{ $t('common.login') }}
            </router-link>
        </h3>
    </div>
</template>

<script>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

export default {
    setup() {
        const route = useRoute()

        const isLogin = computed(() => route.name === 'login')
        const isRegister = computed(() => route.name === 'register')

        return {
            isLogin,
            isRegister,
        }
    }
}
</script>

<style scoped></style>