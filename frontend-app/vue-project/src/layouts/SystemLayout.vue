<template>
    <div class="h-full grid grid-cols-12 grid-rows-12">
        <div class="col-span-12 row-span-1">
            <TopBar></TopBar>
        </div>
    </div>    
</template>

<script>
import TopBar from '@/components/system/topbar/TopBar.vue';

export default {
    name: 'SystemLayout',
    components: {
        TopBar
    }
}
</script>

<style scoped>
</style>