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

    box-shadow: inset 0 0 10px 1px var(--color-secondary-30);
    mix-blend-mode: darken;

    pointer-events: none;
    z-index: -1;
}

.block-glass::after {
    content: "";

    position: absolute;
    inset: 0;

    border-radius: inherit;

    box-shadow: 0 0 5px 1px var(--color-secondary-10);
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
        --background-color: var(--color-secondary-7);
        background-color: var(--color-primary-20);
    }

    .block-glass::before {
        background:
            linear-gradient(135deg, var(--color-secondary-10), var(--color-secondary-5)),
            var(--background-color);
        border-color: var(--color-secondary-50);
        box-shadow: inset 0 1px 1px var(--color-secondary-20), inset 0 0 18px var(--color-secondary-10);
        mix-blend-mode: normal;
    }

    .block-glass::after {
        box-shadow: 0 12px 30px var(--color-primary-20), 0 0 20px var(--color-secondary-20);
        mix-blend-mode: normal;
    }
}
</style>
