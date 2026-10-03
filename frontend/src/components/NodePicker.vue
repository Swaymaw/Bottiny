<script setup>
import { NODE_TYPES } from '../nodeTypes'

const props = defineProps({ x: Number, y: Number })
const emit = defineEmits(['pick', 'close'])

// keep the menu on screen when opened near the bottom or right edge
const left = Math.min(props.x, window.innerWidth - 190)
const top = Math.min(props.y, window.innerHeight - 190)
</script>

<template>
  <!-- the backdrop catches any click outside the menu and closes it -->
  <div class="backdrop" @click="emit('close')" />
  <ul class="picker" :style="{ left: left + 'px', top: top + 'px' }">
    <li v-for="(def, type) in NODE_TYPES" :key="type" @click="emit('pick', type)">
      <span class="swatch" :style="{ background: def.color }" />
      {{ def.label }}
    </li>
  </ul>
</template>

<style scoped>
.backdrop { position: fixed; inset: 0; z-index: 99; }
.picker {
  position: fixed; z-index: 100; margin: 0; padding: 6px; list-style: none; min-width: 170px;
  background: #1c1c1c; border: 1px solid #444; border-radius: 12px; box-shadow: 0 8px 24px #000a;
}
li { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; cursor: pointer; }
li:hover { background: #333; }
.swatch { width: 12px; height: 12px; border-radius: 50%; }
</style>
