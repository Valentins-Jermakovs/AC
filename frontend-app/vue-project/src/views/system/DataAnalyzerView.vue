<template>
  <PageHeader :title="title" :imageUrl="image"></PageHeader>
  <NavigationPanel :buttons="navButtons" v-model="activePage"></NavigationPanel>
  <ExpensesPage v-if="activePage === 'expenses'"></ExpensesPage>
  <BudgetPage v-if="activePage === 'budget'"></BudgetPage>
  <PaymentPage v-if="activePage === 'payments'"></PaymentPage>
</template>

<script>
import PageHeader from '@/components/ui/PageHeader.vue'
import headerImage from '@/assets/images/arturo-anez-RxbkUG80Rag-unsplash.jpg'
import NavigationPanel from '@/components/ui/NavigationPanel.vue'
import ExpensesPage from '@/components/system/analytics/ExpensesPage.vue'
import BudgetPage from '@/components/system/analytics/BudgetPage.vue'
import PaymentPage from '@/components/system/analytics/PaymentPage.vue'


export default {
  name: 'DataAnalyzerView',
  components: {
    PageHeader,
    NavigationPanel,
    ExpensesPage,
    BudgetPage,
    PaymentPage,
  },
  data() {
    return {
      image: headerImage,

      // Currently active page (default is private tasks)
      activePage: 'expenses',
    }
  },
  computed: {
    navButtons() {
      let navButtons = [
        {
          key: 'expenses',
          title: this.$t('finances.titles.expenses'),
        },
        {
          key: 'budget',
          title: this.$t('finances.titles.budget'),
        },
        {
          key: 'payments',
          title: this.$t('finances.titles.payments'),
        },
      ]

      return navButtons
    },
    title() {
      return this.$t('finances.title')
    },
  },
}
</script>

<style scoped></style>
