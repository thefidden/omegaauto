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
                    <img :src="social.icon" alt=""/>
                    {{ social.name }}
                </block-glass-button>
            </div>

            <div class="phones">
                <block-glass class="cell heading" style="--background-color: var(--color-secondary-7)">Телефон</block-glass>

                <block-glass-button class="cell" v-for="phone in phones" :key="phone"
                                    @click="callPhone(phone)">
                    <img :src="PhoneIcon" alt=""/>
                    {{ phone }}
                </block-glass-button>
            </div>

            <img class="picture" :src="CarFrontView" alt="Автомобиль, вид спереди"/>
        </div>
    </div>
</template>

<style scoped>
.sector2 {
    --safe-x: 24px;

    position: relative;

    display: flex;
    justify-content: center;
    align-items: center;

    width: 100%;
    max-width: 100%;
    min-width: 0;
    height: auto;
    min-height: 0;

    box-sizing: border-box;
    padding: 40px var(--safe-x);
}

.grid {
    display: grid;
    grid-template-areas:
        "socials picture"
        "phones picture";
    grid-template-columns: minmax(0, 1fr) minmax(0, 2fr);
    grid-gap: 40px;

    width: 100%;
    max-width: 1200px;
    min-width: 0;
    align-items: center;
}

.cell {
    position: relative;

    display: flex;
    justify-content: center;
    align-items: center;

    box-sizing: border-box;
    padding: 12px 16px 12px 48px;
    min-height: 56px;
    min-width: 0;

    font-weight: 300;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    overflow-wrap: break-word;
    word-break: normal;
}

.heading {
    padding: 16px 20px;
    font-weight: 700;
    font-size: clamp(24px, 3.2vw, 40px);
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.15;
}

.cell img {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);

    display: block;
    width: auto;
    height: 22px;
    object-fit: contain;
}

.socials {
    grid-area: socials;

    display: grid;
    grid-template-rows: auto;
    grid-template-columns: minmax(0, 1fr);
    grid-gap: 16px;
    min-width: 0;
}

.phones {
    grid-area: phones;

    display: grid;
    grid-template-rows: auto;
    grid-template-columns: minmax(0, 1fr);
    grid-gap: 16px;
    min-width: 0;
}

.picture {
    grid-area: picture;

    display: block;
    width: 100%;
    max-width: 100%;
    height: auto;
    object-fit: contain;
    object-position: center;

    justify-self: center;
    align-self: center;
}

@media (max-width: 1100px) {
    .sector2 {
        --safe-x: 24px;
    }

    .grid {
        grid-template-columns: minmax(0, 1fr) minmax(0, 1.35fr);
        grid-gap: 28px;
    }

    .cell {
        font-size: 18px;
        padding-left: 44px;
    }

    .cell img {
        left: 14px;
        height: 20px;
    }
}

@media (max-width: 900px) {
    .sector2 {
        --safe-x: 16px;
        padding-block: 32px;
    }

    .grid {
        grid-template-areas:
            "socials"
            "phones"
            "picture";
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: auto;
        gap: 28px;
    }

    .socials,
    .phones {
        gap: 12px;
    }

    .cell {
        min-height: 54px;
        font-size: 16px;
        color: var(--color-secondary-90);
    }

    .heading {
        font-size: clamp(22px, 6vw, 28px);
        padding: 14px 16px;
    }

    .picture {
        width: min(100%, 420px);
        height: auto;
    }
}

@media (max-width: 700px) {
    .sector2 {
        --safe-x: 16px;
        padding-block: 28px;
    }

    .grid {
        gap: 24px;
    }

    .cell {
        padding: 12px 14px 12px 44px;
    }

    .cell img {
        left: 12px;
        height: 18px;
    }

    .picture {
        width: min(100%, 360px);
    }
}
</style>
