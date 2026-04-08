<template>
  <div class="w-full border border-base-300 bg-base-200 p-2 sm:p-4">

    <div v-if="newsStore.news.length === 0"
      class="w-full flex flex-col items-center justify-center gap-3 p-6 border-2 border-dashed border-base-300 bg-base-100 rounded-lg animate-pulse">
      <font-awesome-icon icon="fa-solid fa-magnifying-glass" class="text-4xl text-error animate-bounce" />
      <p class="text-center text-base-content/70 font-medium">
        {{ $t('errors.news_not_found') }}
      </p>
    </div>

    <!-- Desktop table -->
    <div v-else class="hidden lg:block overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>{{ $t('common.created_at') }}</th>
            <th>{{ $t('common.title') }}</th>
            <th>{{ $t('common.content') }}</th>
            <th>{{ $t('common.actions') }}</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(row, index) in newsStore.news" :key="index">
            <td>{{ row.createdAt.split(' ')[0] }}</td>

            <td class="font-semibold">
              {{ row.title }}
            </td>

            <td class="max-w-md">
              {{ truncateContent(row.content, 100) }}
            </td>

            <td>
              <div class="flex gap-2">
                <button class="btn btn-sm btn-info" @click="selectNews(row)">
                  {{ $t('common.edit') }}
                </button>

                <button class="btn btn-sm btn-error" @click="openDelete(row.id)">
                  {{ $t('common.delete') }}
                </button>
              </div>
            </td>

          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile cards -->
    <div class="flex flex-col gap-3 lg:hidden">

      <div v-for="(row, index) in newsStore.news" :key="index"
        class="bg-base-100 border border-base-300 p-3 rounded-lg flex flex-col gap-2">

        <div class="text-xs opacity-70">
          {{ row.createdAt.split(' ')[0] }}
        </div>

        <div class="font-semibold text-lg">
          {{ row.title }}
        </div>

        <div class="text-sm opacity-80">
          {{ truncateContent(row.content, 120) }}
        </div>

        <div class="flex gap-2 pt-2">

          <button class="btn btn-sm btn-info flex-1" @click="selectNews(row)">
            {{ $t('common.edit') }}
          </button>

          <button class="btn btn-sm btn-error flex-1" @click="openDelete(row.id)">
            {{ $t('common.delete') }}
          </button>

        </div>

      </div>

    </div>

    <!-- Modal -->
    <BaseDialog :title="$t('news.editor.delete_modal.title')" :cancel-text="$t('common.cancel')"
      :confirm-text="$t('common.delete')" v-model="openDeleteModal" @confirm="deleteNews">
      <p>
        {{ $t('news.editor.delete_modal.content') }}
      </p>
    </BaseDialog>

  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useNewsStore } from '@/stores/news'

export default {
  name: 'NewsTable',
  components: { BaseDialog },
  data() {
    return {
      newsStore: useNewsStore(),
      openDeleteModal: false,
      deleteId: null,
    }
  },
  methods: {
    openDelete(row) {
      this.openDeleteModal = true
      this.deleteId = row
    },
    deleteNews() {
      this.newsStore.deleteNews(this.deleteId)
      this.openDeleteModal = false
    },
    selectNews(row) {
      this.newsStore.selectedNews = row
    },

    // -----------------------
    // truncate content and remove HTML tags
    // -----------------------
    truncateContent(content, length = 100) {
      const textOnly = content.replace(/<\/?[^>]+(>|$)/g, '') // no HTML
      if (textOnly.length <= length) return textOnly
      return textOnly.substring(0, length) + '...'
    },
  },
  mounted() {
    this.newsStore.getAllNews()
    this.newsStore.selectedNews = null
  },
}
</script>

<style scoped></style>
