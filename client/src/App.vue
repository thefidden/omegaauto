<script setup lang="ts">

import { nextTick, onMounted, watch } from "vue";
import { useStore } from "./stores/Store.ts";
import { useCarListFilterSet } from "./stores/CarListFilterSet.ts";
import { storeToRefs } from "pinia";
import Header from "./components/Header.vue";
import Navigation from "./components/Navigation.vue";
import { useRoute } from "vue-router";
import { takePendingScroll } from "./router.ts";
import { smoothScrollTo } from "./utils/smoothScroll.ts";

const store = useStore()
const route = useRoute()
const { fetchAvailableBrands, fetchCars, fetchCar } = store
const { carID } = storeToRefs(store)

const carListFilterSet = useCarListFilterSet()
const { brand } = storeToRefs(carListFilterSet)

function scrollToHash(hash: string) {
	if (!hash) return Promise.resolve()

	const target = document.getElementById(decodeURIComponent(hash.slice(1)))
	if (!target) return Promise.resolve()

	const targetTop = window.scrollY + target.getBoundingClientRect().top
	return smoothScrollTo(window.scrollX, targetTop)
}

async function applyPendingScroll() {
	const scroll = takePendingScroll()
	if (!scroll) return false

	if ('hash' in scroll) {
		await scrollToHash(scroll.hash)
		return true
	}

	await smoothScrollTo(scroll.left, scroll.top)
	return true
}

onMounted(async () => {
	void fetchAvailableBrands()
	await nextTick()
	if (!await applyPendingScroll())
		await scrollToHash(route.hash)
})

watch(brand, (newValue, oldValue) => {
	if (newValue !== oldValue)
		fetchCars({ brand: newValue })
})

watch(carID, (newValue, oldValue) => {
	if (newValue && newValue !== oldValue)
		fetchCar(newValue)
})

watch(
	() => ({ path: route.path, hash: route.hash, fullPath: route.fullPath }),
	async (to, from) => {
		if (to.path === from.path) {
			await nextTick()
			await applyPendingScroll()
		}
	}
)
</script>

<template>
	<div class="app">
		<div class="ellipses" aria-hidden="true">
			<div class="ellipse" v-for="n in 7" :key="n"></div>
		</div>

		<div class="root">
			<router-view v-slot="{ Component, route }">
				<Transition name="page"
							mode="out-in"
							@after-enter="applyPendingScroll">
					<main :key="route.path" class="route-page">
						<component :is="Component" />
					</main>
				</Transition>
			</router-view>
			<Navigation class="navigation-animation" />
		</div>

		<Header class="header-animation" />
	</div>

	<div class="noise" />
</template>

<style scoped>
.page-enter-from,
.page-leave-to {
	opacity: 0;
	filter: blur(10px);
}

.page-enter-to,
.page-leave-from {
	opacity: 1;
	filter: blur(0);
}

.page-enter-active,
.page-leave-active {
	transition: opacity .3s ease-out, filter .3s ease-out;
}

.route-page {
	width: 100%;
	min-width: 0;
}

.app {
	position: relative;
	isolation: isolate;
	overflow: clip;
	min-height: 100dvh;
}

.root {
	position: relative;
	z-index: 1;

	display: flex;
	flex-direction: column;

	max-width: 1500px;
	min-height: 100dvh;
	margin: 0 auto;
}

.ellipses {
	--ellipse-small: max(420px, 36.458vw);
	--ellipse-large: max(600px, 52.083vw);

	position: absolute;
	inset: 0;
	z-index: 0;

	width: 100%;
	min-height: 3700px;
	height: auto;
	overflow: hidden;

	filter: blur(clamp(120px, 10.417vw, 200px));
	opacity: 0.6;
	transform: translateZ(0);
	pointer-events: none;
}

.ellipse {
	position: absolute;
	z-index: -3;

	background-color: var(--color-secondary);
	border-radius: 100%;

	will-change: opacity, transform;
	animation: 1s ellipseFadeIn ease-out;
}

.ellipses .ellipse:nth-child(1) {
	left: 50%;
	transform: translateX(-50%) translateY(-50%);

	width: var(--ellipse-small);
	height: var(--ellipse-small);
}

.ellipses .ellipse:nth-child(2) {
	left: 0;
	top: 150px;
	transform: translateX(-50%);

	width: var(--ellipse-small);
	height: var(--ellipse-small);
}

.ellipses .ellipse:nth-child(3) {
	left: 100%;
	top: 150px;
	transform: translateX(-50%);

	width: var(--ellipse-small);
	height: var(--ellipse-small);
}

.ellipses .ellipse:nth-child(4) {
	left: 13.75vw;
	top: 709px;

	width: var(--ellipse-large);
	height: var(--ellipse-large);
}

.ellipses .ellipse:nth-child(5) {
	left: 100%;
	top: 1685px;
	transform: translateX(-50%);

	width: var(--ellipse-small);
	height: var(--ellipse-small);
}

.ellipses .ellipse:nth-child(6) {
	left: -10vw;
	top: 2064px;

	width: var(--ellipse-large);
	height: var(--ellipse-large);
}

.ellipses .ellipse:nth-child(7) {
	left: 50%;
	top: 100%;

	transform: translateX(-50%) translateY(-50%);

	width: var(--ellipse-large);
	height: var(--ellipse-large);
}

.noise {
	position: fixed;
	inset: 0;

	z-index: 11000;
	pointer-events: none;

	opacity: 0.8;
	background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='.65'/%3E%3C/svg%3E");
	background-size: 180px 180px;
	mix-blend-mode: soft-light;
}

.header-animation {
	opacity: 0;
	will-change: opacity, filter, translate;
	animation: .5s headerSlideIn ease-out .3s forwards;
}

.navigation-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s NavigationSlideIn ease-out .3s forwards;
}

@keyframes ellipseFadeIn {
	from {
		opacity: 0;
		scale: 2;
	}
	to {
		opacity: 1;
		scale: 1;
	}
}

@keyframes headerSlideIn {
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

@keyframes NavigationSlideIn {
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
