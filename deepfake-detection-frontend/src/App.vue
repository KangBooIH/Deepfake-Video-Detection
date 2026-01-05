<script setup>
  import Home from './components/Home.vue'
  import navbar from './components/navbar.vue';
</script>

<template>
  <navbar></navbar>
  <!-- <Home></Home> -->
  <!-- <p><strong>Current route path:</strong> {{ $route.fullPath }}</p> -->
  <main>
    <RouterView v-slot="{Component}">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>

  </main>
</template>

<style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: 550ms ease all;
  }

  .fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(60px);
  }

</style>
