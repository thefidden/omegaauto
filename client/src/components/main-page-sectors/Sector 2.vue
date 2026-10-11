<script setup lang="ts">
import CarFrontView from "../../assets/car-front-view.png"
import BlockGlass from "../BlockGlass.vue";
import BlockGlassButton from "../BlockGlassButton.vue";
import TelegramIcon from "../../assets/telegram.svg"
import VkIcon from "../../assets/vk.svg"
import PhoneIcon from "../../assets/phone.svg"

const socials = [
    { name: 'Telegram', href: 'https://t.me/+cL3IltxijBNiNjcy', icon: TelegramIcon },
    { name: 'ВКонтакте', href: 'https://vk.ru/omegaautogroup', icon: VkIcon }
]

const phones = ['+7 (932) 301-89-98', "+7 (902) 602-22-77", "+7 (922) 700-90-90"]

const goToSocial = (url: string) => { window.open(url, '_blank') }
const getPhoneHref = (phone: string) => `tel:${phone.replace(/[^\d+]/g, '')}`
const callPhone = (phone: string) => { window.location.href = getPhoneHref(phone) }
</script>

<template>
    <div class="sector2">
        <div class="grid">
            <div class="socials">
                <block-glass class="cell heading" style="--background-color: var(--color-secondary-7)">Наши соцсети</block-glass>

                <block-glass-button class="cell" v-for="social in socials" :key="social.name"
                                    @click="goToSocial(social.href)">
                    <img :src="social.icon" alt="Telegram"/>
                    {{social.name}}
                </block-glass-button>
            </div>

            <div class="phones">
                <block-glass class="cell heading" style="--background-color: var(--color-secondary-7)">Телефон</block-glass>

                <block-glass-button class="cell" v-for="phone in phones" :key="phone"
                                    @click="callPhone(phone)">
                    <img :src="PhoneIcon" alt="Phone"/>
                    {{phone}}
                </block-glass-button>
            </div>

            <img class="picture" :src="CarFrontView" alt="CarInterface Front View"/>
        </div>
    </div>
</template>

<style scoped>
.sector2 {
    position: relative;

    display: flex;
    justify-content: center;
    align-items: center;

    width: 100%;
    height: 800px;
}

.grid {
    display: grid;
    grid-template-areas:
        "socials picture"
        "phones picture";
    grid-template-columns: 1fr 2fr;
    grid-gap: 50px;

    width: 100%;
}

.cell {
    display: flex;
    justify-content: center;
    align-items: center;

    font-weight: 300;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.7);
}

.heading {
    font-weight: 700;
    font-size: 40px;
    color: rgba(255, 255, 255, 0.9);
}

.cell img {
    position: absolute;
    left: 5%;
}

.socials {
    grid-area: socials;
}

.phones {
    grid-area: phones;
}

.socials {
    display: grid;
    grid-template-rows: 2fr repeat(2, 1fr);
    grid-template-columns: 1fr;
    grid-gap: 20px;
}

.phones {
	display: grid;
	grid-template-rows: 2fr repeat(3, 1fr);
	grid-template-columns: 1fr;
	grid-gap: 20px;
}

.picture {
    grid-area: picture;

    width: 100%;
    height: 100%;
}

@media (max-width: 1000px) {
    .grid {
        grid-template-columns: minmax(280px, 1fr) minmax(0, 1.5fr);
        grid-gap: 50px;
    }
}

@media (max-width: 700px) {
    .sector2 {
        height: auto;
        min-height: 760px;
        padding: 40px 16px;
        box-sizing: border-box;
    }

    .grid {
        grid-template-areas:
            "socials"
            "phones"
            "picture";
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: repeat(3, auto);
        gap: 30px;
    }

    .socials, .phones { gap: 12px; }

    .socials, .phones { min-height: 230px; }

    .cell { min-height: 54px; font-size: 16px; color: var(--color-secondary-90); }

    .heading { font-size: 28px; }

    .picture { width: min(100%, 380px); justify-self: center; }
}
</style>
