<script setup lang="ts">

import BlockGlass from "../components/BlockGlass.vue";
import { storeToRefs } from "pinia";
import CarListCard from "../components/CarListCard.vue";
import { useRouter } from "vue-router";
import { computed, ref, watch } from "vue";
import Arrow from "../assets/arrow.svg";
import BlockGlassButton from "../components/BlockGlassButton.vue";
import LoadingAnimation from "../components/LoadingAnimation.vue";
import { useStore } from "../stores/Store.ts";
import { useCarListFilterSet } from "../stores/CarListFilterSet.ts";
import TextIconButton from "../components/TextIconButton.vue";

const router = useRouter()

const store = useStore()
const { cars, carsLoading } = storeToRefs(store)

const carListFilterSet = useCarListFilterSet()
const { brand } = storeToRefs(carListFilterSet)

const carsPerPage = 10
const carListPage = ref(0)
const carListPages = computed(() => Math.max(1, Math.ceil(cars.value.length / carsPerPage)))

watch(brand, () => carListPage.value = 0)

const goBack = () => router.push({ name: 'main', hash: '#brand-selection' })
const goToCar = (id: string) => router.push({ name: 'car', params: { id } })

const getBrandLogoHref = (brand: string): string => {
	const extension = brand.toLowerCase() === "great wall" ? "png" : "svg"
	return new URL(`../assets/car-logos/${ brand.toLowerCase() }.${ extension }`, import.meta.url).href
}
</script>

<template>
	<LoadingAnimation v-if="carsLoading" />

	<template v-else>
		<div class="carListPage">
			<block-glass class="cell heading cell-heading-animation"
						 style="--background-color: var(--color-secondary-7)">
				<text>
					<span>Автомобили</span>
					<span><b>{{ brand }}</b></span>
				</text>

				<img :src="getBrandLogoHref(brand)" :alt="`${brand} logo`" />
			</block-glass>

			<div class="list">
				<TextIconButton class="button__go-back" :icon="Arrow" :icon-alt="Arrow" @click="goBack()">
					Назад
				</TextIconButton>

				<car-list-card class="car-list-card-animation"
							   v-for="(car, index) in cars.slice(carListPage * carsPerPage, (carListPage + 1) * carsPerPage)"
							   :key="car.id"
							   @click="goToCar(car.id)"

							   :id="car.id"
							   :model="car.model"
							   :brand="car.brand"
							   :year="car.year"
							   :mileage="car.mileage"
							   :power="car.power"
							   :displacement="car.displacement"
							   :fuel="car.fuel"
							   :gear="car.gear"
							   :color="car.color"
							   :price="car.price"
							   :status="car.status"
							   :images="car.images"

							   :style="{ animationDelay: `${0.3 + 0.2 * index}s` }"
				/>
			</div>
		</div>

		<div class="car-list__navigation car-list__navigation__animation">
			<block-glass-button class="button prev"
								@click="carListPage = Math.max(0, carListPage - 1)"
								:style="{
									borderRadius: 100,
									cursor: carListPage === 0 ? 'not-allowed' : 'pointer',
									opacity: carListPage === 0 ? '.5' : '1'
								}"
			>
				<img :src="Arrow" alt="Arrow" />
			</block-glass-button>

			<block-glass class="page">
				Страница {{ carListPage + 1 }} из {{ carListPages }}
			</block-glass>

			<block-glass-button class="button next"
								@click="carListPage = Math.min(carListPage + 1, carListPages - 1)"
								:style="{
									borderRadius: 100,
									cursor: carListPage >= carListPages - 1 ? 'not-allowed' : 'pointer',
									opacity: carListPage >= carListPages - 1 ? '.5' : '1'
								}"
			>
				<img :src="Arrow" alt="Arrow" />
			</block-glass-button>
		</div>
	</template>
</template>

<style scoped>
.car-list__navigation {
	display: flex;
	flex-direction: row;
	gap: 30px;

	position: fixed;
	bottom: 30px;
	right: 30px;

	height: 60px;
	z-index: 20;
}

.car-list__navigation .button {
	flex: 0 0 60px;
	width: 60px;
	height: 100%;
	aspect-ratio: 1/1;
	border-radius: 50% !important;

	box-sizing: border-box;
	padding: 10px;
}

.car-list__navigation .button :deep(img) {
	display: block;
	width: 60%;
	height: 60%;
	object-fit: contain;
}

.car-list__navigation .button.next :deep(img) {
	rotate: 180deg;
}

.car-list__navigation .page {
	font-size: 20px;
	font-weight: 300;
	color: rgba(255, 255, 255, 0.7);

	box-sizing: border-box;
	padding: 0 50px;

	user-select: none;
}

.carListPage {
	position: relative;

	display: flex;
	flex-direction: column;
	align-items: center;

	padding: 120px 0;
	gap: 100px;

	box-sizing: border-box;
}

.cell.heading {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;

	font-size: 40px;
	font-weight: 400;
	color: rgba(255, 255, 255, 0.7);

	width: 600px;
	height: 150px;

	box-sizing: border-box;
	padding: 30px 50px;
}

.cell.heading img {
	object-fit: contain;

	width: 100%;
	height: 100%;

	max-width: 130px;
	max-height: 90px;
}

.heading text {
	display: flex;
	flex-direction: column;
}

.heading text b {
	color: rgba(255, 255, 255, 0.9);
}

.list {
	display: flex;
	flex-direction: column;
	align-items: center;

	gap: 20px;
}

@media (max-width: 1100px) {
	.carListPage {
		padding-inline: 24px;
		padding-bottom: 170px;
	}

	.car-list__navigation {
		right: 24px;
		bottom: 24px;
		gap: 16px;
	}

	.car-list__navigation .page { padding-inline: 28px; }
}

@media (max-width: 700px) {
	.carListPage {
		padding: 100px 16px 150px;
		gap: 48px;
	}

	.cell.heading {
		width: 100%;
		height: 110px;
		padding: 20px 28px;
		font-size: 28px;
	}

	.cell.heading img { max-width: 90px; max-height: 66px; }

	.list { width: 100%; gap: 16px; }

	.car-list__navigation {
		right: 16px;
		bottom: 16px;
		height: 48px;
		gap: 8px;
	}

	.car-list__navigation .button {
		flex-basis: 48px;
		width: 48px;
		padding: 12px;
	}

	.car-list__navigation .page {
		padding: 0 16px;
		font-size: 14px;
	}
}

@media (max-width: 900px) {
	.carListPage { padding-bottom: 32px; }

	.car-list__navigation {
		position: relative;
		right: auto;
		bottom: auto;
		align-self: flex-end;
		margin: 0 16px 24px auto;
	}
}

.cell-heading-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s cellHeadingSlideIn ease-out forwards;
}

.car-list-card-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s carListCardSlideIn ease-out forwards;
}

.car-list__navigation__animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s carListPagesSlideIn ease-out .3s forwards;
}

@keyframes carListCardSlideIn {
	from {
		opacity: 0;
		translate: -20px 0;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		translate: 0 0;
		filter: blur(0);
	}
}

@keyframes cellHeadingSlideIn {
	from {
		opacity: 0;
		translate: 0 -5px;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		translate: 0 0;
		filter: blur(0);
	}
}

@keyframes carListPagesSlideIn {
	from {
		opacity: 0;
		translate: 0 5px;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		translate: 0 0;
		filter: blur(0);
	}
}
</style>
