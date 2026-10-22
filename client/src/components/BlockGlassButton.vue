<script setup lang="ts">

</script>

<template>
	<button type="button" class="block-glass-button">
		<slot />
	</button>
</template>

<style scoped>
.block-glass-button {
	--background-color: #00000000;

	position: relative;

	display: flex;
	align-items: center;
	justify-content: center;

	border-radius: 30px;
	border: 0;
	margin: 0;
	padding: 0;
	appearance: none;
	color: inherit;
	font: inherit;
	text-align: inherit;

	isolation: isolate;
	background-color: transparent;

	backdrop-filter: blur(13px);
}

.block-glass-button::before {
	content: "";

	position: absolute;
	inset: 0;

	border-radius: inherit;

	background-color: var(--background-color);
	border: 1px solid var(--color-secondary-50);

	box-shadow: inset 0 0 10px 1px var(--color-secondary-20);

	transition: background-color 0.3s ease-out;
	will-change: background-color;

	pointer-events: none;
	z-index: -1;
}

.block-glass-button::after {
	content: "";

	position: absolute;
	inset: 0;

	border-radius: inherit;

	box-shadow: 0 0 5px 1px var(--color-secondary-10);
	mix-blend-mode: darken;

	pointer-events: none;
	z-index: -2;
}

.block-glass-button:hover {
	cursor: pointer;
}

.block-glass-button:hover::before {
	background-color: var(--color-secondary-7);
}

.block-glass-button:focus-visible {
	outline: 2px solid var(--color-secondary-70);
	outline-offset: 4px;
}

.block-glass-button:disabled {
	cursor: default;
	opacity: 0.48;
}

.block-glass-button:disabled:hover::before {
	background: linear-gradient(135deg, var(--color-secondary-10), var(--color-secondary-5)),
	var(--background-color);
}

@media (max-width: 1250px) {
	.block-glass-button {
		background-color: var(--color-primary-60);
	}
}

@media (max-width: 900px) {
	.block-glass-button {
		--background-color: var(--color-secondary-7);
		background-color: var(--color-primary-20);
	}

	.block-glass-button::before {
		background: linear-gradient(135deg, var(--color-secondary-10), var(--color-secondary-5)),
		var(--background-color);
		border-color: var(--color-secondary-50);
		box-shadow: inset 0 1px 1px var(--color-secondary-20), inset 0 0 18px var(--color-secondary-10);
		mix-blend-mode: normal;
	}

	.block-glass-button::after {
		box-shadow: 0 12px 30px var(--color-primary-20), 0 0 20px var(--color-secondary-20);
		mix-blend-mode: normal;
	}
}
</style>
