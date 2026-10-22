<script setup lang="ts">

import BlockGlassButton from "./BlockGlassButton.vue";
import type { Car } from "../interfaces/Car.ts";
import { computed } from "vue";
import { useColorMode } from "@vueuse/core";

const colorMode = useColorMode({
	modes: { dark: 'dark', light: 'light' }
})

const props = defineProps<Car>()

const priceFormatted = computed(() =>
	new Intl.NumberFormat("ru-RU").format(Number(props.price_total_rub))
)

const getBrandLogoHref = (brand: string): string => {
	const extension = brand.toLowerCase() === "great wall" ? "png" : "svg"
	return new URL(
		colorMode.value === 'dark'
			? `../assets/car-logos-light/${ brand.toLowerCase() }.${ extension }`
			: `../assets/car-logos-dark/${ brand.toLowerCase() }.${ extension }`,
		import.meta.url
	).href
}
</script>

<template>
	<block-glass-button class="card">
		<div class="image-frame">
			<img :src="props.images.find(image => image.index === 0)?.image" alt="car picture" />
		</div>

		<div class="info">
			<span class="name" style="grid-area: name"><b>{{ props.brand + ' ' + props.model }}</b></span>

			<text class="year" style="grid-area: year">
				<span><b>Год</b></span>
				<span>{{ props.year }}</span>
			</text>

			<text class="mileage" style="grid-area: mileage">
				<span><b>Пробег</b></span>
				<span>{{ props.mileage }} км</span>
			</text>

			<text class="power" style="grid-area: power">
				<span><b>Мощность</b></span>
				<span>{{ props.power }} л.с.</span>
			</text>

			<text class="displacement" style="grid-area: displacement">
				<span><b>Объем</b></span>
				<span>{{ props.displacement }} л</span>
			</text>

			<text class="fuel" style="grid-area: fuel">
				<span><b>Топливо</b></span>
				<span>{{ props.fuel }}</span>
			</text>

			<text class="gear" style="grid-area: gear">
				<span><b>Трансмиссия</b></span>
				<span>{{ props.gear }}</span>
			</text>

			<text class="color" style="grid-area: color">
				<span><b>Цвет</b></span>
				<span>{{ props.color }}</span>
			</text>

			<span class="price" style="grid-area: price"><b>{{ priceFormatted }} ₽</b></span>
		</div>

		<div class="brand-logo__container">
			<img class="brand-logo__img"
				 :src="getBrandLogoHref(props.brand)"
				 :alt="`${props.brand} logo`"
			/>
		</div>
	</block-glass-button>
</template>

<style scoped>
.card {
	display: flex;
	flex-direction: row;
	align-items: stretch;

	background-color: var(--color-primary-30);

	box-sizing: border-box;
	padding: 30px;
	gap: 30px;

	width: 100%;
	max-width: min(1000px, 100%);
	height: 300px;
	min-width: 0;
}

.image-frame {
	flex: 0 1 500px;
	width: 500px;
	max-width: 100%;
	min-width: 0;
	height: 100%;

	border-radius: 30px;
	overflow: hidden;
}

.image-frame img {
	display: block;
	width: 100%;
	height: 100%;

	object-fit: cover;
	object-position: center;

	will-change: scale;
	transition: scale .3s ease-out;
}

.info {
	display: grid;
	grid-template-areas:
		"name name name name"
		"year power fuel color"
		"mileage displacement gear ."
		"price price price price";
	grid-template-rows: 1fr 2fr 2fr 1fr;
	grid-template-columns: repeat(4, minmax(0, 1fr));

	width: 100%;
	min-width: 0;
	height: 100%;
}

.year, .power, .fuel, .color, .mileage, .displacement, .gear {
	display: flex;
	flex-direction: column;
	color: var(--color-secondary-70);
	align-content: center;
	min-width: 0;
	overflow-wrap: anywhere;
}

.name {
	color: var(--color-secondary);
	align-content: start;
	font-size: 24px;
	min-width: 0;
	overflow-wrap: anywhere;
}

.price {
	color: var(--color-secondary);
	align-content: end;
	font-size: 24px;
}

.brand-logo__container {
	position: absolute;
	inset: 0;

	width: 100%;
	height: 100%;

	box-sizing: border-box;
	border-radius: inherit;

	overflow: hidden;
	pointer-events: none;
}

.brand-logo__img {
	position: absolute;

	filter: blur(7px);
	opacity: .2;

	width: min(300px, 45%);
	height: auto;
	object-fit: contain;

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
	scale: 1.05;
}

@media (max-width: 1100px) {
	.card {
		flex-direction: column;
		height: auto;
		padding: 20px;
		gap: 18px;
	}

	.image-frame {
		flex: none;
		width: 100%;
		height: auto;
	}

	.image-frame img {
		width: 100%;
		height: auto;
		object-fit: contain;
	}

	.info {
		grid-template-areas:
			"name name"
			"year power"
			"mileage displacement"
			"fuel gear"
			"color ."
			"price price";
		grid-template-columns: repeat(2, minmax(0, 1fr));
		grid-template-rows: auto;
		gap: 10px 14px;
		height: auto;
	}

	.name,
	.price {
		font-size: clamp(16px, 4.2vw, 20px);
	}

	.brand-logo__img {
		width: min(160px, 40%);
	}
}

@media (max-width: 700px) {
	.card {
		padding: 14px;
		gap: 14px;
	}

	.year, .power, .fuel, .color, .mileage, .displacement, .gear {
		font-size: 13px;
	}
}
</style>
