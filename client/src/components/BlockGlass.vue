<script setup lang="ts">

</script>

<template>
    <div class="block-glass">
        <slot/>
    </div>
</template>

<style scoped>
.block-glass {
    --background-color: #00000000;

    position: relative;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 30px;

    isolation: isolate;
    background-color: transparent;

    backdrop-filter: blur(13px);
}

.block-glass::before {
    content: "";

    position: absolute;
    inset: 0;

    border-radius: inherit;

    background-color: var(--background-color);
    border: 1px solid var(--color-secondary-50);

    box-shadow: inset 0 0 10px 1px var(--color-secondary-50);
    mix-blend-mode: darken;

    pointer-events: none;
    z-index: -1;
}

.block-glass::after {
    content: "";

    position: absolute;
    inset: 0;

    border-radius: inherit;

    box-shadow: 0 0 20px 1px rgba(222, 220, 228, .4);
    mix-blend-mode: darken;

    pointer-events: none;
    z-index: -2;
}

@media (max-width: 1250px) {
    .block-glass {
        background-color: var(--color-primary-60);
    }
}

@media (max-width: 900px) {
    .block-glass {
        --background-color: rgba(222, 220, 228, 0.07);
        background-color: rgba(8, 8, 12, 0.24);
    }

    .block-glass::before {
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.025)),
            var(--background-color);
        border-color: rgba(222, 220, 228, 0.46);
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.2), inset 0 0 18px rgba(222, 220, 228, 0.14);
        mix-blend-mode: normal;
    }

    .block-glass::after {
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18), 0 0 20px rgba(222, 220, 228, 0.2);
        mix-blend-mode: normal;
    }
}
</style>
