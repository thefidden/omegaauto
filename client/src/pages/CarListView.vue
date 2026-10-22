<script setup lang="ts">

import BlockGlass from "../components/BlockGlass.vue";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import BlockGlassButton from "../components/BlockGlassButton.vue";
import LoadingAnimation from "../components/LoadingAnimation.vue";
import { useStore } from "../stores/Store.ts";
import { useCarListFilters } from "../stores/CarListFiltersStore.ts";
import TextIconButton from "../components/TextIconButton.vue";
import CarListFilters from "../components/CarListFilters.vue";
import CarListCardV2 from "../components/CarListCardV2.vue";
import { useColorMode } from "@vueuse/core";
import { navigateToHash } from "../utils/navigateToHash.ts";
import { getBrandLogoHref } from "../utils/brandLogos.ts";

import Arrow from "../assets/svg-light/arrow.svg";
import FilterIcon from "../assets/svg-light/filter.svg";

import ArrowDark from "../assets/svg-dark/arrow.svg";
import FilterIconDark from "../assets/svg-dark/filter.svg";

const colorMode = useColorMode({
	modes: { dark: 'dark', light: 'light' }
})

const router = useRouter()
const route = useRoute()

const store = useStore()
const { cars, carsCount, carsLoading } = storeToRefs(store)

const filters = useCarListFilters()

const brand = computed(() => route.query.brand as string | undefined)
const carsPerPage = 10
const carListPages = computed(() => Math.max(1, Math.ceil(carsCount.value / carsPerPage)))
const navigationAnimating = ref(true)
const filtersOpen = ref(false)
const isMobile = ref(
	typeof window !== 'undefined' && window.matchMedia('(max-width: 900px)').matches
)

let mobileMediaQuery: MediaQueryList | null = null
const syncMobile = () => {
	isMobile.value = mobileMediaQuery?.matches ?? false
	if (!isMobile.value) filtersOpen.value = false
}

const goBack = () => navigateToHash(router, '#brand-selection')
const goToCar = (id: string) => router.push({ name: 'car', params: { id } })
const goToPage = (page: number) => {
	if (page < 1 || page > carListPages.value || page === filters.page) return
	filters.page = page
	filters.apply()
}
const onNavigationAnimationEnd = () => {
	navigationAnimating.value = false
}
const openFilters = () => {
	filtersOpen.value = true
}
const closeFilters = () => {
	filtersOpen.value = false
}

const brandLogoHref = computed(() =>
	brand.value ? getBrandLogoHref(brand.value, colorMode.value === 'dark') : ''
)

watch(() => route.query, () => {
	filters.fetchFromRouteQuery()
	store.fetchCars()
}, { immediate: true })

onMounted(() => {
	mobileMediaQuery = window.matchMedia('(max-width: 900px)')
	syncMobile()
	mobileMediaQuery.addEventListener('change', syncMobile)
})

onUnmounted(() => {
	mobileMediaQuery?.removeEventListener('change', syncMobile)
})
</script>

<template>
	<div class="carListPage">
		<block-glass v-if="brand"
					 class="cell heading cell-heading-animation"
		>
			<span class="heading__title"><b>Автомобили {{ brand }}</b></span>
			<img class="heading__logo" :src="brandLogoHref" :alt="`${brand} logo`" />
		</block-glass>

		<div class="car-list__actions">
			<TextIconButton
				class="button__go-back"
				:icon="colorMode === 'dark' ? Arrow : ArrowDark"
				icon-alt="Назад"
				@click="goBack()"
			>
				К выбору марки
			</TextIconButton>

			<TextIconButton
				v-if="isMobile"
				class="button__filters"
				:icon="colorMode === 'dark' ? FilterIcon : FilterIconDark"
				icon-alt="Фильтры"
				@click="openFilters"
			>
				Фильтры
			</TextIconButton>
		</div>

		<CarListFilters
			v-if="!isMobile"
			class="car-list-filters car-list-filters--panel"
		/>

		<div class="list">
			<Transition name="car-list-card__transition" mode="out-in">
				<LoadingAnimation v-if="carsLoading" key="loading" />

				<div v-else-if="cars.length" key="list" class="list__cards">
					<CarListCardV2
						v-for="(car, index) in cars"
						:key="car.id"
						class="car-list-card-animation"
						:style="{ animationDelay: `${ index * 0.1 }s` }"
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
						:price_total_rub="car.price_total_rub"
						:status="car.status"
						:images="car.images"
					/>
				</div>

				<h2 v-else key="empty" class="list__car-list-empty">
					Автомобили с заданными параметрами отсутствуют
				</h2>
			</Transition>
		</div>
	</div>

	<div
		class="car-list__navigation"
		:class="{ 'car-list__navigation__animation': navigationAnimating }"
		@animationend="onNavigationAnimationEnd"
	>
		<block-glass-button class="button prev"
							@click="goToPage(filters.page - 1)"
							:style="{
								borderRadius: 100,
								cursor: filters.page <= 1 ? 'not-allowed' : 'pointer',
								opacity: filters.page <= 1 ? '.5' : '1'
							}"
		>
			<img :src="colorMode === 'dark' ? Arrow : ArrowDark" alt="Arrow" />
		</block-glass-button>

		<block-glass class="page">
			Страница {{ filters.page }} из {{ carListPages }}
		</block-glass>

		<block-glass-button class="button next"
							@click="goToPage(filters.page + 1)"
							:style="{
								borderRadius: 100,
								cursor: filters.page >= carListPages ? 'not-allowed' : 'pointer',
								opacity: filters.page >= carListPages ? '.5' : '1'
							}"
		>
			<img :src="colorMode === 'dark' ? Arrow : ArrowDark" alt="Arrow" />
		</block-glass-button>
	</div>

	<Teleport to="body">
		<Transition name="car-list-filters-modal">
			<div
				v-if="isMobile && filtersOpen"
				class="car-list-filters-modal"
				@click.self="closeFilters"
				@keydown.esc="closeFilters"
			>
				<div class="car-list-filters-modal__box-wrap">
					<CarListFilters
						class="car-list-filters car-list-filters--modal"
						@applied="closeFilters"
					/>
					<button
						type="button"
						class="car-list-filters-modal__close"
						aria-label="Закрыть фильтры"
						@click="closeFilters"
					>
						<span></span>
						<span></span>
					</button>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<style scoped>
.carListPage {
	--page-pad-x: 24px;
	--page-pad-top: 120px;
	--page-pad-bottom: 120px;

	position: relative;
	box-sizing: border-box;

	display: grid;
	grid-template-areas:
		"actions heading"
		"filters list";
	grid-template-columns: minmax(0, 450px) minmax(0, 1fr);

	width: 100%;
	max-width: 100%;
	min-width: 0;

	padding: var(--page-pad-top) var(--page-pad-x) var(--page-pad-bottom);

	column-gap: 50px;
	row-gap: 25px;
}

.car-list-filters--panel {
	grid-area: filters;
	background-color: var(--color-primary-30);
	min-width: 0;
	max-width: 100%;
}

.car-list__actions {
	grid-area: actions;

	display: flex;
	flex-direction: column;
	align-items: flex-start;
	justify-content: center;
	gap: 12px;
	min-width: 0;
}

.cell.heading {
	grid-area: heading;

	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16px;

	align-self: center;
	justify-self: stretch;

	background-color: var(--color-primary-30);

	font-size: 32px;
	font-weight: 400;
	color: var(--color-secondary-70);

	width: 100%;
	max-width: 100%;
	min-width: 0;
	min-height: 75px;

	box-sizing: border-box;
	padding: 15px clamp(16px, 3vw, 50px);
}

.heading__title {
	min-width: 0;
	overflow-wrap: anywhere;
}

.heading__title b {
	color: var(--color-secondary);
}

.heading__logo {
	display: block;
	flex: 0 0 auto;

	width: auto;
	height: auto;
	max-width: min(130px, 28%);
	max-height: 48px;

	object-fit: contain;
	object-position: center;
}

.list {
	grid-area: list;

	display: flex;
	flex-direction: column;
	align-items: stretch;

	width: 100%;
	min-width: 0;
}

.list__cards {
	display: flex;
	flex-direction: column;
	align-items: stretch;
	gap: 20px;
	width: 100%;
	min-width: 0;
}

.list__car-list-empty {
	color: var(--color-secondary-70);
	user-select: none;
	text-align: center;
	padding-inline: 8px;
}

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
	aspect-ratio: 1 / 1;
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
	color: var(--color-secondary-70);

	box-sizing: border-box;
	padding: 0 50px;

	user-select: none;
}

.button__go-back,
.button__filters {
	width: fit-content;
	max-width: 100%;
}

.car-list-filters-modal {
	display: grid;
	place-items: center;

	position: fixed;
	inset: 0;
	z-index: 10000;

	box-sizing: border-box;
	padding: max(16px, env(safe-area-inset-top)) max(16px, env(safe-area-inset-right)) max(16px, env(safe-area-inset-bottom)) max(16px, env(safe-area-inset-left));

	background-color: var(--color-primary-50);
	backdrop-filter: blur(10px);

	overflow-y: auto;
}

.car-list-filters-modal__box-wrap {
	position: relative;

	width: min(450px, calc(100vw - 32px));
	max-height: calc(100dvh - 32px);
	overflow-x: hidden;
	overflow-y: auto;
}

.car-list-filters-modal__box-wrap :deep(.car-list-filters) {
	background-color: var(--color-primary-80);
	max-width: none;
}

.car-list-filters-modal__box-wrap :deep(img) {
	width: auto;
	height: auto;
	max-height: 22px;
	object-fit: contain;
}

.car-list-filters-modal__close {
	position: absolute;
	top: 12px;
	right: 12px;
	z-index: 2;

	display: grid;
	place-items: center;

	width: 40px;
	height: 40px;

	color: var(--color-secondary);
	background-color: transparent;

	box-sizing: border-box;
	border-radius: 100%;
	padding: 0;
	border: 0;

	cursor: pointer;

	transition: opacity .3s ease-out;
}

.car-list-filters-modal__close span {
	position: absolute;

	background-color: var(--color-secondary);

	box-sizing: border-box;
	border-radius: 2px;

	width: 25px;
	height: 5px;
}

.car-list-filters-modal__close:hover {
	opacity: .5;
}

.car-list-filters-modal__close span:first-child { rotate: 45deg; }

.car-list-filters-modal__close span:last-child { rotate: -45deg; }

.car-list-filters-modal-enter-from,
.car-list-filters-modal-leave-to {
	opacity: 0;
	filter: blur(10px);
	scale: 1.2;
}

.car-list-filters-modal-enter-to,
.car-list-filters-modal-leave-from {
	opacity: 1;
	filter: blur(0);
	scale: 1;
}

.car-list-filters-modal-enter-active,
.car-list-filters-modal-leave-active {
	transition: opacity .3s ease-out, filter .3s ease-out, scale .3s ease-out;
}

@media (max-width: 1100px) {
	.carListPage {
		--page-pad-x: 24px;
		--page-pad-bottom: 170px;
		column-gap: 28px;
		grid-template-columns: minmax(0, 360px) minmax(0, 1fr);
	}

	.cell.heading {
		font-size: 28px;
	}

	.heading__logo {
		max-width: min(110px, 30%);
		max-height: 44px;
	}

	.car-list__navigation {
		right: 24px;
		bottom: 24px;
		gap: 16px;
	}

	.car-list__navigation .page {
		padding-inline: 28px;
	}
}

@media (max-width: 900px) {
	.carListPage {
		--page-pad-x: 16px;
		--page-pad-top: 100px;
		--page-pad-bottom: 32px;

		grid-template-areas:
			"heading"
			"actions"
			"list";
		grid-template-columns: minmax(0, 1fr);
		row-gap: 18px;
	}

	.cell.heading {
		min-height: 64px;
		padding: 14px 16px;
		font-size: clamp(18px, 5vw, 22px);
		gap: 12px;
	}

	.heading__logo {
		max-width: min(72px, 26%);
		max-height: 36px;
	}

	.car-list__actions {
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 8px 16px;
		width: 100%;
	}

	.list__cards {
		gap: 16px;
	}

	.car-list__navigation {
		position: relative;
		right: auto;
		bottom: auto;
		align-self: flex-end;
		justify-content: flex-end;
		flex-wrap: wrap;
		width: calc(100% - 32px);
		max-width: 100%;
		height: auto;
		min-height: 48px;
		margin: 0 16px 24px auto;
		gap: 12px;
	}

	.car-list__navigation .button {
		flex-basis: 48px;
		width: 48px;
		height: 48px;
		padding: 10px;
	}

	.car-list__navigation .page {
		padding: 0 14px;
		font-size: 14px;
		min-height: 48px;
	}
}

@media (max-width: 700px) {
	.carListPage {
		--page-pad-x: 16px;
		--page-pad-top: 96px;
		--page-pad-bottom: 20px;
	}

	.cell.heading {
		padding: 12px 14px;
	}

	.heading__logo {
		max-width: min(64px, 24%);
		max-height: 32px;
	}

	.car-list__navigation {
		right: auto;
		bottom: auto;
		width: calc(100% - 32px);
		margin: 0 16px 16px auto;
		gap: 8px;
	}

	.car-list__navigation .button {
		flex-basis: 48px;
		width: 48px;
		padding: 12px;
	}

	.car-list__navigation .page {
		padding: 0 10px;
		font-size: 13px;
	}
}

.cell-heading-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s cellHeadingSlideIn ease-out forwards;
}

.car-list__navigation__animation {
	opacity: 0;
	will-change: opacity, translate;
	animation: .5s carListPagesSlideIn ease-out .3s forwards;
}

.car-list-card__transition-enter-from,
.car-list-card__transition-leave-to {
	opacity: 0;
	filter: blur(10px);
	translate: 20px 0;
}

.car-list-card__transition-enter-to,
.car-list-card__transition-leave-from {
	opacity: 1;
	filter: blur(0);
	translate: 0 0;
}

.car-list-card__transition-enter-active,
.car-list-card__transition-leave-active {
	transition: opacity .3s ease-out, filter .3s ease-out, translate .3s ease-out;
}

.list__cards.car-list-card__transition-enter-from,
.list__cards.car-list-card__transition-enter-to {
	opacity: 1;
	filter: none;
	translate: none;
}

.list__cards.car-list-card__transition-enter-active {
	transition: none;
}

.car-list-card-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .3s carListCardSlideIn ease-out forwards;
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
	}
	to {
		opacity: 1;
		translate: 0 0;
	}
}

@keyframes carListCardSlideIn {
	from {
		opacity: 0;
		translate: 20px 0;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		translate: 0 0;
		filter: blur(0);
	}
}
</style>
