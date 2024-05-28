<script setup lang="ts">
const router = useRouter()

const nav = [
  { label: 'Home', to: '/' }
]
</script>

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <NuxtLayout dir="routing/pages" :nav="nav" current-route>
    <NuxtPage />
    <NuxtLoadingIndicator />
  </NuxtLayout>
</template>
