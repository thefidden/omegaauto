<script setup lang="ts">

import BlockGlass from "./BlockGlass.vue";
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useStore } from "../stores/Store.ts";
import ButtonShiftingTextWithIcon from "./ButtonShiftingTextWithIcon.vue";

const route = useRoute()
const router = useRouter()

const pageList = computed(() => {
	interface Page {
		title: string,
		href: string,
		ascendant: string | null,
		action: () => ReturnType<typeof router.push>
	}

	const list: Page[] = []
	const { car } = storeToRefs(useStore())
	const brand = route.query.brand || car.value?.brand || ''

	const pages: Record<string, Page> = {
		'main': {
			title: 'Главная страница',
			href: '/',
			ascendant: null,
			action: () => router.push({
				name: 'main'
			})
		},
		'all-brands': {
			title: 'Все бренды',
			href: '/#brand-selection',
			ascendant: 'main',
			action: () => router.push({
				name: 'main',
				hash: '#brand-selection'
			})
		},
		'car-list': {
			title: `Автомобили ${ brand }`,
			href: `/cars/?brand=${ brand }`,
			ascendant: 'all-brands',
			action: () => router.push({
				name: 'car-list',
				query: { brand }
			})
		},
		'car': {
			title: `Автомобиль ${ car.value?.brand } ${ car.value?.model }`.trim(),
			href: `/cars/${ car.value?.id }`,
			ascendant: 'car-list',
			action: () => router.push({
				name: 'car',
				params: { id: car.value?.id }
			})
		}
	}

	for (
		let page: Page | null = pages[route.name as string] ?? pages.main;
		page;
		page = page.ascendant ? pages[page.ascendant] : null
	)
		list.push(page)

	return list.reverse()
})
</script>

<template>
	<block-glass class="footer"
				 :class="{ 'above-pagination': route.name === 'car-list' }"
				 style="background-color: var(--color-primary-30)">
		<nav aria-label="Навигация по страницам">
			<button-shifting-text-with-icon
				v-for="page in pageList"
				:key="page.href"
				class="footer-page"
				icon-alt=""
				@click="page.action()"
			>
				{{ page.title }}
			</button-shifting-text-with-icon>
		</nav>
	</block-glass>
</template>

<style scoped>
.footer {
	position: fixed;
	bottom: 30px;
	left: 30px;
	z-index: 10;

	max-width: calc(100vw - 60px);
	min-height: 60px;

	box-sizing: border-box;
	padding: 10px 20px;

	user-select: none;
}

nav {
	display: flex;
	flex-direction: row;
	align-items: center;

	gap: 0;
	max-width: 100%;
	overflow-x: auto;
	scrollbar-width: none;
}

nav::-webkit-scrollbar { display: none; }

.footer-page {
	white-space: nowrap;
	font-weight: 400;
}

.footer-page:nth-last-child(1) {
	color: rgba(255, 255, 255, 0.9);
}

@media (max-width: 1240px) {
	.footer { background-color: rgba(8, 8, 12, 0.32) !important; }
}

@media (max-width: 900px) {
	.footer {
		position: relative;
		left: auto;
		bottom: auto;
		max-width: calc(100vw - 32px);
		min-height: 52px;
		margin: 24px 16px max(16px, env(safe-area-inset-bottom));
		padding: 6px 10px;
		background-color: rgba(8, 8, 12, 0.38) !important;
	}

	.footer.above-pagination {
		bottom: auto;
	}

	.footer :deep(.footer-page) {
		min-height: 40px;
		padding: 0 10px;
		color: var(--color-secondary-90);
		font-size: 14px;
	}
}
</style>
