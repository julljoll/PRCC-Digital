<template>
  <div :class="[$dark ? 'dark' : '', 'min-h-screen transition-colors duration-300']">
    <div class="p-8 text-center bg-white dark:bg-slate-900 dark:text-white min-h-screen flex flex-col items-center justify-center">
      <button
        @click="toggleDark"
        class="mb-8 px-4 py-2 rounded bg-slate-800 text-white dark:bg-slate-200 dark:text-slate-900 shadow hover:scale-105 transition-transform"
      >
        Cambiar a modo {{ $dark ? 'claro' : 'oscuro' }}
      </button>
      <h1 class="text-3xl font-bold mb-4">¡Proyecto migrado a Vue!</h1>
      <p class="text-lg">Bienvenido a tu nueva app con Vite + Vue + Tailwind.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
const $dark = ref(false);

onMounted(() => {
  $dark.value = document.documentElement.classList.contains('dark');
});

function toggleDark() {
  $dark.value = !$dark.value;
  if ($dark.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}
</script>

<style scoped>
</style>
