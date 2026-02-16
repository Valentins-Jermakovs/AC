<template>
    <!-- Instruction cards -->
    <div class="flex flex-col lg:flex-row p-5 gap-5">

        <div class="w-full lg:w-1/2 bg-base-300 min-h-50 p-6 lg:p-10 flex flex-col justify-around">
            <h1 class="text-2xl lg:text-3xl">Administratora panelis</h1>
            <p class="text-base lg:text-lg">
                Šajā sadaļā administrators var pārvaldīt lietotājus un to lomas,
                aktivitātes statusus utt.
            </p>
        </div>

        <div class="w-full lg:w-1/2 bg-base-200 min-h-50 p-6 lg:p-10 flex flex-col justify-center gap-3">
            <h2 class="text-lg lg:text-xl">Pieejamie režīmi:</h2>
            <ul class="list-disc pl-5 text-sm lg:text-base">
                <li>lietotāju atlase/meklēšana</li>
                <li>lietotāju lomu modificēšana</li>
                <li>aktivitātes statusa maiņa</li>
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
                        <input type="text" v-model="adminStore.searchQuery" placeholder="Meklējamie dati"
                            class="input input-bordered w-full"
                            :disabled="adminStore.searchMode === '' || adminStore.searchMode === 'all'" />
                        <button class="btn btn-primary" :class="adminStore.searchMode === '' ? 'btn-disabled' : ''"
                            @click="searchButton">Veikt pieprasījumu</button>
                    </div>
                    <!-- Search filter - dropdown list -->
                    <div class="flex p-4 items-center">
                        <select v-model="adminStore.searchMode" class="select select-bordered w-full lg:w-64">
                            <option disabled value="">Meklēšanas režīms</option>
                            <option value="all">Visi lietotāji</option>
                            <option value="id">Pēc ID</option>
                            <option value="username">Pēc lietotājvārda/e-pasta</option>
                            <option value="role">Pēc lomas</option>
                        </select>
                    </div>
                </div>
                <!-- Control buttons-->
                <div class="flex flex-col sm:flex-row flex-wrap gap-3 p-4 justify-center">

                    <button class="btn btn-neutral hover:btn-primary w-full sm:w-auto" @click="addRoleModal = true"
                        :class="selectedUserIds.length === 0 ? 'btn-disabled' : ''">
                        Pievienot lomu
                    </button>

                    <button class="btn btn-neutral hover:btn-primary w-full sm:w-auto" @click="removeRoleModal = true"
                        :class="selectedUserIds.length === 0 ? 'btn-disabled' : ''">
                        Dzēst lomu
                    </button>

                    <button class="btn btn-neutral hover:btn-primary w-full sm:w-auto"
                        @click="changeActivityModal = true" :class="selectedUserIds.length === 0 ? 'btn-disabled' : ''">
                        Bloķēt/atbloķēt
                    </button>

                </div>

            </div>
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
                            <th class="whitespace-nowrap">Lietotājs</th>
                            <th class="whitespace-nowrap max-w-50">E-pasts</th>
                            <th class="whitespace-nowrap max-w-45">Lomas</th>
                            <th class="whitespace-nowrap">Reģistrēts</th>
                            <th class="whitespace-nowrap">Statuss</th>
                        </tr>
                    </thead>

                    <tbody v-if="!adminStore.loading">
                        <tr v-for="user in adminStore.users" :key="user.id"
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
                                    <span v-for="role in user.roles" :key="role" class="badge badge-warning">{{ role
                                        }}</span>
                                </div>
                            </td>
                            <td class="whitespace-nowrap">{{ user.created_at }}</td>
                            <td class="whitespace-nowrap">
                                <span :class="user.active ? 'text-success' : 'text-error'">
                                    {{ user.active ? 'Aktīvs' : 'Bloķēts' }}
                                </span>
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
                    <div v-for="user in adminStore.users" :key="user.id"
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
                                <div class="opacity-60">Statuss</div>
                                <div :class="user.active ? 'text-success' : 'text-error'">
                                    {{ user.active ? 'Aktīvs' : 'Bloķēts' }}
                                </div>
                            </div>

                            <div class="col-span-2">
                                <div class="opacity-60 mb-1">Lomas</div>
                                <div class="flex flex-wrap gap-2">
                                    <span v-for="role in user.roles" :key="role" class="badge badge-warning">
                                        {{ role }}
                                    </span>
                                </div>
                            </div>

                            <div class="col-span-2">
                                <div class="opacity-60">Reģistrēts</div>
                                <div>{{ user.created_at }}</div>
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
                        <label class="text-sm opacity-70">Rādīt ierakstus:</label>
                        <select v-model.number="adminStore.meta.limit"
                            @change="adminStore.setLimit(adminStore.meta.limit)"
                            class="select select-bordered mt-1 sm:mt-0" :disabled="adminStore.searchMode === 'id'">
                            <option :value="5">5</option>
                            <option :value="10">10</option>
                            <option :value="20">20</option>
                            <option :value="50">50</option>
                        </select>
                    </div>

                    <!-- Total matches -->
                    <div class="text-sm opacity-80 whitespace-nowrap">
                        Sakritību skaits: <span class="font-semibold">{{ adminStore.meta.total_users }}</span>
                    </div>

                    <!-- Page info -->
                    <div class="text-sm opacity-80 whitespace-nowrap">
                        Lapa <span class="font-semibold">{{ adminStore.meta.page }}</span> /
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
        <BaseDialog v-model="addRoleModal" :title="'Pievienot lomu'" :cancel-text="$t('common.cancel')"
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
                        <span class="label-text">Lomas</span>
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
        <BaseDialog v-model="removeRoleModal" :title="'Dzēst lomu'" :cancel-text="$t('common.cancel')"
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
                        <span class="label-text">Lomas</span>
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
        <BaseDialog v-model="changeActivityModal" :title="'Mainīt aktivitātes statusu'"
            :cancel-text="$t('common.cancel')" :confirm-text="$t('common.confirm')" @confirm="changeActivity" @cancel="cancelChangeActivity">
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
                        <span class="label-text">Aktivitātes statuss</span>
                    </label>
                    <!-- dropdown list -->
                    <select v-model="selectedActivityStatus" class="select select-bordered w-full">
                        <option value="active">Aktīvs</option>
                        <option value="blocked">Bloķēts</option>
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
        searchButton() {
            const store = this.adminStore;
            const query = store.searchQuery.toLowerCase();

            if (store.searchMode === 'all') {
                store.fetchUsers();
                store.clearSearch();
            } else if (store.searchMode === 'id') {
                store.getUserById(query);
            } else if (store.searchMode === 'username') {
                store.getUserByNameEmail(query);
            } else if (store.searchMode === 'role') {
                store.getUserByRole(query);
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
                this.adminStore.error = '';
                this.selectedActivityStatus = 'active';
                this.selectedRemoveRole = 2;
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

<style scoped></style>