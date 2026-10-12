<script setup lang="ts">

import { ref } from "vue";
import BlockGlass from "./BlockGlass.vue";
import ButtonShiftingTextWithIcon from "./ButtonShiftingTextWithIcon.vue";
import TelegramIcon from '../assets/telegram.svg'
import VkIcon from '../assets/vk.svg'
import HomeIcon from '../assets/home.svg'
import CarIcon from '../assets/car.svg'
import InfoIcon from '../assets/info.svg'
import { useRouter } from "vue-router";
import CompanyInfo from "./CompanyInfo.vue";

const router = useRouter()

type Page = { name: string, icon: string, action: () => void }
type Social = { name: string, href: string, icon: string }

const pages: Page[] = [
	{
		name: 'Главная',
		icon: HomeIcon,
		action: () => router.push({ name: 'main' })
	},
	{
		name: 'Каталог',
		icon: CarIcon,
		action: () => router.push({ name: 'main', hash: '#brand-selection' })
	},
	{
		name: 'О нас',
		icon: InfoIcon,
		action: () => companyInfo.value?.open()
	}
]

const socials: Social[] = [
	{ name: 'Telegram', href: 'https://t.me/+cL3IltxijBNiNjcy', icon: TelegramIcon },
	{ name: 'ВКонтакте', href: 'https://vk.ru/omegaautogroup', icon: VkIcon }
]

const companyInfo = ref<InstanceType<typeof CompanyInfo> | null>(null)
const menuOpen = ref(false)
</script>

<template>
	<block-glass class="header"
				 style="background-color: var(--color-primary-30)"
				 @keydown.esc="menuOpen = false">
		<span class="omega-auto" @click="router.push({name: 'main'})">OMEGA AUTO</span>

		<div class="header-sector pages">
			<button-shifting-text-with-icon
				v-for="page in pages"
				:key="page.name"
				:icon="page.icon"
				icon-alt=""
				@click="page.action()"
			>
				{{ page.name }}
			</button-shifting-text-with-icon>
		</div>

		<div class="header-sector socials">
			<button-shifting-text-with-icon
				v-for="social in socials"
				:key="social.name"
				:href="social.href || undefined"
				target="_blank"
				rel="noopener noreferrer"
				:icon="social.icon"
				icon-alt=""
			>
				{{ social.name }}
			</button-shifting-text-with-icon>
		</div>

		<button class="menu-toggle"
				type="button"
				:aria-expanded="menuOpen"
				aria-controls="mobile-menu"
				:aria-label="menuOpen ? 'Закрыть меню' : 'Открыть меню'"
				@click="menuOpen = !menuOpen">
			<span></span>
			<span></span>
			<span></span>
		</button>

		<Teleport to="body">
			<block-glass v-if="menuOpen"
						 id="mobile-menu"
						 class="mobile-menu"
						 style="background-color: var(--color-primary-80)">
				<section>
					<span class="menu-heading">Навигация</span>
					<button-shifting-text-with-icon
						v-for="page in pages"
						:key="page.name"
						:icon="page.icon"
						icon-alt=""
						@click="menuOpen = false; page.action()"
					>{{ page.name }}
					</button-shifting-text-with-icon>
				</section>

				<section>
					<span class="menu-heading">Социальные сети</span>
					<button-shifting-text-with-icon
						v-for="social in socials"
						:key="social.name"
						:href="social.href || undefined"
						target="_blank"
						rel="noopener noreferrer"
						:icon="social.icon"
						icon-alt=""
						@click="menuOpen = false"
					>{{ social.name }}
					</button-shifting-text-with-icon>
				</section>
			</block-glass>
		</Teleport>

		<CompanyInfo ref="companyInfo" />
	</block-glass>
</template>

<style scoped>
.header {
	position: fixed;
	z-index: 30;

	inset: 0;
	top: 30px;
	left: 50%;
	transform: translateX(-50%);

	width: 1200px;
	height: 60px;

	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;

	box-sizing: border-box;
	padding: 10px 50px;
	user-select: none;
}

.omega-auto {
	font-size: 20px;
	font-weight: 700;
	color: rgba(255, 255, 255, 1);
	cursor: pointer;
}

.header-sector {
	display: flex;
	align-items: center;
	height: 100%;
}

.menu-toggle,
.mobile-menu {
	display: none;
}

@media (max-width: 1240px) {
	.header {
		width: calc(100vw - 48px);
		padding-inline: 30px;
		background-color: rgba(8, 8, 12, 0.38) !important;
	}
}

@media (max-width: 900px) {
	.header {
		inset: auto;
		top: 16px;
		left: 16px;
		width: calc(100vw - 32px);
		height: 60px;
		padding: 8px 12px 8px 20px;
		transform: none;
		background-color: rgba(8, 8, 12, 0.48) !important;
	}

	.omega-auto {
		font-size: clamp(14px, 4.5vw, 18px);
	}

	.header-sector { display: none; }

	.menu-toggle {
		all: unset;
		display: grid;
		place-content: center;
		grid-template-columns: 24px;
		grid-template-rows: repeat(3, 2px);
		gap: 5px;
		width: 44px;
		height: 44px;
		cursor: pointer;
	}

	.menu-toggle span {
		width: 24px;
		height: 2px;
		border-radius: 2px;
		background: var(--color-secondary-90);
	}

	.menu-toggle:focus-visible {
		outline: 2px solid var(--color-secondary-90);
		outline-offset: 2px;
	}

	.mobile-menu {
		position: fixed;
		top: 88px;
		right: 16px;
		z-index: 31;
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 20px;
		width: min(320px, calc(100vw - 32px));
		max-height: calc(100dvh - 104px);
		overflow-y: auto;
		padding: 20px;
		box-sizing: border-box;
		background-color: rgba(8, 8, 12, .44) !important;
		backdrop-filter: blur(28px) saturate(80%);
	}

	.mobile-menu section {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.menu-heading {
		margin: 0 10px 6px;
		color: var(--color-secondary-80);
		font-size: 13px;
		font-weight: 500;
	}

	.mobile-menu :deep(.button-shifting-text-with-icon) {
		min-height: 44px;
		padding: 0 8px 0 36px;
		color: var(--color-secondary-90);
	}
}
</style>
