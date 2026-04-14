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
      title: 'Data Analyzer',
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
          title: 'Expenses',
        },
        {
          key: 'budget',
          title: 'Budget',
        },
        {
          key: 'payments',
          title: 'Payments',
        },
      ]

      return navButtons
    },
  },
}
</script>

<style scoped></style>
