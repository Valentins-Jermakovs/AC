<template>
    <div class="flex flex-col w-72">
        <div class="bg-base-200 border border-base-300
        w-full h-16 flex items-center gap-3 pl-2">
            <!-- Title -->
            <h1 class="flex-1 w-full text-center">ToDo</h1>
            <!-- left dropdown -->
            <div class="dropdown dropdown-right">
                <div tabindex="0" role="button" class="btn m-1">:</div>
                <ul tabindex="-1" class="dropdown-content menu bg-base-200 border
                border-base-300 rounded-box z-1 w-52 p-2 items-start">
                    <li class="w-full">
                        <button class="btn btn-sm btn-ghost">
                            <font-awesome-icon icon="fa-solid fa-pencil" /> Update stage
                        </button>
                    </li>
                    <li class="w-full">
                        <button class="btn btn-sm btn-ghost">
                            <font-awesome-icon icon="fa-solid fa-arrow-left" /> Insert stage before
                        </button>
                    </li>
                    <li class="w-full">
                        <button class="btn btn-sm btn-ghost">
                            <font-awesome-icon icon="fa-solid fa-arrow-right" /> Insert stage after
                        </button>
                    </li>
                    <li class="w-full">
                        <button class="btn btn-sm btn-ghost">
                            <font-awesome-icon icon="fa-solid fa-arrow-right" /> Move stage to right
                        </button>
                    </li>
                    <li class="w-full">
                        <button class="btn btn-sm btn-ghost">
                            <font-awesome-icon icon="fa-solid fa-arrow-left" /> Move stage to left
                        </button>
                    </li>
                    <li class="w-full">
                        <button class="btn btn-sm btn-ghost">
                            <font-awesome-icon icon="fa-solid fa-trash" /> Delete stage
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        <!-- List -->
        <div class="w-full bg-base-200 border border-base-300 p-1 flex flex-col
        items-center">
            <!-- Items -->
            <div class="w-full flex flex-col bg-base-100 border border-base-300 p-2
            gap-2">
                <!-- Title and options -->
                <div class="w-full  rounded-box
                flex items-center">
                    <h1 class="flex-1 w-full">Lorem ipsum</h1>
                    <div class="dropdown dropdown-right">
                        <div tabindex="0" role="button" class="btn">:</div>
                        <ul tabindex="-1" class="dropdown-content menu bg-base-200 border
                        border-base-300 rounded-box z-1 w-52 p-2 items-start">
                            <li class="w-full">
                                <button class="btn btn-sm btn-ghost">
                                    <font-awesome-icon icon="fa-solid fa-pencil" /> Update task
                                </button>
                            </li>
                            <li class="w-full">
                                <button class="btn btn-sm btn-ghost">
                                    <font-awesome-icon icon="fa-solid fa-arrow-up" /> Move up
                                </button>
                            </li>
                            <li class="w-full">
                                <button class="btn btn-sm btn-ghost">
                                    <font-awesome-icon icon="fa-solid fa-arrow-down" /> Move down
                                </button>
                            </li>
                            <li class="w-full">
                                <button class="btn btn-sm btn-ghost">
                                    <font-awesome-icon icon="fa-solid fa-arrow-right" /> Move to right stage
                                </button>
                            </li>
                            <li class="w-full">
                                <button class="btn btn-sm btn-ghost">
                                    <font-awesome-icon icon="fa-solid fa-arrow-left" /> Move to left stage
                                </button>
                            </li>
                            <li class="w-full">
                                <button class="btn btn-sm btn-ghost">
                                    <font-awesome-icon icon="fa-solid fa-trash" /> Delete task
                                </button>
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- Description -->
                <div class="bg-base-200 border border-base-200 w-full
                rounded-box p-1">
                    <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Adipisci, blanditiis excepturi debitis facere vitae quam
                        quaerat facilis exercitationem laboriosam numquam a quibusdam
                        corrupti perspiciatis id, quo animi ratione sapiente fuga?
                    </p>
                </div>
            </div>
        </div>
        <!-- Create task button -->
        <div class="bg-base-200 p-1 w-full border border-base-300">
            <button class="btn btn-primary w-full">
                <font-awesome-icon icon="fa-solid fa-plus" />
                Create task
            </button>
        </div>
    </div>
</template>

<script>
</script>

<style scoped></style>