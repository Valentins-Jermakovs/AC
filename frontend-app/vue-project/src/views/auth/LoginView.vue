<template>
    <AuthLayout>
        <AuthHeader></AuthHeader>
        <LoginForm></LoginForm>
        <AuthFooter></AuthFooter>
    </AuthLayout>
</template>

<script>
import AuthFooter from '@/components/auth/AuthFooter.vue';
import AuthHeader from '@/components/auth/AuthHeader.vue';
import LoginForm from '@/components/auth/LoginForm.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';

export default {
    components: {
        AuthFooter,
        AuthHeader,
        LoginForm,
        AuthLayout
    }
}
</script>

<style scoped></style>