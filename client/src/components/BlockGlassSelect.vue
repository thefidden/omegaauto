<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, watch, type ComponentPublicInstance } from "vue";
import BlockGlass from "./BlockGlass.vue";
import TextIconButton from "./TextIconButton.vue";
import ArrowIcon from "../assets/angle-arrow-down.svg"
import TickIcon from "../assets/tick.svg"
import CrossIcon from "../assets/cross.svg"

const props = withDefaults(
	defineProps<{
		values: string[] | number[],
		label: string,
		isOpen?: boolean,
		initialValue?: string | number | null
	}>(),
	{
		isOpen: false
	})

const emit = defineEmits<{
	'update:value': [value: null | string | number]
	'update:isOpen': [value: boolean]
}>()

const trigger = ref<HTMLElement | null>(null)
const menu = ref<ComponentPublicInstance | null>(null)
const value = ref<string | number | null>(props.initialValue != null ? props.initialValue : null)
const menuStyle = ref<Record<string, string>>({})

watch(() => props.initialValue, (newValue) => {
	value.value = newValue != null ? newValue : null
})

const setValue = (newValue: null | string | number) => {
	value.value = newValue
	emit('update:value', newValue)
	setOpen(false)
}

const setOpen = (newValue: boolean) => emit('update:isOpen', newValue)

const updateMenuPosition = () => {
	const el = trigger.value
	if (!el) return

	const rect = el.getBoundingClientRect()
	const gap = 10
	const edge = 16
	const preferredMax = 300
	const spaceBelow = window.innerHeight - rect.bottom - gap - edge
	const spaceAbove = rect.top - gap - edge
	const openUp = spaceBelow < Math.min(preferredMax, 180) && spaceAbove > spaceBelow
	const available = Math.max(120, openUp ? spaceAbove : spaceBelow)
	const maxHeight = Math.min(preferredMax, available)

	const left = Math.min(
		Math.max(edge, rect.left),
		window.innerWidth - edge - Math.min(rect.width, window.innerWidth - edge * 2)
	)
	const width = Math.min(rect.width, window.innerWidth - edge * 2)

	menuStyle.value = openUp
		? {
			position: 'fixed',
			top: 'auto',
			bottom: `${ window.innerHeight - rect.top + gap }px`,
			left: `${ left }px`,
			width: `${ width }px`,
			maxHeight: `${ maxHeight }px`,
			zIndex: '10050',
		}
		: {
			position: 'fixed',
			top: `${ rect.bottom + gap }px`,
			bottom: 'auto',
			left: `${ left }px`,
			width: `${ width }px`,
			maxHeight: `${ maxHeight }px`,
			zIndex: '10050',
		}
}

const onPointerDownOutside = (event: PointerEvent) => {
	const target = event.target as Node | null
	if (!target) return

	const menuEl = menu.value?.$el as HTMLElement | undefined
	const insideTrigger = trigger.value?.contains(target)
	const insideMenu = menuEl?.contains(target)
	if (insideTrigger || insideMenu) return

	setOpen(false)
}

watch(() => props.isOpen, async (open) => {
	if (!open) {
		document.removeEventListener('pointerdown', onPointerDownOutside, true)
		return
	}
	await nextTick()
	updateMenuPosition()
	requestAnimationFrame(updateMenuPosition)
	document.addEventListener('pointerdown', onPointerDownOutside, true)
})

const onReposition = () => {
	if (props.isOpen) updateMenuPosition()
}

window.addEventListener('resize', onReposition)
window.addEventListener('scroll', onReposition, true)
onBeforeUnmount(() => {
	window.removeEventListener('resize', onReposition)
	window.removeEventListener('scroll', onReposition, true)
	document.removeEventListener('pointerdown', onPointerDownOutside, true)
})

defineExpose({ value })
</script>

<template>
	<div ref="trigger" class="block-glass-select-root">
		<div class="block-glass-select" @click="setOpen(!props.isOpen)">
			<Transition name="block-glass-select__content__transition" mode="out-in">
				<text
					v-if="value === null"
					class="block-glass-select__label__value-is-null"
				>
					{{ props.label }}
				</text>

				<div v-else class="block-glass-select__filled">
					<text class="block-glass-select__label__value-is-not-null">
						{{ props.label }}
					</text>
					<Transition name="block-glass-select__value__transition" mode="out-in">
						<text class="block-glass-select__value" :key="value">{{ value }}</text>
					</Transition>
				</div>
			</Transition>

			<img :src="ArrowIcon" alt="arrow" :style="{
				rotate: props.isOpen ? '180deg' : '0deg'
			}" />
		</div>
	</div>

	<Teleport to="body">
		<Transition name="values__transition" mode="out-in">
			<block-glass
				v-if="props.isOpen"
				ref="menu"
				class="values"
				:style="menuStyle"
				@click.stop
			>
				<div class="values__scroll">
					<text-icon-button :icon="CrossIcon" @click="setValue(null)">Сбросить</text-icon-button>
					<text-icon-button
						v-for="valueFor in values"
						:icon="valueFor === value ? TickIcon : ''"
						@click="setValue(valueFor)"
					>
						{{ valueFor }}
					</text-icon-button>
				</div>
			</block-glass>
		</Transition>
	</Teleport>
</template>

<style scoped>
.block-glass-select-root {
	position: relative;

	width: 100%;
	user-select: none;
}

.block-glass-select {
	width: 100%;
	height: 55px;

	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: start;

	cursor: pointer;

	box-sizing: border-box;
	padding: 0 25px;

	--background-color: var(--color-primary-30);
	color: var(--color-secondary-70);
}

.block-glass-select__filled {
	display: flex;
	flex-direction: column;
	align-items: start;
	justify-content: center;
}

.block-glass-select__label__value-is-not-null {
	left: 20px;
	top: 5px;

	font-weight: 300;
	font-size: 12px;
}

.block-glass-select__value {
	color: var(--color-secondary-90);
}

.values {
	--background-color: var(--color-primary-30);

	display: flex;
	flex-direction: column;
	align-items: stretch;

	box-sizing: border-box;
	padding: 15px;

	max-height: 300px;
	overflow: hidden;
}

.values__scroll {
	display: flex;
	flex-direction: column;
	flex: 1 1 auto;
	gap: 10px;

	width: 100%;
	min-height: 0;
	overflow-x: hidden;
	overflow-y: auto;
	-webkit-overflow-scrolling: touch;

	scrollbar-width: thin;
	scrollbar-color: rgba(255, 255, 255, .7) transparent;
}

.values__scroll::-webkit-scrollbar {
	width: 4px;
}

.values__scroll::-webkit-scrollbar-track {
	background: transparent;
}

.values__scroll::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, .7);
	border-radius: 999px;
}

img {
	position: absolute;
	right: 20px;
	transition: rotate .2s ease-out;
}

.values__transition-enter-from,
.values__transition-leave-to {
	opacity: 0;
	translate: 0 -10px;
}

.values__transition-enter-to,
.values__transition-leave-from {
	opacity: 1;
	translate: 0 0;
}

.values__transition-enter-active,
.values__transition-leave-active {
	transition: opacity .2s ease-out, translate .2s ease-out;
}

.block-glass-select__value__transition-enter-from,
.block-glass-select__value__transition-leave-to,
.block-glass-select__content__transition-enter-from,
.block-glass-select__content__transition-leave-to {
	opacity: 0;
	translate: 0 5px;
}

.block-glass-select__value__transition-enter-to,
.block-glass-select__value__transition-leave-from,
.block-glass-select__content__transition-enter-to,
.block-glass-select__content__transition-leave-from {
	opacity: 1;
	translate: 0 0;
}

.block-glass-select__value__transition-enter-active,
.block-glass-select__value__transition-leave-active,
.block-glass-select__content__transition-enter-active,
.block-glass-select__content__transition-leave-active {
	transition: opacity .2s ease-out, translate .2s ease-out;
}
</style>
