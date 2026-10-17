<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(defineProps<{
	icon: string
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
		class="text-icon-button"
		:href="props.href"
		:target="element === 'a' ? props.target : undefined"
		:rel="element === 'a' ? props.rel : undefined"
		:type="element === 'button' ? props.type : undefined"
		:disabled="element === 'button' ? props.disabled : undefined"
	>
		<img :src="props.icon" :alt="props.iconAlt" />
		<span><slot /></span>
	</component>
</template>

<style scoped>
.text-icon-button {
	all: unset;

	position: relative;
	display: flex;
	align-items: center;

	width: fit-content;

	box-sizing: border-box;
	padding: 0 35px;

	font-size: 16px;
	font-weight: 400;
	line-height: 1.25;

	color: var(--color-secondary-70);
	text-decoration: none;

	cursor: pointer;
}

.text-icon-button img {
	position: absolute;
	left: 0;
	top: 50%;

	width: auto;
	height: 15px;
	object-fit: contain;

	transform: translateY(-50%);
}

.text-icon-button span {
	display: block;
	will-change: transform, color;
	transition: transform 0.3s ease-out, color 0.3s ease-out;
}

.text-icon-button:hover span {
	color: rgba(255, 255, 255, 0.9);
	transform: translateY(-10%);
}

.text-icon-button:focus-visible {
	outline: 2px solid var(--color-secondary-60);
	outline-offset: 4px;
}

.text-icon-button:disabled {
	cursor: default;
	opacity: 0.48;
}

@media (max-width: 700px) {
	.text-icon-button {
		min-height: 44px;
		font-size: 14px;
	}
}
</style>
