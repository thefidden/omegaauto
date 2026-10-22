<script setup lang="ts">

import BlockGlass from "../BlockGlass.vue";
import BlockGlassButton from "../BlockGlassButton.vue";
import { useRouter } from "vue-router";
import { useColorMode } from "@vueuse/core";
import { navigateToHash } from "../../utils/navigateToHash.ts";

import carSideView from "../../assets/webp/car-side-view-dark.webp";
import carSideViewLight from "../../assets/webp/car-side-view-light.webp";

import chinaMap from "../../assets/svg-light/china.svg";
import russiaMap from "../../assets/svg-light/russia.svg";
import lineGradient from "../../assets/svg-light/line-gradient.svg";

import chinaMapDark from "../../assets/svg-dark/china.svg";
import russiaMapDark from "../../assets/svg-dark/russia.svg";
import lineGradientDark from "../../assets/svg-dark/line-gradient.svg";

const router = useRouter()
const colorMode = useColorMode({
	modes: { dark: 'dark', light: 'light' }
})

const goToBrandSelection = () => navigateToHash(router, '#brand-selection')
</script>

<template>
	<div class="sector1">
		<img
			:src="colorMode === 'dark' ? carSideView : carSideViewLight"
			alt="Автомобиль, вид сбоку"
			class="carSideView"
		/>

		<div class="grid">
			<block-glass class="china">
				<img :src="colorMode === 'dark' ? chinaMap : chinaMapDark" alt="Китай" class="flag" />
			</block-glass>

			<block-glass class="russia">
				<img :src="colorMode === 'dark' ? russiaMap : russiaMapDark" alt="Россия" class="flag" />
			</block-glass>

			<block-glass class="import">
				<span>Импорт автомобилей</span>
				<span>из <b>Китая</b> в <b>Россию</b></span>
			</block-glass>

			<block-glass-button class="go-to-store" @click="goToBrandSelection()">
				<img :src="colorMode === 'dark' ? lineGradient : lineGradientDark" alt="" class="lineGradient" />
				Перейти к каталогу
				<img :src="colorMode === 'dark' ? lineGradient : lineGradientDark" alt="" class="lineGradient" />
			</block-glass-button>
		</div>
	</div>
</template>

<style scoped>
.sector1 {
	--safe-x: 24px;

	position: relative;

	display: flex;
	flex-direction: column;
	align-items: center;

	width: 100%;
	max-width: 100%;
	min-width: 0;
	height: auto;
	min-height: 800px;

	box-sizing: border-box;
	padding: 50px var(--safe-x) 40px;
	overflow: visible;
}

.grid {
	position: relative;
	z-index: 1;

	display: grid;
	grid-gap: 40px;
	grid-template-columns: 100px minmax(0, 1fr) 100px;
	grid-template-rows: auto auto;
	grid-template-areas:
        "china import russia"
        "store store store";

	width: 100%;
	max-width: 950px;
	min-width: 0;

	align-items: center;
	justify-items: center;
}

.grid .import {
	grid-area: import;
	width: 100%;
	min-width: 0;
	min-height: 120px;
	box-sizing: border-box;
	padding: 16px 20px;
}

.grid .go-to-store {
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;

	width: 100%;
	min-height: 72px;
	gap: clamp(16px, 4vw, 50px);

	grid-area: store;
	box-sizing: border-box;
	padding: 12px 16px;
}

.grid .go-to-store .lineGradient {
	display: block;
	width: auto;
	height: auto;
	max-width: min(120px, 18vw);
	max-height: 24px;
	object-fit: contain;
	opacity: 0.8;
}

.grid .go-to-store .lineGradient:last-child {
	rotate: 180deg;
}

.grid .china,
.grid .russia {
	width: 100px;
	height: 100px;
}

.grid .china { grid-area: china; }

.grid .russia { grid-area: russia; }

.flag {
	display: block;
	width: auto;
	height: auto;
	max-width: 68%;
	max-height: 68%;
	object-fit: contain;
}

.import {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	gap: 6px;

	color: var(--color-secondary-70);
	font-size: clamp(22px, 3.5vw, 40px);
	line-height: 1.15;
	text-align: center;
}

.import b {
	color: var(--color-secondary-90);
}

.go-to-store {
	color: var(--color-secondary-70);
	font-size: clamp(16px, 2vw, 20px);
	font-weight: 700;
	text-align: center;
}

.carSideView {
	position: absolute;
	z-index: 0;

	top: 224px;
	left: 50%;
	transform: translateX(-50%);

	display: block;
	width: auto;
	max-width: 95%;
	height: auto;
	object-fit: contain;
	pointer-events: none;
}

.go-to-store .lineGradient {
	will-change: transform, opacity;
	transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}

.go-to-store:hover .lineGradient:first-child,
.go-to-store:hover .lineGradient:last-child {
	opacity: 0;
	transform: translateX(-25px);
}

@media (max-width: 1100px) {
	.sector1 {
		--safe-x: 24px;
		min-height: 720px;
	}

	.grid {
		grid-gap: 24px;
		grid-template-columns: 80px minmax(0, 1fr) 80px;
	}

	.grid .china,
	.grid .russia {
		width: 80px;
		height: 80px;
	}

	.carSideView {
		max-width: min(95%, calc(100% - 48px));
	}
}

@media (max-width: 900px) {
	.sector1 {
		--safe-x: 16px;
		min-height: 680px;
		padding-top: 100px;
		padding-bottom: 28px;
	}

	.grid {
		grid-template-columns: 64px minmax(0, 1fr) 64px;
		column-gap: 16px;
		row-gap: 18px;
		width: 100%;
	}

	.grid .china,
	.grid .russia {
		width: 64px;
		height: 64px;
	}

	.grid .import {
		min-height: 0;
		padding: 14px 12px;
	}

	.import {
		font-size: clamp(18px, 5.2vw, 26px);
	}

	.grid .go-to-store {
		min-height: 56px;
		gap: 12px;
		font-size: 16px;
	}

	.carSideView {
		top: 360px;
		width: calc(100% - 32px);
		max-width: 560px;
		height: auto;
	}
}

@media (max-width: 700px) {
	.sector1 {
		--safe-x: 16px;
		min-height: 650px;
		padding-top: 96px;
	}

	.grid .go-to-store .lineGradient {
		max-width: min(68px, 18vw);
	}
}
</style>
