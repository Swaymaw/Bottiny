<script setup>
import ButtonItem from "./items/ButtonItem.vue";
import { uid } from "../../utils";

const props = defineProps({ config: { type: Object, required: true } });

const addChoice = () =>
    props.config.buttons.push({ id: uid("opt_"), label: "" });
const removeChoice = (i) => props.config.buttons.splice(i, 1);
</script>

<template>
    <div>
        <label class="block mb-2">
            Question
            <input
                class="bg-black rounded-md p-2 text-sm w-full"
                v-model="config.text"
                placeholder="Pick one please..."
            />
        </label>
        <hr class="border-t-4 border-dashed border-gray-300 mb-4" />
        <div class="mb-2">Choices</div>
        <ButtonItem
            v-for="(b, i) in config.buttons"
            :key="b.id"
            :button="b"
            @remove="removeChoice(i)"
        />
        <button
            class="border-dotted border-2 w-full rounded-md mt-5"
            @click="addChoice"
        >
            + Add choice
        </button>
    </div>
</template>
