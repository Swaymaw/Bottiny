<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";
import { useFlowsStore } from "../stores/flows";

const flows = useFlowsStore();

onMounted(flows.fetch);
</script>

<template>
    <div class="flex h-screen bg-gray-800">
        <aside class="w-64 px-5 py-7 shrink-0">
            <h2 class="mb-5 text-xl font-semibold text-white">Flows</h2>

            <RouterLink
                :to="{ name: 'editor' }"
                class="block w-full rounded-xl border-4 pt-1 pb-1 pl-3 text-zinc-300 hover:text-white"
            >
                + New flow
            </RouterLink>
            <div class="mt-10 rounded-lg border-4 border-white min-h-3/4">
                <div
                    v-for="flow in flows.items"
                    :key="flow.name"
                    class="items-start"
                >
                    <RouterLink
                        :to="{
                            name: 'editor',
                            params: { name: flow.name },
                        }"
                        exact-active-class="text-white"
                        class="py-1.5 text-zinc-400 transition-colors hover:text-white"
                    >
                        <div class="items-center m-4 flex justify-between">
                            {{ flow.name }}

                            <input
                                type="checkbox"
                                :checked="flow.enabled"
                                title="Enabled"
                                @change="flows.toggle(flow)"
                            />
                        </div>
                    </RouterLink>
                </div>
            </div>
        </aside>

        <main class="min-w-0 flex-1">
            <RouterView />
        </main>
    </div>
</template>
