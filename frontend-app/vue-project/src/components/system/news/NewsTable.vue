<template>
  <div class="w-full border border-base-300 bg-base-200 p-4">
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
          <td>{{ row.title }}</td>
          <td>
            <div>{{ truncateContent(row.content, 100) }}</div>
          </td>

          <td class="flex gap-2">
            <button class="btn btn-sm btn-info" @click="selectNews(row)">
              {{ $t('common.edit') }}
            </button>
            <button class="btn btn-sm btn-error" @click="openDelete(row.id)">
              {{ $t('common.delete') }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Remove News Modal -->
    <BaseDialog
      :title="$t('news.editor.delete_modal.title')"
      :cancel-text="$t('common.cancel')"
      :confirm-text="$t('common.delete')"
      v-model="openDeleteModal"
      @confirm="deleteNews"
    >
      <p>{{ $t('news.editor.delete_modal.content') }}</p>
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
