<script setup lang="ts">

import BlockGlass from "../BlockGlass.vue";
import { computed, ref } from "vue";
import BlockGlassButton from "../BlockGlassButton.vue";
import { storeToRefs } from "pinia";
import { useStore } from "../../stores/Store.ts";
import LoadingAnimation from "../LoadingAnimation.vue";
import { useCarListFilters } from "../../stores/CarListFiltersStore.ts";
import { useColorMode } from "@vueuse/core";
import { getBrandLogoHref } from "../../utils/brandLogos.ts";

import Arrow from "../../assets/svg-light/arrow.svg"
import ArrowDark from "../../assets/svg-dark/arrow.svg"

const colorMode = useColorMode({
	modes: { dark: 'dark', light: 'light' }
})

const store = useStore()
const { brands, brandsLoading } = storeToRefs(store)

const carListFilterSetStore = useCarListFilters()
const { apply: applyFilterSet, reset: flushFilterSet } = carListFilterSetStore

const brandsPerPage = 10
const brandListPage = ref(0)
const brandListPages = computed(() => Math.floor(brands.value.length / brandsPerPage) + 1)

const brandLogo = (brand: string) => getBrandLogoHref(brand, colorMode.value === 'dark')

const goToBrand = (brand: string) => {
	flushFilterSet()
	carListFilterSetStore.brand = brand
	applyFilterSet()
}
</script>

<template>
	<div class="sector4">
		<block-glass class="cell heading">
			Выберите марку автомобиля
		</block-glass>

		<div class="cars">
			<LoadingAnimation v-if="brandsLoading" contained class="brands-loading" />

			<template v-else>
				<Transition name="brand-button__transition" mode="out-in">
					<div :key="brandListPage" class="brand-page">
						<block-glass-button
							v-for="brand in brands.slice(brandListPage * brandsPerPage, (brandListPage + 1) * brandsPerPage)"
							:key="brand"
							@click="goToBrand(brand)"
							class="cell car"
						>
							{{ brand }}
							<div class="image-frame">
								<img :src="brandLogo(brand)" :alt="`${brand} logo`" />
							</div>

							<div class="brand-logo__blurred__container">
								<img class="brand-logo__blurred__img"
									 :src="brandLogo(brand)"
									 :alt="`${brand} logo`"
								/>
							</div>
						</block-glass-button>
					</div>
				</Transition>

				<div class="cell navigation">
					<block-glass-button class="cell button prev"
										@click="brandListPage = Math.max(0, brandListPage - 1)"
										:style="{
											borderRadius: 100,
											opacity: brandListPage === 0 ? .5 : 1,
											cursor: brandListPage === 0  ? 'auto' : 'pointer'
										}"
					>
						<img :src="colorMode === 'dark' ? Arrow : ArrowDark" alt="Arrow" />
					</block-glass-button>

					<block-glass class="page">
						Страница {{ brandListPage + 1 }} из {{ brandListPages }}
					</block-glass>

					<block-glass-button class="cell button next"
										@click="brandListPage = Math.min(brandListPage + 1, brandListPages - 1)"
										:style="{
											borderRadius: 100,
											opacity: brandListPage === brandListPages - 1 ? .5 : 1,
											cursor: brandListPage === brandListPages - 1  ? 'auto' : 'pointer'
										}"
					>
						<img :src="colorMode === 'dark' ? Arrow : ArrowDark" alt="Arrow" />
					</block-glass-button>
				</div>
			</template>
		</div>
	</div>
</template>

<style scoped>
.sector4 {
	position: relative;
	isolation: isolate;

	display: flex;
	flex-direction: column;
	align-items: center;

	gap: 48px;

	width: 100%;
	max-width: 100%;
	min-width: 0;
	box-sizing: border-box;
	padding-inline: 24px;
}

.cars {
	display: grid;
	grid-template-rows: repeat(3, 120px);
	grid-template-columns: repeat(4, minmax(0, 350px));

	column-gap: 24px;
	row-gap: 40px;

	width: 100%;
	justify-content: space-between;
	justify-items: center;
}

.brands-loading {
	grid-column: 1 / -1;
	grid-row: 1 / -1;

	width: 100%;
	height: 100%;
}

.brand-page {
	display: grid;
	grid-column: 1 / -1;
	grid-row: 1 / 3;
	grid-template-columns: repeat(4, minmax(0, 350px));
	grid-template-rows: repeat(2, 120px);
	column-gap: 24px;
	row-gap: 40px;
	width: 100%;
	justify-content: space-between;
	justify-items: center;
}

.cell {
	width: 100%;
	height: 120px;

	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;

	box-sizing: border-box;
	padding: 30px;

	color: var(--color-secondary-90);
	font-size: 24px;
	font-weight: 700;
}

.heading {
	font-size: 40px;

	display: flex;
	align-items: center;
	justify-content: center;

	width: 750px;
	height: 120px;
}

.car .image-frame {
	position: relative;
	flex: 0 0 auto;
	width: min(100px, 28%);
	height: auto;
	max-height: 50px;

	display: flex;
	flex-direction: row;
	justify-content: end;
	align-items: center;
}

.car .image-frame img {
	display: block;
	width: auto;
	height: auto;
	max-width: 100%;
	max-height: 50px;
	object-fit: contain;
}

.car .brand-logo__blurred__img {
	width: auto;
	height: auto;
	max-width: 120px;
	object-fit: contain;
}

.navigation {
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;

	gap: 50px;

	grid-row: 3;
	grid-column: 3 / 5;

	width: 100%;

	padding: 0;
}

.button {
	flex: 0 0 120px;
	width: 120px;
	height: 120px;
	aspect-ratio: 1;
	border-radius: 50% !important;
	padding: 30px;
}

.button img {
	display: block;
	width: 100%;
	height: 100%;
	object-fit: contain;
}

.button.next img {
	rotate: 180deg;
}

.page {
	min-width: 0;
	height: 100%;
	width: 100%;

	border-radius: 100px;
	text-align: center;

	user-select: none;
}

.brand-logo__blurred__container {
	position: absolute;

	top: 0;
	left: 0;

	width: 100%;
	height: 100%;

	box-sizing: border-box;
	border-radius: inherit;

	overflow: hidden;
}

.brand-logo__blurred__img {
	position: absolute;

	filter: blur(2px);
	opacity: 0;
	scale: 3;

	top: 50%;
	right: 0;

	translate: 0 -50%;
}

@media (max-width: 1100px) {
	.sector4 {
		padding-inline: 24px;
		box-sizing: border-box;
		gap: 48px;
		width: 100%;
		max-width: 100%;
	}

	.heading {
		width: 100%;
		max-width: 100%;
		height: auto;
		min-height: 96px;
		padding: 16px 20px;
		box-sizing: border-box;
		font-size: clamp(24px, 4vw, 36px);
		text-align: center;
	}

	.cars {
		grid-template-columns: repeat(2, minmax(0, 1fr));
		grid-template-rows: repeat(6, 104px);
		gap: 24px;
		width: 100%;
	}

	.brand-page {
		grid-row: 1 / 6;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		grid-template-rows: repeat(5, 104px);
		gap: 24px;
	}

	.cell { height: 104px; }

	.navigation {
		grid-row: 6;
		grid-column: 1 / -1;
		height: 64px;
		gap: 16px;
	}

	.button {
		flex-basis: 64px;
		width: 64px;
		height: 64px;
		padding: 18px;
	}

	.button img {
		width: auto;
		height: auto;
		max-width: 100%;
		max-height: 100%;
		object-fit: contain;
	}

	.page { height: 64px; }
}

@media (max-width: 900px) {
	.sector4 {
		padding-inline: 16px;
		gap: 40px;
	}

	.heading {
		min-height: 88px;
		font-size: clamp(22px, 6vw, 30px);
	}
}

@media (max-width: 700px) {
	.sector4 {
		gap: 40px;
		padding-inline: 16px;
	}

	.heading {
		width: 100%;
		height: 100px;
		padding: 20px;
		font-size: clamp(23px, 7vw, 30px);
		line-height: 1.15;
		text-align: center;
	}

	.cars {
		grid-template-rows: repeat(6, 92px);
		gap: 16px;
	}

	.brand-page {
		grid-template-rows: repeat(5, 92px);
		gap: 16px;
	}

	.cell {
		height: 92px;
		padding: 20px;
		font-size: 20px;
	}

	.navigation {
		height: 52px;
		gap: 10px;
		padding: 0;
	}

	.button {
		flex-basis: 52px;
		width: 52px;
		height: 52px;
		padding: 14px;
	}

	.page { height: 52px; font-size: 14px; }
}

@media (max-width: 520px) {
	.cars {
		grid-template-columns: minmax(0, 1fr);
		grid-template-rows: none;
	}

	.brand-page {
		grid-column: auto;
		grid-row: auto;
		grid-template-columns: minmax(0, 1fr);
		grid-template-rows: none;
	}

	.navigation {
		grid-row: auto;
		grid-column: auto;
	}

	.brands-loading {
		grid-row: auto;
		min-height: 300px;
	}
}

.brand-button__transition-enter-from,
.brand-button__transition-leave-to {
	opacity: 0;
	filter: blur(10px);
	scale: 1.1;
}

.brand-button__transition-enter-to,
.brand-button__transition-leave-from {
	opacity: 1;
	filter: blur(0);
	scale: 1;
}

.brand-button__transition-enter-active,
.brand-button__transition-leave-active {
	transition: opacity .2s ease-out, filter .3s ease-out, scale .3s ease-out;
}
</style>
