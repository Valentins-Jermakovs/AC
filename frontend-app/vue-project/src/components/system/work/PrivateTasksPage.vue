<template>
    <div class=" h-full bg-base-100 p-1 flex">
        <!-- Left screen: task list with search bar, filter button, search button -->
        <!-- and drop down menu and buttons for pagination -->
        <div class="w-1/2 bg-base-200 border-base-300 border ">
            <div class="w-full h-full p-1 flex flex-col  items-center justify-between gap-1">

                <!-- Search bar, filter button, search button -->
                <div class="flex w-full items-center bg-base-100 p-3 border border-base-300
                rounded-box">
                    <!-- Search panel -->
                    <input type="text" class="flex-1 input bg-base-100
                    text-lg" placeholder="Meklēt...">
                    <!-- Filter dropdown list -->
                    <select class="select select-bordered w-auto bg-neutral text-neutral-content">
                        <option disabled selected>Filter</option>
                        <option>All</option>
                        <option>By title</option>
                        <option>By description</option>
                        <option>By duedate</option>
                        <option>By month and year</option>
                    </select>
                    <!-- Search button -->
                    <button class="btn btn-primary">
                        <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
                    </button>
                </div>


                <!-- Task list -->
                <div class="w-full flex flex-col gap-2 flex-1 bg-base-100 overflow-y-scroll
                rounded-box border border-base-300 p-2">
                    <!-- Task list items go here -->

                    <!-- Task -->
                    <div class="w-full h-16 flex items-center p-2
                    border border-base-300
                    bg-base-200
                    hover:bg-base-300
                    hover:cursor-pointer">

                        <div class="flex flex-col flex-1 px-4">
                            <h1 class="font-medium text-md">
                                Title lorem ipsum...
                            </h1>

                            <p class="text-xs text-base-content/60">
                                Description lorem ipsum...
                            </p>
                        </div>

                        <div class="pr-4 text-xs text-base-content/60">
                            Due 2023-06-17
                        </div>

                    </div>

                    <!-- Task -->
                    <div class="w-full h-16 flex items-center p-2
                    border border-base-300
                    bg-base-200
                    hover:bg-base-300
                    hover:cursor-pointer">

                        <div class="flex flex-col flex-1 px-4">
                            <h1 class="font-medium text-md">
                                Title lorem ipsum...
                            </h1>

                            <p class="text-xs text-base-content/60">
                                Description lorem ipsum...
                            </p>
                        </div>

                        <div class="pr-4 text-xs text-base-content/60">
                            Due 2023-06-17
                        </div>

                    </div>

                    <!-- Task -->
                    <div class="w-full h-16 flex items-center p-2
                    border border-base-300
                    bg-base-200
                    hover:bg-base-300
                    hover:cursor-pointer">

                        <div class="flex flex-col flex-1 px-4">
                            <h1 class="font-medium text-md">
                                Title lorem ipsum...
                            </h1>

                            <p class="text-xs text-base-content/60">
                                Description lorem ipsum...
                            </p>
                        </div>

                        <div class="pr-4 text-xs text-base-content/60">
                            Due 2023-06-17
                        </div>

                    </div>

                    <!-- Task -->
                    <div class="w-full h-16 flex items-center p-2
                    border border-base-300
                    bg-base-200
                    hover:bg-base-300
                    hover:cursor-pointer">

                        <div class="flex flex-col flex-1 px-4">
                            <h1 class="font-medium text-md">
                                Title lorem ipsum...
                            </h1>

                            <p class="text-xs text-base-content/60">
                                Description lorem ipsum...
                            </p>
                        </div>

                        <div class="pr-4 text-xs text-base-content/60">
                            Due 2023-06-17
                        </div>

                    </div>
                </div>

                <!-- Pagination controls -->
                <div class="w-full p-4 rounded-box 
                    border border-base-300 bg-base-100 
                    flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <!-- Left section: Limit selector, total users, current page info -->
                    <div class="flex flex-col 
                    sm:flex-row sm:items-center sm:gap-6 w-full sm:w-auto">

                        <!-- Page size selector -->
                        <div class="flex flex-col sm:flex-row sm:items-center gap-2">
                            <label class="text-sm opacity-70">
                                limit
                            </label>
                            <select class="select select-bordered mt-1 sm:mt-0">
                                <option :value="5">5</option>
                                <option :value="10">10</option>
                                <option :value="20">20</option>
                                <option :value="50">50</option>
                            </select>
                        </div>

                        <!-- Total users count -->
                        <div class="text-sm opacity-80 whitespace-nowrap">
                            Total:
                            <span class="font-semibold">total</span>
                        </div>

                        <!-- Current page info -->
                        <div class="text-sm opacity-80 whitespace-nowrap">
                            Page Current:
                            <span class="font-semibold">1</span> /
                            <span class="font-semibold">10</span>
                        </div>
                    </div>

                    <!-- Right section: Pagination buttons -->
                    <div class="flex flex-col sm:flex-row sm:gap-3 gap-2 w-full sm:w-auto">
                        <button class="btn btn-neutral hover:btn-primary flex-1 p-2">
                            <font-awesome-icon icon=" fa-solid fa-arrow-left" />
                        </button>
                        <button class="btn btn-neutral hover:btn-primary flex-1 p-2">
                            <font-awesome-icon icon="fa-solid fa-arrow-right" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Right screen: task details -->
        <div class="w-1/2 bg-base-200 border-base-300 border-y border-r p-1 flex flex-col gap-4">

            <!-- Task Card -->
            <div class="border border-base-300 rounded-box p-4 bg-base-100 flex flex-col gap-5 h-full">

                <div class="flex flex-col gap-5">
                    <!-- Title -->
                    <h1 class="font-semibold text-2xl">Title Title Title Title</h1>

                    <!-- Metadata -->
                    <div class="flex flex-wrap gap-4 text-sm text-base-content/70">
                        <div class="flex gap-1 items-center">
                            <span class="font-medium">Status:</span>
                            <span class="px-2 py-0.5 rounded-full bg-green-100 text-green-800 text-xs">Completed</span>
                        </div>
                        <div class="flex gap-1 items-center">
                            <span class="font-medium">Created:</span>
                            <span class="text-info">2023-06-17</span>
                        </div>
                        <div class="flex gap-1 items-center">
                            <span class="font-medium">Due date:</span>
                            <span class="text-warning">2023-06-17</span>
                        </div>
                    </div>
                </div>

                <div>
                    <!-- Description -->
                    <p class="text-base text-base-content/70">
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Enim laborum modi dolor atque eaque!
                        Vel soluta error dolores itaque reprehenderit eveniet porro nulla, beatae suscipit aliquam
                        asperiores laudantium, ipsam fugiat. Porro reiciendis omnis dolorum beatae labore laborum
                        rem vel nesciunt libero vitae, saepe voluptatum cum debitis voluptatibus doloribus
                        voluptate quidem distinctio delectus excepturi impedit iure, eaque officiis nam! Ullam, quam.
                    </p>
                    <div class="divider"></div>
                </div>

                <!-- divider -->
                <div class="flex-1"></div>

                <!-- Action Buttons -->
                <div class="flex flex-wrap justify-end gap-2 mt-2">
                    <button class="btn btn-md btn-error">Delete</button>
                    <button class="btn btn-md btn-success">Complete</button>
                    <button class="btn btn-md btn-secondary">Edit</button>
                    <button class="btn btn-md btn-primary">Create new</button>
                </div>

            </div>

        </div>
    </div>
</template>

<script>
</script>

<style scoped></style>