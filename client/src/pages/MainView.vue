<script setup lang="ts">

import Sector1 from "../components/main-page-sectors/Sector 1.vue"
import Sector2 from "../components/main-page-sectors/Sector 2.vue"
import Sector3 from "../components/main-page-sectors/Sector 3.vue"
import Sector4 from "../components/main-page-sectors/Sector 4.vue"
</script>

<template>
    <div class="mainPage main-page__fade-in">
        <sector-1/>
        <sector-2/>
        <sector-3/>
        <sector-4 id="brand-selection"/>
    </div>
</template>

<style scoped>
.mainPage {
    --safe-x: 0;

    position: relative;

    display: flex;
    flex-direction: column;

    width: 100%;
    max-width: 100%;
    min-width: 0;
    min-height: 0;
    align-items: stretch;

    padding: 100px 0 64px;
    gap: 80px;

    box-sizing: border-box;
}

@media (max-width: 1250px) {
    .mainPage {
        gap: 64px;
    }
}

@media (max-width: 900px) {
    .mainPage {
        padding: 88px 0 56px;
        gap: 48px;
    }
}

@media (max-width: 700px) {
    .mainPage {
        padding: 80px 0 48px;
        gap: 40px;
    }
}

.main-page__fade-in {
	animation: .5s MainPageFadeIn .3s ease-out backwards;
}

@keyframes MainPageFadeIn {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}
</style>
