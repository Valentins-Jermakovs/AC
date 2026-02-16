<template>
    <!-- Instruction cards -->
    <div class="flex p-5">
        <div class="w-1/2 bg-base-300 h-52 p-10 flex flex-col items-start justify-around">
            <h1 class="text-3xl">Administratora panelis</h1>
            <p class="text-lg">
                Šajā sadaļā administrators var pārvaldīt lietotājus un to lomas, aktivitātes statusus, utt.
                Pirms veikt izmaiņas, pārdomājiet, vai tās ir nepeciešamas.
            </p>
        </div>
        <div class="w-1/2 bg-base-200 h-52 text-lg p-10 flex flex-col items-center justify-center gap-2">
            <h2>Pieejamie administratora paneļa režīmi:</h2>
            <ul class="list-disc">
                <li>
                    lietotāju atlase/meklēšana
                </li>
                <li>
                    lietotāju lomu modificēšana
                </li>
                <li>
                    lietotāju aktivitātes statusa maiņa
                </li>
            </ul>
        </div>
    </div>
    <!-- Admin panel -->
    <div class="px-5 pb-5">
        <div class="flex flex-col w-full bg-base-200 border border-base-300">
            <!-- Admin panel top (control elements) -->
            <div class="flex flex-1">
                <div class="flex-1 flex">
                    <!-- Search bar -->
                    <div class="flex flex-1 p-5 items-center justify-center">
                        <input type="text" v-model="adminStore.searchQuery" placeholder="Meklējamie dati"
                            class="input input-bordered w-full"
                            :disabled="adminStore.searchMode === '' || adminStore.searchMode === 'all'" />
                        <button class="btn btn-primary" :class="adminStore.searchMode === '' ? 'btn-disabled' : ''"
                            @click="searchButton">Meklēt</button>
                    </div>
                    <!-- Search filter - dropdown list -->
                    <div class="flex p-5 items-center justify-center">
                        <select v-model="adminStore.searchMode" class="select select-bordered w-full max-w-xs">
                            <option disabled value="">Meklēšanas režīms</option>
                            <option value="all">Visi lietotāji</option>
                            <option value="id">Pēc ID</option>
                            <option value="username">Pēc lietotājvārda/e-pasta</option>
                            <option value="role">Pēc lomas</option>
                        </select>
                    </div>
                </div>
                <!-- Control buttons-->
                <div class="flex p-5 items-center justify-center">
                    <button class="btn btn-neutral hover:btn-primary" @click="addRoleModal = true">Pievienot
                        lomu</button>
                    <button class="btn btn-neutral hover:btn-primary" @click="removeRoleModal = true">Dzēst
                        lomu</button>
                    <button class="btn btn-neutral hover:btn-primary"
                        @click="changeActivityModal = true">Bloķēt/atbloķēt</button>
                </div>
            </div>
            <!-- Admin panel table -->
            <div class="flex flex-1">
                <div class="flex-1 flex p-5 items-center justify-center">
                    <table class="table w-full">
                        <!-- Table header -->
                        <thead>
                            <tr>
                                <th>
                                    <label>
                                        <input type="checkbox" class="checkbox checkbox-neutral"
                                            v-model="selectAll" @change="toggleSelectAll" />
                                    </label>
                                </th>
                                <th>ID</th>
                                <th>Lietotājs</th>
                                <th>E-pasts</th>
                                <th>Lomas</th>
                                <th>Registrešanas datums</th>
                                <th>Aktivitātes statuss</th>
                            </tr>
                        </thead>
                        <!-- Table body with users -->
                        <tbody v-if="!adminStore.loading">
                            <tr v-for="user in adminStore.users" :key="user.id" :class="{'bg-base-300': selectedUserIds.includes(user.id)}">
                                <td>
                                    <label>
                                        <input type="checkbox" class="checkbox checkbox-neutral"
                                            v-model="selectedUserIds" :value="user.id" />
                                    </label>
                                </td>
                                <td>{{ user.id }}</td>
                                <td>{{ user.username }}</td>
                                <td>{{ user.email }}</td>
                                <td>
                                    <div class="flex gap-2 overflow-x-auto max-w-xs">
                                        <span v-for="role in user.roles" :key="role" class="badge badge-warning">
                                            {{ role }}
                                        </span>
                                    </div>
                                </td>
                                <td>{{ user.created_at }}</td>
                                <td>
                                    <span :class="user.active ? 'text-success' : 'text-error'">
                                        {{ user.active ? 'Aktīvs' : 'Bloķēts' }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>

                        <tbody v-else>
                            <tr>
                                <td colspan="7">
                                    <LoadingScreen></LoadingScreen>
                                </td>
                            </tr>
                        </tbody>
                        <!-- Table footer -->
                        <tfoot>
                            <tr>
                                <!-- dropdown list -->
                                <th>
                                    <select v-model.number="adminStore.meta.limit"
                                        @change="adminStore.setLimit(adminStore.meta.limit)"
                                        class="select select-bordered" :disabled="selectedSearchMode === 'id'">
                                        <option :value="5">5</option>
                                        <option :value="10">10</option>
                                        <option :value="20">20</option>
                                        <option :value="50">50</option>
                                    </select>
                                </th>
                                <th colspan="3"></th>
                                <th>
                                    Sakritību skaits: {{ adminStore.meta.total_users }}
                                </th>
                                <th>
                                    Lapa {{ adminStore.meta.page }} / {{ adminStore.meta.total_pages }}
                                </th>
                                <th>
                                    <div>
                                        <button class="btn btn-neutral hover:btn-primary"
                                            :disabled="adminStore.meta.page === 1" @click="adminStore.prevPage()">
                                            <font-awesome-icon icon="angle-left" />
                                        </button>
                                        <button class="btn btn-neutral hover:btn-primary"
                                            :disabled="adminStore.meta.page === adminStore.meta.total_pages"
                                            @click="adminStore.nextPage()">
                                            <font-awesome-icon icon="angle-right" />
                                        </button>
                                    </div>
                                </th>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </div>

        <!-- 3 modals -->

        <!-- Add role modal -->
        <BaseDialog v-model="addRoleModal" :title="'Pievienot lomu'" :cancel-text="$t('common.cancel')"
            :confirm-text="$t('common.confirm')">
            <div class="flex flex-col gap-2 w-full">
                <label class="label">
                    <span class="label-text">Lomas</span>
                </label>
                <!-- dropdown list -->
                <select v-model="selectedAddRole" class="select select-bordered w-full">
                    <option disabled value="">Izvēlies lomu</option>
                    <option value="admin">Admin</option>
                    <option value="user">User</option>
                    <option value="developer">Developer</option>
                    <option value="manager">Manager</option>
                    <option value="support">Support</option>
                    <option value="content_manager">Content Manager</option>
                </select>
            </div>
        </BaseDialog>
        <!-- Remove role modal -->
        <BaseDialog v-model="removeRoleModal" :title="'Dzēst lomu'" :cancel-text="$t('common.cancel')"
            :confirm-text="$t('common.confirm')">
            <div class="flex flex-col gap-2 w-full">
                <label class="label">
                    <span class="label-text">Lomas</span>
                </label>
                <!-- dropdown list -->
                <select v-model="selectedRemoveRole" class="select select-bordered w-full">
                    <option disabled value="">Izvēlies lomu</option>
                    <option value="admin">Admin</option>
                    <option value="user">User</option>
                    <option value="developer">Developer</option>
                    <option value="manager">Manager</option>
                    <option value="support">Support</option>
                    <option value="content_manager">Content Manager</option>
                </select>
            </div>
        </BaseDialog>
        <!-- Change activity modal -->
        <BaseDialog v-model="changeActivityModal" :title="'Mainīt aktivitātes statusu'"
            :cancel-text="$t('common.cancel')" :confirm-text="$t('common.confirm')">
            <div class="flex flex-col gap-2 w-full">
                <label class="label">
                    <span class="label-text">Aktivitātes statuss</span>
                </label>
                <!-- dropdown list -->
                <select v-model="selectedActivityStatus" class="select select-bordered w-full">
                    <option disabled value="">Izvēlies statusu</option>
                    <option value="active">Aktīvs</option>
                    <option value="blocked">Bloķēts</option>
                </select>
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

            selectedAddRole: '',
            selectedRemoveRole: '',
            selectedActivityStatus: '',
            selectedPageSize: 10,

            selectedUserIds: [],
            selectAll: false,
        }
    },

    computed: {
        adminStore() {
            return useAdminStore()
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