<template>
    <!-- Instruction cards -->
    <div class="flex flex-col lg:flex-row p-5 gap-5">

        <div class="w-full lg:w-1/2 bg-base-300 min-h-50 p-6 lg:p-10 flex flex-col justify-around">
            <h1 class="text-2xl lg:text-3xl">{{ $t('cabinet.admin.cards.card_one.title') }}</h1>
            <p class="text-base lg:text-lg">
                {{ $t('cabinet.admin.cards.card_one.content') }}
            </p>
        </div>

        <div class="w-full lg:w-1/2 bg-base-200 min-h-50 p-6 lg:p-10 flex flex-col justify-center gap-3">
            <h2 class="text-lg lg:text-xl">{{ $t('cabinet.admin.cards.card_two.title') }}</h2>
            <ul class="list-disc pl-5 text-sm lg:text-base">
                <li>{{ $t('cabinet.admin.cards.card_two.content[0]') }}</li>
                <li>{{ $t('cabinet.admin.cards.card_two.content[1]') }}</li>
                <li>{{ $t('cabinet.admin.cards.card_two.content[2]') }}</li>
            </ul>
        </div>

    </div>

    <!-- Admin panel -->
    <div class="px-4 sm:px-5 pb-5">
        <div class="flex flex-col w-full bg-base-200 border border-base-300">
            <!-- Admin panel top (control elements) -->
            <div class="flex flex-col xl:flex-row w-full bg-base-100">
                <div class="flex flex-col lg:flex-row flex-1 ">
                    <!-- Search bar -->
                    <div class="flex flex-col sm:flex-row flex-1 p-4 gap-3 items-stretch sm:items-center">
                        <input type="text" v-model="adminStore.searchQuery" :placeholder="$t('common.search')"
                            class="input input-bordered w-full"
                            :disabled="adminStore.searchMode === '' || adminStore.searchMode === 'all'" />
                        <button class="btn btn-primary" @click="searchButton">{{ $t('common.make_query') }}</button>
                    </div>
                    <!-- Search filter - dropdown list -->
                    <div class="flex p-4 items-center">
                        <select v-model="adminStore.searchMode" class="select select-bordered w-full lg:w-64"
                            @change="clearEmptyError">
                            <option value="all">{{ $t('cabinet.admin.admin_top.filters[0]') }}</option>
                            <option value="id">{{ $t('cabinet.admin.admin_top.filters[1]') }}</option>
                            <option value="username">{{ $t('cabinet.admin.admin_top.filters[2]') }}</option>
                            <option value="role">{{ $t('cabinet.admin.admin_top.filters[3]') }}</option>
                        </select>
                    </div>
                </div>
                <!-- Control buttons-->
                <div class="flex flex-col sm:flex-row flex-wrap gap-3 p-4 justify-center">

                    <button class="btn btn-neutral hover:btn-primary w-full sm:w-auto" @click="addRoleModal = true"
                        :class="selectedUserIds.length === 0 ? 'btn-disabled' : ''">
                        {{ $t('common.add_role') }}
                    </button>

                    <button class="btn btn-neutral hover:btn-primary w-full sm:w-auto" @click="removeRoleModal = true"
                        :class="selectedUserIds.length === 0 ? 'btn-disabled' : ''">
                        {{ $t('common.remove_role') }}
                    </button>

                    <button class="btn btn-neutral hover:btn-primary w-full sm:w-auto"
                        @click="changeActivityModal = true" :class="selectedUserIds.length === 0 ? 'btn-disabled' : ''">
                        {{ $t('common.change_activity') }}
                    </button>

                </div>

            </div>
            <Transition name="error-slide">
                <div v-if="emptyError" class="w-full bg-base-100 p-5 border border-base-300">
                    <h1 class="text-error text-center">{{ emptyError }}</h1>
                </div>
            </Transition>
            <!-- Admin panel table Desktop -->
            <!-- Desktop table -->
            <div class="hidden lg:block w-full overflow-x-auto p-4">
                <table class="table w-full min-w-175">
                    <thead>
                        <tr>
                            <th class="whitespace-nowrap">
                                <label>
                                    <input type="checkbox" class="checkbox checkbox-neutral" v-model="selectAll"
                                        @change="toggleSelectAll" />
                                </label>
                            </th>
                            <th class="whitespace-nowrap">ID</th>
                            <th class="whitespace-nowrap">{{ $t('cabinet.admin.table_top.username') }}</th>
                            <th class="whitespace-nowrap max-w-50">{{ $t('cabinet.admin.table_top.email') }}</th>
                            <th class="whitespace-nowrap max-w-45">{{ $t('cabinet.admin.table_top.roles') }}</th>
                            <th class="whitespace-nowrap">{{ $t('cabinet.admin.table_top.created_at') }}</th>
                            <th class="whitespace-nowrap">{{ $t('cabinet.admin.table_top.status') }}</th>
                        </tr>
                    </thead>

                    <tbody v-if="!adminStore.loading">
                        <tr v-if="adminStore.users.length > 0" v-for="user in adminStore.users" :key="user.id"
                            :class="{ 'bg-base-300': selectedUserIds.includes(user.id) }">
                            <td class="whitespace-nowrap">
                                <label>
                                    <input type="checkbox" class="checkbox checkbox-neutral" v-model="selectedUserIds"
                                        :value="user.id" />
                                </label>
                            </td>
                            <td class="whitespace-nowrap">{{ user.id }}</td>
                            <td class="whitespace-nowrap">{{ user.username }}</td>
                            <td class="truncate max-w-50" :title="user.email">{{ user.email }}</td>
                            <td>
                                <div class="flex gap-2 overflow-x-auto max-w-45">
                                    <span v-for="role in user.roles" :key="role" class="badge badge-info">{{ role
                                    }}</span>
                                </div>
                            </td>
                            <td class="whitespace-nowrap">{{ user.created_at }}</td>
                            <td class="whitespace-nowrap">
                                <span :class="user.active ? 'text-success' : 'text-error'">
                                    {{ user.active ? $t('cabinet.admin.table_body.status_active') : $t('cabinet.admin.table_body.status_inactive') }}
                                </span>
                            </td>
                        </tr>
                        <tr v-else>
                            <td colspan="7">
                                <div class="p-4">
                                    <div class="alert alert-error flex">
                                        <div class="flex flex-col p-2 text-2xl  w-full gap-2">
                                            <div class="flex gap-5 items-center justify-center">
                                                <font-awesome-icon icon="fa-solid fa-info-circle" />
                                                <span>{{ $t('common.no_data') }}</span>
                                            </div>
                                            <div class="flex items-center justify-center">
                                                <p>{{ $t('common.try_later') }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr>
                            <td colspan="7">
                                <LoadingScreen />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Mobile card layout -->
            <div class="lg:hidden p-4 space-y-4">

                <div v-if="!adminStore.loading">
                    <div v-for="user in adminStore.users" :key="user.id" v-if="adminStore.users.length > 0"
                        class="bg-base-200 border border-base-300 p-4 shadow-sm"
                        :class="{ 'bg-base-300': selectedUserIds.includes(user.id) }">
                        <!-- Top row -->
                        <div class="flex justify-between items-start mb-3">
                            <div>
                                <div class="font-semibold text-lg">
                                    {{ user.username }}
                                </div>
                                <div class="text-sm opacity-70">
                                    {{ user.email }}
                                </div>
                            </div>

                            <input type="checkbox" class="checkbox checkbox-neutral" v-model="selectedUserIds"
                                :value="user.id" />
                        </div>

                        <!-- Info grid -->
                        <div class="grid grid-cols-2 gap-3 text-sm">

                            <div>
                                <div class="opacity-60">ID</div>
                                <div>{{ user.id }}</div>
                            </div>

                            <div>
                                <div class="opacity-60">{{ $t('cabinet.admin.table_top.status') }}</div>
                                <div :class="user.active ? 'text-success' : 'text-error'">
                                    {{ user.active ? 'Aktīvs' : 'Bloķēts' }}
                                </div>
                            </div>

                            <div class="col-span-2">
                                <div class="opacity-60 mb-1">{{ $t('cabinet.admin.table_top.roles') }}</div>
                                <div class="flex flex-wrap gap-2">
                                    <span v-for="role in user.roles" :key="role" class="badge badge-info">
                                        {{ role }}
                                    </span>
                                </div>
                            </div>

                            <div class="col-span-2">
                                <div class="opacity-60">{{ $t('cabinet.admin.table_top.created_at') }}</div>
                                <div>{{ user.created_at }}</div>
                            </div>

                        </div>
                    </div>

                    <div v-else>
                        <div class="p-4">
                            <div class="alert alert-error flex">
                                <div class="flex flex-col p-2 text-2xl  w-full gap-2">
                                    <div class="flex gap-5 items-center justify-center">
                                        <font-awesome-icon icon="fa-solid fa-info-circle" />
                                        <span>{{ $t('common.no_data') }}</span>
                                    </div>
                                    <div class="flex items-center justify-center">
                                        <p>{{ $t('common.try_later') }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else class="flex justify-center">
                    <LoadingScreen />
                </div>


            </div>

            <!-- Pagination Container (Adoptīvs visiem ekrāniem) -->
            <div
                class="w-full p-4 border-t border-base-300 bg-base-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

                <!-- Limit + total + page info -->
                <div class="flex flex-col sm:flex-row sm:items-center sm:gap-6 w-full sm:w-auto">

                    <!-- Limit -->
                    <div class="flex flex-col sm:flex-row sm:items-center gap-2">
                        <label class="text-sm opacity-70">{{ $t('cabinet.admin.table_footer.limit') }}</label>
                        <select v-model.number="adminStore.meta.limit" @change="setNewLimit"
                            class="select select-bordered mt-1 sm:mt-0" :disabled="adminStore.searchMode === 'id'">
                            <option :value="5">5</option>
                            <option :value="10">10</option>
                            <option :value="20">20</option>
                            <option :value="50">50</option>
                        </select>
                    </div>

                    <!-- Total matches -->
                    <div class="text-sm opacity-80 whitespace-nowrap">
                        {{ $t('cabinet.admin.table_footer.total') }} <span class="font-semibold">{{ adminStore.meta.total_users }}</span>
                    </div>

                    <!-- Page info -->
                    <div class="text-sm opacity-80 whitespace-nowrap">
                        {{ $t('cabinet.admin.table_footer.page') }} <span class="font-semibold">{{ adminStore.meta.page }}</span> /
                        <span class="font-semibold">{{ adminStore.meta.total_pages }}</span>
                    </div>

                </div>

                <!-- Pagination buttons -->
                <div class="flex flex-col sm:flex-row sm:gap-3 gap-2 w-full sm:w-auto">
                    <button class="btn btn-neutral hover:btn-primary flex-1 p-2" :disabled="adminStore.meta.page === 1"
                        @click="adminStore.prevPage()">
                        <font-awesome-icon icon="fa-solid fa-arrow-left" />
                    </button>
                    <button class="btn btn-neutral hover:btn-primary flex-1 p-2"
                        :disabled="adminStore.meta.page === adminStore.meta.total_pages" @click="adminStore.nextPage()">
                        <font-awesome-icon icon="fa-solid fa-arrow-right" />
                    </button>
                </div>

            </div>


        </div>

        <!-- 3 modals -->

        <!-- Add role modal -->
        <BaseDialog v-model="addRoleModal" :title="$t('modals.add_role.title')" :cancel-text="$t('common.cancel')"
            :confirm-text="$t('common.confirm')" @confirm="addRole" @cancel="cancelAddRole">
            <div class="flex flex-col w-full gap-5">
                <Transition name="error-slide">
                    <div v-if="error" class="overflow-hidden">
                        <h1 class="text-red-500 mb-2">
                            {{ error }}
                        </h1>
                    </div>
                </Transition>
                <div class="flex flex-col gap-2 w-full">
                    <label class="label">
                        <span class="label-text">{{ $t('modals.add_role.label') }}</span>
                    </label>
                    <!-- dropdown list -->
                    <select v-model="selectedAddRole" class="select select-bordered w-full">
                        <option value=1>Admin</option>
                        <option value=2>User</option>
                        <option value=3>Developer</option>
                        <option value=4>Manager</option>
                        <option value=5>Support</option>
                        <option value=6>Content Manager</option>
                    </select>
                </div>
            </div>
        </BaseDialog>
        <!-- Remove role modal -->
        <BaseDialog v-model="removeRoleModal" :title="$t('modals.add_role.title')" :cancel-text="$t('common.cancel')"
            :confirm-text="$t('common.confirm')" @confirm="removeRole" @cancel="cancelRemoveRole">
            <div class="flex flex-col w-full gap-5">
                <Transition name="error-slide">
                    <div v-if="error" class="overflow-hidden">
                        <h1 class="text-red-500 mb-2">
                            {{ error }}
                        </h1>
                    </div>
                </Transition>
                <div class="flex flex-col gap-2 w-full">
                    <label class="label">
                        <span class="label-text">{{ $t('modals.remove_role.label') }}</span>
                    </label>
                    <!-- dropdown list -->
                    <select v-model="selectedRemoveRole" class="select select-bordered w-full">
                        <option value=1>Admin</option>
                        <option value=2>User</option>
                        <option value=3>Developer</option>
                        <option value=4>Manager</option>
                        <option value=5>Support</option>
                        <option value=6>Content Manager</option>
                    </select>
                </div>
            </div>
        </BaseDialog>
        <!-- Change activity modal -->
        <BaseDialog v-model="changeActivityModal" :title="$t('modals.change_activity.title')"
            :cancel-text="$t('common.cancel')" :confirm-text="$t('common.confirm')" @confirm="changeActivity"
            @cancel="cancelChangeActivity">
            <div class="flex flex-col w-full gap-5">
                <Transition name="error-slide">
                    <div v-if="error" class="overflow-hidden">
                        <h1 class="text-red-500 mb-2">
                            {{ error }}
                        </h1>
                    </div>
                </Transition>
                <div class="flex flex-col gap-2 w-full">
                    <label class="label">
                        <span class="label-text">{{ $t('modals.change_activity.label') }}</span>
                    </label>
                    <!-- dropdown list -->
                    <select v-model="selectedActivityStatus" class="select select-bordered w-full">
                        <option value="active">{{ $t('modals.change_activity.active') }}</option>
                        <option value="blocked">{{ $t('modals.change_activity.blocked') }}</option>
                    </select>
                </div>
            </div>
        </BaseDialog>
    </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';
import LoadingScreen from '@/components/common/LoadingScreen.vue';
import { useAdminStore } from '@/stores/admin';


export default {
    name: 'AdminPage',

    components: {
        BaseDialog,
        LoadingScreen
    },

    data() {
        return {
            addRoleModal: false,
            removeRoleModal: false,
            changeActivityModal: false,

            selectedAddRole: 2,
            selectedRemoveRole: 2,
            selectedActivityStatus: 'active',
            selectedPageSize: 10,

            selectedUserIds: [],
            selectAll: false,

            emptyError: ''
        }
    },

    computed: {
        adminStore() {
            return useAdminStore()
        },
        error() {
            return this.adminStore.error
        }
    },

    methods: {
        async setNewLimit() {
            await this.adminStore.setLimit(this.adminStore.meta.limit);
            await this.adminStore.refresh();
        },
        clearEmptyError() {
            this.emptyError = ''
        },
        async searchButton() {
            const store = this.adminStore;
            const query = store.searchQuery.toLowerCase();

            if (store.searchMode === 'all') {
                store.fetchUsers();
                store.clearSearch();
            } else if (store.searchMode === 'id') {

                if (query === '') {
                    this.emptyError = 'Tukšs ievades lauks!';
                    return;
                }

                const numericId = Number(query);

                if (!Number.isInteger(numericId)) {
                    this.emptyError = 'Invalid ID format'
                    return
                }


                await store.getUserById(numericId);
                this.emptyError = '';
            } else if (store.searchMode === 'username') {
                if (query === '') {
                    this.emptyError = 'Tukšs ievades lauks!';
                    return;
                }
                await store.getUserByNameEmail(query);
                this.emptyError = '';
            } else if (store.searchMode === 'role') {
                if (query === '') {
                    this.emptyError = 'Tukšs ievades lauks!';
                    return;
                }
                store.getUserByRole(query);
                this.emptyError = '';
            }
        },
        toggleSelectAll() {
            if (this.selectAll) {
                this.selectedUserIds = this.adminStore.users.map(user => user.id);
            } else {
                this.selectedUserIds = [];
            }
        },
        async addRole() {
            try {
                await this.adminStore.addRoleToSelectedUsers(this.selectedAddRole, this.selectedUserIds);
                this.addRoleModal = false;
                this.adminStore.error = '';
                this.selectedAddRole = 2;
                await this.adminStore.refresh();
            } catch (error) {
                console.error(error);
            }
        },
        cancelAddRole() {
            this.addRoleModal = false;
            this.adminStore.error = '';
            this.addRoleModal = false;
        },
        async removeRole() {
            try {
                await this.adminStore.removeRoleFromSelectedUsers(this.selectedRemoveRole, this.selectedUserIds);
                this.removeRoleModal = false;
                this.adminStore.error = '';
                this.selectedRemoveRole = 2;
                await this.adminStore.refresh();
            }
            catch (error) {
                console.error(error);
            }
        },
        cancelRemoveRole() {
            this.adminStore.error = '';
            this.selectedRemoveRole = 2;
            this.removeRoleModal = false;
        },
        async changeActivity() {
            try {
                await this.adminStore.updateUserActivity(this.selectedUserIds, this.selectedActivityStatus);
                this.changeActivityModal = false;
                this.adminStore.error = '';
                this.selectedActivityStatus = 'active';
                this.selectedRemoveRole = 2;
                await this.adminStore.refresh();
            }
            catch (error) {
                console.error(error);
            }
        },
        cancelChangeActivity() {
            this.adminStore.error = '';
            this.selectedActivityStatus = 'active';
            this.changeActivityModal = false;
        }
    },

    watch: {
        selectedUserIds(newVal) {
            this.selectAll = newVal.length === this.adminStore.users.length;
        },
        'adminStore.users'(newUsers) {
            this.selectedUserIds = [];
            this.selectAll = false;
        }
    },

    mounted() {
        this.adminStore.fetchUsers()
    }
}
</script>

<style scoped>
.error-slide-enter-active,
.error-slide-leave-active {
    transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
    max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
    opacity: 1;
    transform: translateY(0);
    max-height: 100px;
}
</style>