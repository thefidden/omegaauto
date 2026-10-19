<script setup lang="ts">
import EarthIcon from "../../assets/earth.svg"
import SearchIcon from "../../assets/search.svg"
import ShieldIcon from "../../assets/shield.svg"
import DeliveryIcon from "../../assets/delivery.svg"
import CarHighAngleView from "../../assets/car-high-angle-view.webp"
import BlockGlass from "../BlockGlass.vue"
</script>

<template>
    <div class="sector3">
        <img class="carHighAngleView" :src="CarHighAngleView" alt="" aria-hidden="true" v-for="index in 2" :key="index"/>

        <block-glass class="cell heading" style="--background-color: var(--color-secondary-20);">
            Наши преимущества
        </block-glass>

        <block-glass class="cell brands">
            <img :src="EarthIcon" alt=""/>
            <div class="name">Автомобили любых производителей</div>
            <div class="description">
                <span>Подберём автомобиль любой марки: китайской, европейской, японской, корейской или другой</span>
            </div>
        </block-glass>

        <block-glass class="cell review">
            <img :src="ShieldIcon" alt=""/>
            <div class="name">Юридическая и техническая проверка</div>
            <div class="description">
                <span>Проверим историю, документы и техническое состояние автомобиля</span>
            </div>
        </block-glass>

        <block-glass class="cell search">
            <img :src="SearchIcon" alt=""/>
            <div class="name">Тщательный подбор под запросы</div>
            <div class="description">
                <span>Подберём автомобиль нужной марки, модели и комплектации</span>
            </div>
        </block-glass>

        <block-glass class="cell escort">
            <img :src="DeliveryIcon" alt=""/>
            <div class="name">Сопровождение до получения</div>
            <div class="description">
                <span>Организуем процесс покупки, доставки и передачи автомобиля вам</span>
            </div>
        </block-glass>
    </div>
</template>

<style scoped>
.sector3 {
    position: relative;

    width: 100%;
    max-width: 100%;
    min-width: 0;
    height: auto;
    min-height: 0;

    display: grid;
    grid-template-areas:
        ". header header ."
        "brands brands search search"
        "review review escort escort";
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-template-rows: auto;
    grid-gap: 48px 40px;

    justify-items: stretch;
    align-items: stretch;

    box-sizing: border-box;
    padding: 24px 24px 48px;
    overflow: visible;
}

.cell {
    position: relative;

    width: 100%;
    min-width: 0;
    height: auto;
    min-height: 220px;

    display: grid;
    grid-template-areas:
        "icon name"
        "description description";
    grid-template-columns: 72px minmax(0, 1fr);
    grid-template-rows: auto auto;
    gap: 16px 20px;
    justify-items: end;
    align-items: start;

    box-sizing: border-box;
    padding: 28px;

    text-align: end;
}

.cell img {
    grid-area: icon;

    position: relative;
    justify-self: start;
    align-self: start;

    display: block;
    width: auto;
    height: auto;
    max-width: 56px;
    max-height: 56px;
    object-fit: contain;
}

.cell .name {
    grid-area: name;

    min-width: 0;
    max-width: 100%;

    font-weight: 700;
    font-size: clamp(18px, 1.7vw, 24px);
    line-height: 1.25;
    color: rgba(255, 255, 255, 0.9);

    overflow-wrap: break-word;
    word-break: normal;
    hyphens: manual;
}

.cell .description {
    grid-area: description;

    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
    max-width: 100%;
    line-height: 1.35;

    font-weight: 400;
    font-size: clamp(16px, 1.5vw, 22px);
    color: rgba(255, 255, 255, 0.7);

    overflow-wrap: break-word;
    word-break: normal;
}

.heading {
    grid-area: header;

    width: min(750px, 100%);
    max-width: 100%;
    height: auto;
    min-height: 100px;

    font-weight: 700;
    font-size: clamp(28px, 3vw, 40px);
    color: rgba(255, 255, 255, 0.9);
    text-align: center;

	background-color: var(--color-primary-30);

    display: flex;
    justify-content: center;
    align-items: center;

    box-sizing: border-box;
    padding: 20px 24px;
    justify-self: center;


}

.brands { grid-area: brands; }
.search { grid-area: search; }
.review { grid-area: review; }
.escort { grid-area: escort; }

.carHighAngleView {
    position: absolute;
    z-index: 0;
    display: block;

    width: min(480px, 36vw);
    height: auto;
    object-fit: contain;
    pointer-events: none;
    opacity: 0.85;
}

.cell,
.heading {
    position: relative;
    z-index: 1;
}

.carHighAngleView:nth-child(1) {
    left: auto;
    right: 0;
    top: 48%;
    rotate: 180deg;
}

.carHighAngleView:nth-child(2) {
    left: 0;
    top: 36%;
}

@media (max-width: 1250px) {
    .sector3 {
        grid-template-areas:
            "header header"
            "brands search"
            "review escort";
        grid-template-columns: repeat(2, minmax(0, 1fr));
        grid-gap: 28px;
        padding: 32px 24px 40px;
    }

    .heading {
        width: 100%;
        min-height: 88px;
        font-size: clamp(24px, 3.5vw, 34px);
    }

    .cell {
        min-height: 200px;
        padding: 24px;
        grid-template-columns: 56px minmax(0, 1fr);
    }

    .cell .name,
    .cell .description {
        font-size: clamp(16px, 1.8vw, 20px);
    }

    .carHighAngleView {
        width: min(300px, 34vw);
        opacity: 0.4;
    }
}

@media (max-width: 900px) {
    .sector3 {
        grid-template-areas:
            "header"
            "brands"
            "review"
            "search"
            "escort";
        grid-template-columns: minmax(0, 1fr);
        gap: 18px;
        padding: 28px 16px 32px;
    }

    .heading {
        min-height: 80px;
        font-size: clamp(22px, 6vw, 28px);
        padding: 16px;
    }

    .cell {
        min-height: 0;
        padding: 20px;
        grid-template-columns: 48px minmax(0, 1fr);
        gap: 12px 14px;
        justify-items: start;
        text-align: start;
    }

    .cell img {
        max-width: 40px;
        max-height: 40px;
    }

    .cell .name {
        font-size: 18px;
    }

    .cell .description {
        font-size: 15px;
        line-height: 1.45;
        gap: 6px;
        color: var(--color-secondary-90);
    }

    .carHighAngleView {
        width: min(200px, 50vw);
        opacity: 0.2;
    }

    .carHighAngleView:nth-child(1) {
        top: 24%;
        right: 0;
    }

    .carHighAngleView:nth-child(2) {
        top: 62%;
        left: 0;
    }
}
</style>
