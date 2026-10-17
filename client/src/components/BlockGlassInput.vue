<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";
import BlockGlass from "./BlockGlass.vue";

const props = withDefaults(
	defineProps<{
		label: string,
		type?: 'text' | 'number',
		isFocused?: boolean,
		initialValue?: string | number | null
	}>(),
	{
		type: 'text',
		isFocused: false
	}
)

const emit = defineEmits<{
	'update:value': [value: string | number | null]
	'update:isFocused': [value: boolean]
}>()

const inputEl = ref<HTMLInputElement | null>(null)
const value = ref<string | number | null>(props.initialValue != null ? props.initialValue : null)

watch(() => props.initialValue, (newValue) => value.value = newValue != null ? newValue : null)

const hasValue = computed(() => value.value !== null && value.value !== '')
const isFilled = computed(() => props.isFocused || hasValue.value)

const inputText = computed(() => {
	if (value.value === null) return ''
	return String(value.value)
})

const setFocused = (focused: boolean) => emit('update:isFocused', focused)

const setValue = (newValue: string | number | null) => {
	value.value = newValue
	emit('update:value', newValue)
}

const focusInput = async () => {
	setFocused(true)
	await nextTick()
	inputEl.value?.focus()
}

const onInput = (event: Event) => {
	const raw = (event.target as HTMLInputElement).value

	if (props.type === 'number') {
		if (raw === '') {
			setValue(null)
			return
		}
		const num = Number(raw)
		if (!Number.isNaN(num)) setValue(num)
		return
	}

	setValue(raw === '' ? null : raw)
}

const onBlur = () => setFocused(false)

watch(() => props.isFocused, async (focused) => {
	if (!focused) {
		inputEl.value?.blur()
		return
	}
	await nextTick()
	inputEl.value?.focus()
})

defineExpose({ value, focusInput })
</script>

<template>
	<div class="block-glass-input-root">
		<div class="block-glass-input" @click="focusInput">
			<Transition
				name="block-glass-input__content__transition"
				mode="out-in"
				@after-enter="props.isFocused && inputEl?.focus()"
			>
				<text v-if="!isFilled" key="empty" class="block-glass-input__label__value-is-null">
					{{ props.label }}
				</text>

				<div v-else key="filled" class="block-glass-input__filled">
					<text class="block-glass-input__label__value-is-not-null">
						{{ props.label }}
					</text>
					<input
						ref="inputEl"
						class="block-glass-input__value"
						:type="props.type"
						:value="inputText"
						@input="onInput"
						@focus="setFocused(true)"
						@blur="onBlur"
						@click.stop
					/>
				</div>
			</Transition>
		</div>
	</div>
</template>

<style scoped>
.block-glass-input-root {
	position: relative;
	width: 100%;
	user-select: none;
}

.block-glass-input {
	width: 100%;
	height: 55px;

	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: start;

	cursor: text;

	box-sizing: border-box;
	padding: 0 25px;

	--background-color: var(--color-primary-30);
	color: var(--color-secondary-70);
}

.block-glass-input__filled {
	display: flex;
	flex-direction: column;
	align-items: start;
	justify-content: center;
	width: 100%;
}

.block-glass-input__label__value-is-not-null {
	font-weight: 300;
	font-size: 12px;
}

.block-glass-input__value {
	all: unset;

	width: 100%;
	box-sizing: border-box;

	color: var(--color-secondary-90);
	cursor: text;
}

.block-glass-input__value[type="number"] {
	appearance: textfield;
	-moz-appearance: textfield;
}

.block-glass-input__value[type="number"]::-webkit-outer-spin-button,
.block-glass-input__value[type="number"]::-webkit-inner-spin-button {
	appearance: none;
	margin: 0;
}

.block-glass-input__content__transition-enter-from,
.block-glass-input__content__transition-leave-to {
	opacity: 0;
	translate: 0 5px;
}

.block-glass-input__content__transition-enter-to,
.block-glass-input__content__transition-leave-from {
	opacity: 1;
	translate: 0 0;
}

.block-glass-input__content__transition-enter-active,
.block-glass-input__content__transition-leave-active {
	transition: opacity .2s ease-out, translate .2s ease-out;
}
</style>
