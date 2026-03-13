<template>
    <div class="h-full flex flex-col w-64 bg-base-200 border border-base-300 p-1
    gap-2">
        <!-- Search bar -->
        <div class="w-full p-1 bg-base-100 border border-base-300
        flex flex-col items-center gap-2">
            <div class="w-full">
                <input type="text" class="input" placeholder="Search...">
            </div>
            <div class="w-full flex items-center gap-2">
                <select class="select select-bordered flex-1">
                    <option disabled selected>Filter</option>
                    <option>Filter 1</option>
                    <option>Filter 2</option>
                </select>
                <button class="btn btn-primary">
                    <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
                </button>
            </div>
        </div>
        <!-- List of boards -->
        <div class="w-full  flex flex-1 flex-col bg-base-100 border border-base-300
        overflow-y-auto p-3 gap-2">
            <!-- Item -->
            <div class="w-full bg-base-200 border border-base-300 rounded-box p-3
            flex items-center justify-start pl-2 hover:cursor-pointer hover:border-2 hover:border-info
            duration-300 transition-all">
                <h1>Lorem ipsum dolor...</h1>
            </div>
        </div>
        <!-- Footer -->
        <div class="bg-base-100 border border-base-300 flex flex-col p-1 gap-2">
            <!-- Limit drop down menu -->
            <select class="select select-bordered w-full max-w-xs">
                <option disabled selected>Limit</option>
                <option>10</option>
                <option>20</option>
                <option>30</option>
            </select>
            <!-- Info -->
            <div class="w-full p-1 flex flex-col items-start
            bg-base-100 border border-base-300 gap-1 text-base-content/60">
                <p>Current page 1/2</p>
                <p>Limit: 10</p>
            </div>
            <!-- Pagination buttons -->
            <div class="w-full gap-1 flex items-center p-1 justify-center">
                <button class="btn btn-neutral w-1/2">
                    <font-awesome-icon icon="fa-solid fa-arrow-left" />
                </button>
                <button class="btn btn-neutral w-1/2">
                    <font-awesome-icon icon="fa-solid fa-arrow-right" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
</script>

<style scoped>
</style>