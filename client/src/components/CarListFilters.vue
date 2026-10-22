<script setup lang="ts">

import BlockGlass from "./BlockGlass.vue";
import { useStore } from "../stores/Store.ts";
import { storeToRefs } from "pinia";
import { computed, ref } from "vue";
import BlockGlassSelect from "./BlockGlassSelect.vue";
import BlockGlassInput from "./BlockGlassInput.vue";
import TextIconButton from "./TextIconButton.vue";
import { type CarListOrdering, useCarListFilters } from "../stores/CarListFiltersStore.ts";
import { useColorMode } from "@vueuse/core";

import TickIcon from "../assets/svg-light/tick.svg"
import CrossIcon from "../assets/svg-light/cross.svg"

import TickIconDark from "../assets/svg-dark/tick.svg"
import CrossIconDark from "../assets/svg-dark/cross.svg"

const colorMode = useColorMode({
	modes: { dark: 'dark', light: 'light' }
})

const emit = defineEmits<{
	applied: []
}>()

const store = useStore()
const { brands, colors, fuels, gears } = storeToRefs(store)

const filters = useCarListFilters()

const applyFilters = () => {
	if (!filters.validate()) return
	filters.page = 1
	filters.apply()
	emit('applied')
}

const years = computed(() => {
	const currentYear = new Date().getFullYear()
	const minYear = 2010
	return Array.from({ length: currentYear - minYear + 1 }, (_, i) => currentYear - i)
})

const displacements = computed(() => {
	const minDisplacement = 1
	const maxDisplacement = 5

	return Array.from(
		{ length: (maxDisplacement - minDisplacement + 1) * 10 },
		(_, i) => minDisplacement + i / 10
	)
})

const orderings: Array<{
	name: string,
	value: CarListOrdering
}> = [
	{ name: 'Стоимость (по возрастанию)', value: 'price_total_rub' },
	{ name: 'Стоимость (по убыванию)', value: '-price_total_rub' },
	{ name: 'Пробег, км. (по возрастанию)', value: 'mileage' },
	{ name: 'Пробег, км. (по убыванию)', value: '-mileage' },
	{ name: 'Год (по возрастанию)', value: 'year' },
	{ name: 'Год (по убыванию)', value: '-year' },
	{ name: 'Мощность, л.с. (по возрастанию)', value: 'power' },
	{ name: 'Мощность, л.с. (по убыванию)', value: '-power' },
	{ name: 'Марка (по возрастанию)', value: 'brand' },
	{ name: 'Марка (по убыванию)', value: '-brand' },
	{ name: 'Объем, л. (по возрастанию)', value: 'displacement' },
	{ name: 'Объем, л. (по убыванию)', value: '-displacement' },
]

const brand = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const gear = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const color = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const fuel = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const yearMin = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const yearMax = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const displacementMin = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const displacementMax = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const mileageMin = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const mileageMax = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const powerMin = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const powerMax = ref<InstanceType<typeof BlockGlassSelect> | null>(null)
const ordering = ref<InstanceType<typeof BlockGlassSelect> | null>(null)

type FilterField =
	| 'brand'
	| 'gear'
	| 'color'
	| 'fuel'
	| 'yearMin' | 'yearMax'
	| 'displacementMin' | 'displacementMax'
	| 'mileageMin' | 'mileageMax'
	| 'powerMin' | 'powerMax'
	| 'ordering'

const activeFilter = ref<FilterField | null>(null)
const setActiveFilter = (field: FilterField, isOpen: boolean) => {
	if (isOpen) activeFilter.value = field
	else if (activeFilter.value === field) activeFilter.value = null
}
const getOrderingValueByName = (orderingName: string) =>
	orderings.find(orderingRecord => orderingRecord.name === orderingName)?.value
const getOrderingNameByValue = (orderingValue: CarListOrdering) =>
	orderings.find(orderingRecord => orderingRecord.value === orderingValue)?.name

</script>

<template>
	<block-glass class="car-list-filters">
		<h1>Фильтры</h1>

		<form action="" method="get">
			<div>
				<block-glass-select
					class="car-list-filters__brand"
					:values="brands"
					label="Марка"
					ref="brand"
					:isOpen="activeFilter === 'brand'"
					:initialValue="filters.brand || null"
					@update:isOpen="setActiveFilter('brand', $event)"
					@update:value="value => filters.brand = (value != null && value !== '' ? String(value) : null)"
				/>
				<block-glass-select
					class="car-list-filters__gear"
					:values="gears"
					label="Трансмиссия"
					ref="gear"
					:isOpen="activeFilter === 'gear'"
					:initialValue="filters.gear || null"
					@update:isOpen="setActiveFilter('gear', $event)"
					@update:value="value => filters.gear = (value != null && value !== '' ? String(value) : null)"
				/>
			</div>

			<div>
				<block-glass-select
					class="car-list-filters__color"
					:values="colors"
					label="Цвет"
					ref="color"
					:isOpen="activeFilter === 'color'"
					:initialValue="filters.color || null"
					@update:isOpen="setActiveFilter('color', $event)"
					@update:value="value => filters.color = (value != null && value !== '' ? String(value) : null)"
				/>
				<block-glass-select
					class="car-list-filters__fuel"
					:values="fuels"
					label="Топливо"
					ref="fuel"
					:isOpen="activeFilter === 'fuel'"
					:initialValue="filters.fuel || null"
					@update:isOpen="setActiveFilter('fuel', $event)"
					@update:value="value => filters.fuel = (value!= null && value !== '' ? String(value) : null)"
				/>
			</div>

			<div class="car-list-filters__years">
				<block-glass-select
					class="car-list-filters__year-min"
					:values="years"
					label="Год, от"
					ref="yearMin"
					:isOpen="activeFilter === 'yearMin'"
					:initialValue="filters.yearMin || null"
					@update:isOpen="setActiveFilter('yearMin', $event)"
					@update:value="value => filters.yearMin = (value != null && value !== '' ? Number(value) : null)"
				/>
				<block-glass-select
					class="car-list-filters__year-max"
					:values="years"
					label="Год, до"
					ref="yearMax"
					:isOpen="activeFilter === 'yearMax'"
					:initialValue="filters.yearMax || null"
					@update:isOpen="setActiveFilter('yearMax', $event)"
					@update:value="value => filters.yearMax = (value != null && value !== '' ? Number(value) : null)"
				/>
			</div>

			<div class="car-list-filters__displacements">
				<block-glass-select
					class="car-list-filters__displacement-min"
					:values="displacements"
					label="Объем, л, от"
					ref="displacementMin"
					:isOpen="activeFilter === 'displacementMin'"
					:initialValue="filters.displacementMin || null"
					@update:isOpen="setActiveFilter('displacementMin', $event)"
					@update:value="value => filters.displacementMin = (value != null && value !== '' ? Number(value) : null)"
				/>
				<block-glass-select
					class="car-list-filters__displacement-max"
					:values="displacements"
					label="Объем, л, до"
					ref="displacementMax"
					:isOpen="activeFilter === 'displacementMax'"
					:initialValue="filters.displacementMax || null"
					@update:isOpen="setActiveFilter('displacementMax', $event)"
					@update:value="value => filters.displacementMax = (value != null && value !== '' ? Number(value) : null)"
				/>
			</div>

			<div class="car-list-filters__mileages">
				<block-glass-input
					class="car-list-filters__mileage-min"
					label="Пробег, км, от"
					type="number"
					ref="mileageMin"
					:isFocused="activeFilter === 'mileageMin'"
					:initialValue="filters.mileageMin || null"
					@update:isFocused="setActiveFilter('mileageMin', $event)"
					@update:value="value => filters.mileageMin = (value != null && value !== '' ? Number(value) : null)"
				/>
				<block-glass-input
					class="car-list-filters__mileage-max"
					label="Пробег, км, до"
					type="number"
					ref="mileageMax"
					:isFocused="activeFilter === 'mileageMax'"
					:initialValue="filters.mileageMax || null"
					@update:isFocused="setActiveFilter('mileageMax', $event)"
					@update:value="value => filters.mileageMax = (value != null && value !== '' ? Number(value) : null)"
				/>
			</div>

			<div class="car-list-filters__powers">
				<block-glass-input
					class="car-list-filters__power-min"
					label="Мощность, л.с., от"
					type="number"
					ref="powerMin"
					:isFocused="activeFilter === 'powerMin'"
					:initialValue="filters.powerMin || null"
					@update:isFocused="setActiveFilter('powerMin', $event)"
					@update:value="value => filters.powerMin = (value != null && value !== '' ? Number(value) : null)"
				/>
				<block-glass-input
					class="car-list-filters__power-max"
					label="Мощность, л.с., до"
					type="number"
					ref="powerMax"
					:isFocused="activeFilter === 'powerMax'"
					:initialValue="filters.powerMax || null"
					@update:isFocused="setActiveFilter('powerMax', $event)"
					@update:value="value => filters.powerMax = (value != null && value !== '' ? Number(value) : null)"
				/>
			</div>

			<div>
				<block-glass-select
					class="car-list-filters__ordering"
					label="Сортировка"
					ref="ordering"
					:values="orderings.map(ordering => ordering.name)"
					:isOpen="activeFilter === 'ordering'"
					:initialValue="filters.ordering ? getOrderingNameByValue(filters.ordering) || null : null"
					@update:isOpen="setActiveFilter('ordering', $event)"
					@update:value="orderingName =>
						filters.ordering =
							orderingName != null && orderingName !== ''
							? getOrderingValueByName(String(orderingName)) || null
							: null
					"
				/>
			</div>

			<div class="car-list-filters__actions">
				<TextIconButton
					:icon="colorMode === 'dark' ? TickIcon : TickIconDark"
					class="car-list-filters__apply"
					@click="applyFilters"
				>
					Применить
				</TextIconButton>

				<TextIconButton
					:icon="colorMode === 'dark' ? CrossIcon : CrossIconDark"
					class="car-list-filters__flush"
					@click="filters.reset()"
				>
					Сбросить
				</TextIconButton>
			</div>

		</form>
	</block-glass>
</template>

<style scoped>
.car-list-filters {
	display: flex;
	flex-direction: column;
	justify-content: start;

	width: 100%;
	max-width: 450px;
	height: fit-content;

	box-sizing: border-box;
	padding: 10px 25px 25px;
	gap: 5px;
}

h1 {
	color: var(--color-secondary);
	font-weight: bold;
	user-select: none;
}

form {
	display: flex;
	flex-direction: column;
	gap: 5px;
}

form > div {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	gap: 15px;
}

.car-list-filters__year-min,
.car-list-filters__year-max,
.car-list-filters__displacement-min,
.car-list-filters__displacement-max,
.car-list-filters__mileage-min,
.car-list-filters__mileage-max,
.car-list-filters__power-min,
.car-list-filters__power-max,
.car-list-filters__ordering {
	width: 100%;
}

.car-list-filters__actions {
	flex-wrap: wrap;
	justify-content: center;
	gap: 12px 24px;
}

.car-list-filters__apply,
.car-list-filters__flush {
	align-self: center;
	margin-top: 20px;

	font-size: 20px;
	font-weight: 600;
	line-height: 1.2;
	color: var(--color-secondary-90);
}

.car-list-filters__apply :deep(img),
.car-list-filters__flush :deep(img) {
	width: auto;
	height: 22px;
	object-fit: contain;
}

@media (max-width: 900px) {
	.car-list-filters {
		max-width: none;
		padding: 16px 20px 24px;
	}

	h1 {
		font-size: 22px;
		padding-right: 40px;
	}

	form > div {
		flex-wrap: wrap;
		gap: 10px;
	}

	.car-list-filters__apply,
	.car-list-filters__flush {
		margin-top: 12px;
		font-size: 16px;
	}
}
</style>