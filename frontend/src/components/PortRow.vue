<script setup>
import { computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { useEditorStore } from '../stores/editor'

const props = defineProps({
  nodeId: { type: String, required: true },
  port: { type: Object, required: true }, // { id, label }
})

const store = useEditorStore()
// A port already has one arrow, so it doesn't offer "+" any more.
const connected = computed(() => store.hasEdge(props.nodeId, props.port.id))

const openPicker = (e) => store.openPicker({ nodeId: props.nodeId, port: props.port.id, x: e.clientX, y: e.clientY })
</script>

<template>
  <div class="port">
    <span>{{ port.label }}</span>

    <!-- "+" is its own button next to the handle, not part of it,
         because a click on the handle itself belongs to Vue Flow (drag to connect). -->
    <div v-if="!connected" class="plus-zone">
      <button class="plus nodrag" title="Add next node" @click.stop="openPicker">+</button>
    </div>

    <!-- The handle's id IS the port name sent to the backend. -->
    <Handle :id="port.id" type="source" :position="Position.Right" class="dot" />
  </div>
</template>

<style scoped>
.port {
  position: relative;
  display: flex;
  justify-content: flex-end;
  padding: 8px 16px;
  font-size: 13px;
  color: #ccc;
  border-top: 1px solid #333;
}
.dot { width: 12px; height: 12px; right: -9px; background: var(--c); border: 2px solid #232323; }

.plus-zone {
  position: absolute; right: -40px; top: 0; bottom: 0; width: 34px; /* touches the handle, so hover isn't lost */
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity 0.15s;
}
.port:hover .plus-zone { opacity: 1; }
.plus { width: 22px; height: 22px; border-radius: 50%; border: none; background: var(--c); color: #fff; line-height: 1; }
</style>
