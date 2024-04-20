<script setup lang="ts">
const router = useRouter()

const nav = [
  { label: 'Home', to: '/' }
]
</script>

<template>
  <NuxtLayout dir="routing/pages" :nav="nav" current-route>
    <NuxtPage />
    <NuxtLoadingIndicator />
  </NuxtLayout>
</template>
