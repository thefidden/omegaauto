<script setup lang="ts">

import chinaMap from "../../assets/china-map.svg";
import russiaMap from "../../assets/russia-map.svg";
import lineGradient from "../../assets/line-gradient.svg";
import carSideView from "../../assets/car-side-view.png";
import BlockGlass from "../BlockGlass.vue";
import BlockGlassButton from "../BlockGlassButton.vue";
import { useRouter } from "vue-router";

const router = useRouter()
const goToBrandSelection = () => {
    router.push({ name: 'main', hash: '#brand-selection' })
}
</script>

<template>
    <div class="sector1">
        <img :src="carSideView" alt="CarInterface Side View" class="carSideView"/>

        <div class="grid">
            <block-glass class="china" style="--background-color: var(--color-secondary-7)">
                <img :src="chinaMap" alt="China" class="flag"/>
            </block-glass>

            <block-glass class="russia" style="--background-color: var(--color-secondary-7)">
                <img :src="russiaMap" alt="Russia" class="flag"/>
            </block-glass>

            <block-glass class="import" style="--background-color: var(--color-secondary-7)">
                <span>Импорт автомобилей</span>
                <span>из <b>Китая</b> в <b>Россию</b></span>
            </block-glass>

            <block-glass-button class="go-to-store" @click="goToBrandSelection()">
                <img :src="lineGradient" alt="Line Gradient" class="lineGradient"/>
                Перейти к каталогу
                <img :src="lineGradient" alt="Line Gradient" class="lineGradient"/>
            </block-glass-button>
        </div>
    </div>
</template>

<style scoped>
.sector1 {
    position: relative;

    display: flex;
    flex-direction: column;
    align-items: center;

    width: 100%;
    height: 800px;

    box-sizing: border-box;

    padding: 50px 0;
}

.grid {
    display: grid;
    grid-gap: 50px;
    grid-template-columns: 0.75fr 5fr 0.75fr;
    grid-template-rows: 2fr 1fr;
    grid-template-areas:
        "china import russia"
        "store store store";

    width: 950px;
    height: 225px;

    align-items: center;
    justify-items: center;
}

.grid .import {
    grid-area: import;

    width: 100%;
    height: 100%;
}

.grid .go-to-store {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;

    width: 100%;
    height: 100%;

    gap: 50px;

    grid-area: store;

    .lineGradient {
        opacity: 80%;
    }

    .lineGradient:nth-child(2) {
        rotate: 180deg;
    }
}

.grid .china {
    grid-area: china;
    width: 100px;
    height: 100px;
}

.grid .russia {
    grid-area: russia;
    width: 100px;
    height: 100px;
}

.flag {
    display: block;
    width: 68%;
    height: 68%;
    object-fit: contain;
}

.import {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 6px;

    color: rgb(255, 255, 255, 0.7);
    font-size: 40px;
    line-height: 1.1;

    text-align: center;

    b {
        color: rgb(255, 255, 255, 0.9)
    }
}

.go-to-store {
    color: rgb(255, 255, 255, 0.7);
    font-size: 20px;
    font-weight: 700;

    text-align: center;
}

.carSideView {
    position: absolute;

    top: 224px;
    left: 50%;

    transform: translateX(-50%);

    max-width: 95%;
}

.go-to-store {
    img {
        will-change: transform, opacity;
        transition: transform 0.3s ease-out, opacity 0.3s ease-out;
    }
}

.go-to-store:hover {
    .lineGradient:nth-child(1) {
        opacity: 0;
        transform: translateX(-25px);
    }

    .lineGradient:nth-child(2) {
        opacity: 0;
        transform: translateX(-25px);
    }
}

@media (max-width: 1100px) {
    .grid {
        width: min(86vw, 850px);
        grid-gap: 30px;
    }

    .import { font-size: clamp(28px, 4vw, 36px); }
}

@media (max-width: 700px) {
    .sector1 {
        height: 650px;
        padding-top: 110px;
    }

    .grid {
        grid-template-columns: 64px minmax(0, 1fr) 64px;
        grid-template-rows: minmax(128px, auto) 60px;
        width: 100%;
        height: auto;
        column-gap: 24px;
        row-gap: 22px;
        padding: 0 16px;
        box-sizing: border-box;
    }

    .grid .china,
    .grid .russia {
        width: 64px;
        height: 64px;
    }

    .flag { width: 62%; height: 62%; }

    .import {
        padding: 12px;
        font-size: clamp(20px, 6.5vw, 27px);
    }

    .grid .go-to-store {
        min-height: 60px;
        gap: 14px;
        font-size: 16px;
    }

    .go-to-store .lineGradient { width: min(18vw, 68px); }

    .carSideView {
        top: 360px;
        width: calc(100% - 32px);
        max-width: 560px;
    }
}
</style>
