<template>
  <!-- Render the router view -->
  <router-view></router-view>
</template>

<script setup>
import { useDocumentTitle } from './utils/useDocumentTitle';
useDocumentTitle();
</script>

<style scoped></style>
