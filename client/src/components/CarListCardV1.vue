<script setup lang="ts">

import BlockGlassButton from "./BlockGlassButton.vue";
import type { Car } from "../interfaces/Car.ts";
import { computed } from "vue";
import { useColorMode } from "@vueuse/core";
import { getBrandLogoHref } from "../utils/brandLogos.ts";

const colorMode = useColorMode({
	modes: { dark: 'dark', light: 'light' }
})

const props = defineProps<Car>()

const priceFormatted = computed(() =>
	new Intl.NumberFormat("ru-RU").format(Number(props.price_total_rub))
)

const brandLogoHref = computed(() =>
	getBrandLogoHref(props.brand, colorMode.value === 'dark')
)
</script>

<template>
	<block-glass-button class="card">
		<div class="image-frame">
			<img :src="props.images.find(image => image.index === 0)?.image" alt="car picture" />
		</div>

		<div class="info">
			<span class="name label" style="grid-area: name">{{ props.brand + ' ' + props.model }}</span>

			<span class="year label" style="grid-area: year-l">Год</span>
			<span class="mileage label" style="grid-area: mileage-l">Пробег</span>
			<span class="power label" style="grid-area: power-l">Мощность</span>
			<span class="displacement label" style="grid-area: displacement-l">Объем</span>
			<span class="fuel label" style="grid-area: fuel-l">Топливо</span>
			<span class="gear label" style="grid-area: gear-l">Коробка</span>
			<span class="color label" style="grid-area: color-l">Цвет</span>
			<span class="price label" style="grid-area: price-l">Цена</span>

			<span class="year value" style="grid-area: year-v">{{ props.year }}</span>
			<span class="mileage value" style="grid-area: mileage-v">{{ props.mileage }} км</span>
			<span class="power value" style="grid-area: power-v">{{ props.power }} л.с.</span>
			<span class="displacement value" style="grid-area: displacement-v">{{ props.displacement }} л</span>
			<span class="fuel value" style="grid-area: fuel-v">{{ props.fuel }}</span>
			<span class="gear value" style="grid-area: gear-v">{{ props.gear }}</span>
			<span class="color value" style="grid-area: color-v">{{ props.color }}</span>
			<span class="price value" style="grid-area: price-v">{{ priceFormatted }} ₽</span>
		</div>

		<div class="brand-logo__container">
			<img class="brand-logo__img"
				 :src="brandLogoHref"
				 :alt="`${props.brand} logo`"
			/>
		</div>
	</block-glass-button>
</template>

<style scoped>
.brand-logo__container {
	position: absolute;

	width: 100%;
	height: 100%;

	box-sizing: border-box;
	border-radius: inherit;

	inset: 0;

	overflow: hidden;
	pointer-events: none;
}

.brand-logo__img {
	position: absolute;

	filter: blur(7px);
	opacity: .2;

	width: min(400px, 100%);
	height: auto;

	right: 0;
	bottom: 0;
	transform: translateX(25%) translateY(25%);
	transform-origin: right bottom;

	transition: filter .3s ease-out;
}

.card:hover .brand-logo__img {
	filter: blur(10px);
}

.card:hover .image-frame img {
	scale: 1.1;
}

.card {
	display: flex;
	flex-direction: row;

	box-sizing: border-box;
	padding: 30px;

	gap: 30px;

	width: min(1500px, calc(100vw - 48px));
	height: 300px;
}

.image-frame {
	flex: 0 0 330px;
	height: 100%;
	width: 330px;

	border-radius: 30px;
	overflow: hidden;
}

.image-frame img {
	width: 100%;
	height: 100%;
	object-fit: cover;

	transition: scale .3s ease-out;
}

.info {
	display: grid;
	grid-template-areas:
        "name name name name name name name"
        "year-l mileage-l power-l displacement-l fuel-l gear-l color-l"
        "year-v mileage-v power-v displacement-v fuel-v gear-v color-v"
        "price-l price-v price-v price-v price-v price-v price-v";
	grid-template-rows: repeat(4, 1fr);
	grid-template-columns: repeat(7, 1fr);

	width: 100%;
	min-width: 0;
	height: 100%;
}

.value {
	font-size: 24px;
	font-weight: 300;
	color: var(--color-secondary-70);
}

.label {
	font-size: 24px;
	font-weight: 700;
	color: var(--color-secondary-70);
}

.name {
	color: var(--color-secondary-90);
}

@media (max-width: 1250px) {
	.card {
		height: 340px;
		padding: 24px;
		gap: 24px;
	}

	.image-frame {
		flex-basis: 300px;
		width: 300px;
	}

	.info {
		grid-template-areas:
            "name name name name"
            "year-l mileage-l power-l displacement-l"
            "year-v mileage-v power-v displacement-v"
            "fuel-l gear-l color-l price-l"
            "fuel-v gear-v color-v price-v";
		grid-template-columns: repeat(4, minmax(0, 1fr));
		grid-template-rows: repeat(5, 1fr);
		column-gap: 12px;
	}

	.value, .label { font-size: 19px; }
}

@media (max-width: 900px) {
	.card {
		flex-direction: column;
		width: calc(100vw - 32px);
		height: auto;
		padding: 16px;
		gap: 18px;
		background-color: var(--color-primary-20);
	}

	.image-frame {
		flex: none;
		width: 100%;
		height: auto;
		aspect-ratio: 16 / 9;
	}

	.info {
		grid-template-areas:
            "name name"
            "year-l mileage-l"
            "year-v mileage-v"
            "power-l displacement-l"
            "power-v displacement-v"
            "fuel-l gear-l"
            "fuel-v gear-v"
            "color-l price-l"
            "color-v price-v";
		grid-template-columns: repeat(2, minmax(0, 1fr));
		grid-template-rows: repeat(9, auto);
		gap: 6px 16px;
	}

	.value, .label {
		min-width: 0;
		overflow-wrap: anywhere;
		font-size: clamp(14px, 4vw, 18px);
		color: var(--color-secondary-90);
	}

	.value { margin-bottom: 10px; }

	.name { margin-bottom: 10px; font-size: clamp(19px, 5.5vw, 24px); }
}
</style>
