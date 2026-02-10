<template>
    <AuthLayout>
        <AuthHeader></AuthHeader>
        <RegisterForm></RegisterForm>
        <AuthFooter></AuthFooter>
    </AuthLayout>
</template>

<script>
import AuthFooter from '@/components/auth/AuthFooter.vue';
import AuthHeader from '@/components/auth/AuthHeader.vue';
import RegisterForm from '@/components/auth/RegisterForm.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';

export default {
    components: {
        AuthFooter,
        AuthHeader,
        RegisterForm,
        AuthLayout
    }
}
</script>

<style scoped></style>