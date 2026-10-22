<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(defineProps<{
    icon?: string
    iconAlt?: string
    href?: string
    target?: "_blank" | "_self" | "_parent" | "_top"
    rel?: string
    type?: "button" | "submit" | "reset"
    disabled?: boolean
}>(), {
    iconAlt: "",
    target: undefined,
    rel: undefined,
    type: "button",
    disabled: false,
    href: undefined,
})

const element = computed(() => props.href ? "a" : "button")
</script>

<template>
    <component
        :is="element"
        class="button-shifting-text-with-icon"
        :href="props.href"
        :target="element === 'a' ? props.target : undefined"
        :rel="element === 'a' ? props.rel : undefined"
        :type="element === 'button' ? props.type : undefined"
        :disabled="element === 'button' ? props.disabled : undefined"
    >
        <img v-if="props.icon" :src="props.icon" :alt="props.iconAlt"/>
        <span><slot/></span>
    </component>
</template>

<style scoped>
.button-shifting-text-with-icon {
    all: unset;

    position: relative;
    display: flex;
    align-items: center;

    box-sizing: border-box;
    padding: 0 35px;

    font-size: 16px;
    font-weight: 400;
    color: var(--color-secondary-70);
    text-decoration: none;
    cursor: pointer;

    width: auto;

    > img {
        position: absolute;
        height: 15px;

        left: 0;
        top: 50%;

        transform: translateY(-50%);
    }

    > span {
        display: inline-block;

        will-change: transform, color;
        transition: transform 0.3s ease-out, color 0.3s ease-out;
    }
}

.button-shifting-text-with-icon:hover > span {
    color: var(--color-secondary-90);
    transform: translateY(-2px);
}

.button-shifting-text-with-icon:focus-visible {
    outline: 2px solid var(--color-secondary-60);
    outline-offset: 4px;
}
</style>
