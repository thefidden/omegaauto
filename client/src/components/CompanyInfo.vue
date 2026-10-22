<script setup lang="ts">

import { ref } from "vue";
import BlockGlass from "./BlockGlass.vue";

const isOpen = ref(false)
const open = () => isOpen.value = true
const close = () => isOpen.value = false


defineExpose({ open })
</script>

<template>
	<Teleport to="body">
		<Transition name="company-info">
			<div v-if="isOpen"
				 class="company-info"
				 @click.self="close"
				 @keydown.esc="close"
			>
				<block-glass class="company-info__box">
					<h2>ДАННЫЕ О КОМПАНИИ</h2>

					<button
						class="company-info__close"
						@click="close"
					>
						<span></span>
						<span></span>
					</button>

					<div class="company-info__text">
						<span>ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ОМЕГА", ИНН 7456062662</span>
						<div></div>
						<span>Электронный ресурс не является публичной офертой и носит информационный и ознакомительный характер</span>
					</div>
				</block-glass>
			</div>
		</Transition>
	</Teleport>
</template>

<style scoped>
.company-info {
	display: grid;
	place-items: center;

	position: fixed;
	inset: 0;
	z-index: 10000;

	background-color: var(--color-primary-50);
	backdrop-filter: blur(10px);

	user-select: none;
}

.company-info__box {
	display: flex;
	flex-direction: column;
	justify-content: start;
	align-items: start;

	box-sizing: border-box;
	padding: 25px 50px;
}

.company-info__text {
	display: flex;
	flex-direction: column;
	justify-content: start;
	align-items: start;
}

.company-info__box h2 {
	color: var(--color-secondary-90);
}

.company-info__text {
	color: var(--color-secondary-70);
}

.company-info__close {
	position: absolute;
	top: 18px;
	right: 18px;

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

.company-info__close span {
	position: absolute;

	background-color: var(--color-secondary);

	box-sizing: border-box;
	border-radius: 2px;

	width: 25px;
	height: 5px;
}

.company-info__close:hover {
	opacity: .5;
}

.company-info__close span:first-child { rotate: 45deg; }

.company-info__close span:last-child { rotate: -45deg; }

.company-info-enter-from,
.company-info-leave-to {
	opacity: 0;
	filter: blur(10px);
	scale: 1.2;
}

.company-info-enter-to,
.company-info-leave-from {
	opacity: 1;
	filter: blur(0);
	scale: 1;
}

.company-info-enter-active,
.company-info-leave-active {
	transition: opacity .3s ease-out, filter .3s ease-out, scale .3s ease-out;
}
</style>