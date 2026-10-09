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
    position: relative;

    display: flex;
    flex-direction: column;

    min-height: 3700px;
    align-items: center;

    padding: 100px 0;
    gap: 100px;

    box-sizing: border-box;
}

@media (max-width: 1100px) {
    .mainPage {
        height: auto;
        min-height: 3700px;
    }
}

@media (max-width: 700px) {
    .mainPage {
        padding: 80px 0 120px;
        gap: 80px;
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
