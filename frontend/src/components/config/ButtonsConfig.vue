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
                class="bg-black rounded-md p-2 text-sm w-full mt-3"
                v-model="config.text"
                placeholder="Pick one please..."
            />
        </label>
        <div class="mb-2 border-t border-[#333] pt-5">Choices</div>
        <ButtonItem
            v-for="(b, i) in config.buttons"
            :key="b.id"
            :button="b"
            @remove="removeChoice(i)"
        />
        <button
            class="border-dotted border-2 w-full rounded-md mt-5 pt-1 pb-1 text-[#ccc] hover:text-white"
            @click="addChoice"
        >
            + Add choice
        </button>
    </div>
</template>
