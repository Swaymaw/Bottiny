<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";
import { useFlowsStore } from "../stores/flows";

const flows = useFlowsStore();

onMounted(flows.fetch);
</script>

<template>
    <div class="grid h-full grid-cols-[220px_1fr] bg-gray-800">
        <aside class="overflow-y-auto px-5 py-7">
            <h2 class="mb-5 text-xl font-semibold text-white">Flows</h2>

            <RouterLink
                :to="{ name: 'editor' }"
                class="block w-full rounded-xl border-4 pt-1 pb-1 pl-3 text-zinc-300 hover:text-white"
            >
                + New flow
            </RouterLink>

            <div
                v-for="flow in flows.items"
                :key="flow.name"
                class="mt-10 flex items-center justify-between"
            >
                <RouterLink
                    :to="{
                        name: 'editor',
                        params: { name: flow.name },
                    }"
                    exact-active-class="text-white"
                    class="block py-1.5 text-zinc-400 transition-colors hover:text-white"
                >
                    {{ flow.name }}
                </RouterLink>

                <input
                    type="checkbox"
                    :checked="flow.enabled"
                    title="Enabled"
                    @change="flows.toggle(flow)"
                />
            </div>
        </aside>

        <main class="h-full py-8 pr-8">
            <RouterView />
        </main>
    </div>
</template>
