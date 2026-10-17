<script setup lang="ts">

import { computed, ref } from "vue";

import BlockGlass from "../components/BlockGlass.vue";

import { storeToRefs } from "pinia";
import BlockGlassButton from "../components/BlockGlassButton.vue";
import LoadingAnimation from "../components/LoadingAnimation.vue";
import TextIconButton from "../components/TextIconButton.vue";
import TelegramIcon from "../assets/telegram.svg";
import VkIcon from "../assets/vk.svg";
import PhoneIcon from "../assets/phone.svg";
import ArrowIcon from "../assets/arrow.svg";
import { useStore } from "../stores/Store.ts";
import { useRouter } from "vue-router";

const router = useRouter()

const store = useStore()
const { car, carLoading } = storeToRefs(store)

const socials = [
	{ name: 'Telegram', href: 'https://t.me/omegaautogroup?direct', icon: TelegramIcon },
	{ name: 'ВКонтакте', href: 'https://vk.me/omegaautogroup', icon: VkIcon }
]
const phones = [
	{ label: '+7 (932) 301-89-98', href: 'tel:+79323018998' },
	{ label: '+7 (902) 602-22-77', href: 'tel:+79026022277' },
	{ label: '+7 (922) 700-90-90', href: 'tel:+79227009090' },
]
const currentImageIndex = ref(0)

const goBack = () => router.back()
const numberFormatted = (n: number) => new Intl.NumberFormat("ru-RU").format(Number(n))

const shiftImage = (delta: number) => {
	const imagesCount = car.value?.images?.length ?? 0
	if (!imagesCount) return
	currentImageIndex.value = (currentImageIndex.value + delta + imagesCount) % imagesCount
}

const carSpecs = computed(() => [
	{ key: 'name', label: '', value: `${ car.value?.brand } ${ car.value?.model }` },
	{ key: 'year', label: 'Год', value: car.value?.year },
	{ key: 'mileage', label: 'Пробег', value: `${ numberFormatted(car.value?.mileage || 0) } км` },
	{ key: 'power', label: 'Мощность', value: `${ car.value?.power } л.с.` },
	{ key: 'displacement', label: 'Объем', value: `${ car.value?.displacement } л` },
	{ key: 'gear', label: 'Трансмиссия', value: car.value?.gear },
	{ key: 'color', label: 'Цвет', value: car.value?.color },
	{ key: 'fuel', label: 'Топливо', value: car.value?.fuel },
	{ key: 'price', label: '', value: `${ numberFormatted(car.value?.price || 0) } ¥` },
])
</script>

<template>
	<LoadingAnimation v-if="carLoading || !car" />

	<template v-else>
		<div class="carPage">
			<TextIconButton class="button__go-back" :icon="ArrowIcon" icon-alt="Arrow" @click="goBack">
				К списку автомобилей
			</TextIconButton>

			<div class="card">
				<div class="image-frame image-animation" style="grid-area: image">
					<Transition name="image-frame__background__transition" mode="out-in">
						<img
							:key="`background-${currentImageIndex}`"
							:src="car?.images?.at(currentImageIndex)?.image"
							alt="Car Image"
							class="background"
						/>
					</Transition>
					<Transition name="image-frame__foreground__transition" mode="out-in">
						<img
							:key="`foreground-${currentImageIndex}`"
							:src="car?.images?.at(currentImageIndex)?.image"
							alt="Car Image"
							class="foreground"
						/>
					</Transition>

					<block-glass-button class="gallery-arrow gallery-arrow-left" type="button"
										aria-label="Предыдущее изображение" @click="shiftImage(-1)">
						&#10094;
					</block-glass-button>

					<block-glass-button class="gallery-arrow gallery-arrow-right" type="button"
										aria-label="Следующее изображение" @click="shiftImage(1)">
						&#10095;
					</block-glass-button>
				</div>

				<block-glass class="info right-block-slide-in-animation"
							 style="grid-area: info; animation-delay: .2s"
				>
					<text
						v-for="carSpec in carSpecs"
						:key="carSpec.key"
						:class="carSpec.key"
						:style="{ gridArea: carSpec.key }"
					>
						<span v-if="carSpec.label"><b>{{ carSpec.label }}</b></span>
						<span v-if="carSpec.label">{{ carSpec.value }}</span>
						<span v-else><b>{{ carSpec.value }}</b></span>
					</text>
				</block-glass>

				<div class="gallery" style="grid-area: gallery">
					<div
						class="image-frame gallery-image-slide-in-animation"
						v-for="(image, index) in car?.images" :key="image.index"
						:style="{ animationDelay: `${0.6 + 0.1 * index}s` }"
					>
						<img
							:src="image.image"
							alt="Car Image"
							@click="currentImageIndex = index"
							:style="{ filter: `brightness(${index === currentImageIndex ? '1' : '0.7'})` }"
						/>
					</div>
				</div>

				<block-glass class="links right-block-slide-in-animation"
							 style="grid-area: links; animation-delay: .4s"
				>
					<text>
						<span><b>Понравился автомобиль?</b></span>
						<span>Обратитесь к нам по одному из способов, указанных ниже</span>
					</text>

					<div class="buttons" style="grid-area: buttons">
						<div class="buttons__socials">
							<TextIconButton
								v-for="social in socials"
								:key="social.name"
								:icon="social.icon"
								:icon-alt="social.name"
								:href="social.href"
								target="_blank"
								rel="noopener noreferrer"
							>
								{{ social.name }}
							</TextIconButton>
						</div>

						<div class="buttons__phones">
							<TextIconButton
								v-for="phone in phones"
								:key="phone.label"
								:icon="PhoneIcon"
								icon-alt="Phone"
								:href="phone.href"
							>
								{{ phone.label }}
							</TextIconButton>
						</div>
					</div>
				</block-glass>
			</div>
		</div>
	</template>
</template>

<style scoped>
.carPage {
	position: relative;

	display: flex;
	flex-direction: column;

	box-sizing: border-box;
	padding: 120px 0;
	gap: 20px;
}

.card {
	width: 100%;

	display: grid;
	grid-template-areas:
        "image info"
        "gallery links";
	grid-template-columns: 900px minmax(0, 1fr);
	grid-template-rows: 600px auto;
	grid-column-gap: 50px;
	grid-row-gap: 25px;
}

.image-frame {
	position: relative;

	width: 900px;
	height: 600px;

	box-sizing: border-box;
	border-radius: 30px;

	overflow: hidden;
}

.image-frame img {
	width: 100%;
	height: 100%;

	object-fit: contain;
}

.image-frame .background {
	position: absolute;
	inset: 0;

	width: 100%;
	height: 100%;

	object-fit: cover;
	filter: blur(30px) brightness(0.7);
	transform: scale(1.1);
	z-index: 0;
	pointer-events: none;
}

.image-frame .foreground {
	position: relative;
	z-index: 1;
	display: block;
}

.gallery-arrow {
	position: absolute;
	top: 50%;
	z-index: 2;

	display: flex;
	align-items: center;
	justify-content: center;

	width: 56px;
	height: 56px;
	aspect-ratio: 1;
	border-radius: 50% !important;

	color: rgba(255, 255, 255, 0.9);
	font-size: 32px;
	line-height: 1;
	cursor: pointer;

	transform: translateY(-50%);

	user-select: none;
}

.gallery-arrow-left {
	left: 24px;
}

.gallery-arrow-right {
	right: 24px;
}

.info {
	width: 100%;
	height: 100%;

	display: grid;
	grid-template-areas:
        "name name"
        "year mileage"
        "power displacement"
        "gear color"
        "fuel ."
        "price price";
	grid-template-columns: repeat(2, 1fr);
	grid-template-rows: repeat(6, 1fr);

	padding: 30px 50px;
	box-sizing: border-box;
}

.info text {
	display: flex;
	flex-direction: column;
}

.info text {
	font-size: 24px;
	font-weight: 300;
	color: rgba(255, 255, 255, 0.7);
}

.info text b {
	font-weight: 700;
}

.info .name, .info .price {
	color: rgba(255, 255, 255, 0.9);
	font-size: 48px;
}

.gallery {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	align-self: start;

	width: 900px;
	height: fit-content;
	gap: 10px;

	border-radius: 30px;

	overflow: hidden;
}

.gallery .image-frame {
	width: 172px;
	height: 115px;
	overflow: hidden;
	border-radius: 0;

	box-sizing: border-box;
}

.gallery .image-frame img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.links {
	display: flex;
	flex-direction: column;
	justify-content: start;
	align-items: start;

	height: fit-content;

	gap: 40px;

	box-sizing: border-box;
	padding: 30px 30px;

	font-size: 15px;
	font-weight: 300;
	color: rgba(255, 255, 255, 0.7);

	b {
		font-size: 24px;
		font-weight: 700;
		color: rgba(255, 255, 255, 0.9);
	}
}

.links > text {
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.links .buttons {
	display: flex;
	flex-direction: row;

	width: 100%;
}

.buttons .buttons__phones,
.buttons .buttons__socials {
	display: flex;
	flex-direction: column;
	gap: 15px;
}

.info, .links {
	background-color: var(--color-primary-30);
}

@media (max-width: 1180px) {
	.carPage {
		padding: 120px 24px;
	}

	.card {
		grid-template-areas:
            "image"
            "info"
            "gallery"
            "links";
		grid-template-columns: minmax(0, 1fr);
		grid-template-rows: auto;
		gap: 24px;
	}

	.image-frame {
		width: 100%;
		height: auto;
		aspect-ratio: 3 / 2;
	}

	.info { min-height: 480px; }

	.gallery {
		display: grid;
		grid-template-columns: repeat(5, minmax(0, 1fr));
		width: 100%;
	}

	.gallery .image-frame {
		width: 100%;
		height: auto;
		aspect-ratio: 3 / 2;
	}

	.links { width: 100%; }

	.buttons .buttons__phones,
	.buttons .buttons__socials {
		gap: 10px;
	}
}

@media (max-width: 700px) {
	.carPage {
		max-height: none;
		padding: 100px 16px 100px;
	}

	.card { gap: 16px; }

	.gallery { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }

	.gallery-arrow {
		width: 44px;
		height: 44px;
		font-size: 24px;
	}

	.gallery-arrow-left { left: 12px; }

	.gallery-arrow-right { right: 12px; }

	.info {
		min-height: 430px;
		padding: 20px;
	}

	.info text {
		min-width: 0;
		overflow-wrap: anywhere;
		font-size: clamp(15px, 4vw, 18px);
		color: var(--color-secondary-90);
	}

	.info .name,
	.info .price { font-size: clamp(25px, 8vw, 34px); }

	.links {
		gap: 24px;
		padding: 24px 20px;
		color: var(--color-secondary-90);
	}

	.links .buttons {
		grid-template-columns: 1fr 1fr;
		grid-template-rows: repeat(2, minmax(44px, auto));
		grid-auto-flow: row;
	}

	.buttons .buttons__phones,
	.buttons .buttons__socials {
		gap: 8px;
	}
}

@media (max-width: 480px) {
	.links .buttons {
		grid-template-columns: minmax(0, 1fr);
		grid-template-rows: repeat(4, 44px);
	}

	.buttons .buttons__phones,
	.buttons .buttons__socials {
		gap: 6px;
	}
}

.image-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s imageSlideIn ease-out forwards;
}

.right-block-slide-in-animation {
	opacity: 0;
	will-change: opacity, translate, filter;
	animation: .5s rightBlockSlideIn ease-out forwards;
}

.gallery-image-slide-in-animation {
	opacity: 0;
	will-change: opacity, scale, filter;
	animation: .5s galleryImageFadeIn ease-out forwards;
}

.image-frame__background__transition-enter-from,
.image-frame__background__transition-leave-to,
.image-frame__foreground__transition-enter-from,
.image-frame__foreground__transition-leave-to {
	filter: blur(10px);
	opacity: .5;
}

.image-frame__background__transition-enter-to,
.image-frame__background__transition-leave-from,
.image-frame__foreground__transition-enter-to,
.image-frame__foreground__transition-leave-from {
	filter: blur(0);
	opacity: 1;
}

.image-frame__background__transition-enter-active,
.image-frame__background__transition-leave-active,
.image-frame__foreground__transition-enter-active,
.image-frame__foreground__transition-leave-active {
	transition: filter .15s ease-out, opacity .15s ease-out;
}

@keyframes rightBlockSlideIn {
	from {
		opacity: 0;
		translate: 25px 0;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		translate: 0 0;
		filter: blur(0);
	}
}

@keyframes imageSlideIn {
	from {
		opacity: 0;
		translate: -25px 0;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		translate: 0 0;
		filter: blur(0);
	}
}

@keyframes galleryImageFadeIn {
	from {
		opacity: 0;
		scale: 1.2;
		filter: blur(10px);
	}
	to {
		opacity: 1;
		scale: 1;
		filter: blur(0);
	}
}
</style>
