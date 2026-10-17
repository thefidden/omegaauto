import { createWebHistory, createRouter, type RouteLocationNormalized } from 'vue-router'
import MainView from "./pages/MainView.vue";
import CarListView from "./pages/CarListView.vue";
import CarView from "./pages/CarView.vue";
import { storeToRefs } from "pinia";
import { useStore } from "./stores/Store.ts";
import { watch } from "vue";
import { smoothScrollTo } from "./utils/smoothScroll.ts";
import { useCarListFilters } from "./stores/CarListFiltersStore.ts";

type PendingScroll = {
    left: number
    top: number
} | {
    hash: string
}

let pendingScroll: PendingScroll | null = null

export function takePendingScroll() {
    const scroll = pendingScroll
    pendingScroll = null
    return scroll
}

const router = createRouter({
    history: createWebHistory(),

    scrollBehavior(to, from, savedPosition) {
        // Hash must win over savedPosition: beforeEach scrolls to top before
        // leaving a page, so back-navigation often restores { top: 0 } and
        // would otherwise skip targets like #brand-selection.
        pendingScroll = to.hash
            ? { hash: to.hash }
            : savedPosition
                ? { left: savedPosition.left, top: savedPosition.top }
                : { left: 0, top: 0 }

        return false
    },

    routes: [
        {
            path: '/',
            component: MainView,
            name: 'main',
            beforeEnter: async (route: RouteLocationNormalized) => {
                document.title = 'Omega Auto'
            }
        },

        {
            path: '/cars/',
            component: CarListView,
            name: 'car-list'
        },

        {
            path: '/cars/:id',
            component: CarView,
            name: 'car',
            props: (route: RouteLocationNormalized) => ({
                id: route.params.id
            }),
            beforeEnter: async (route: RouteLocationNormalized) => {
                const store = useStore()
                const { carID, car } = storeToRefs(store)
                carID.value = route.params.id as string

                watch(car, () => {
                    if (car)
                        document.title = `${ car.value?.brand || '' } ${ car.value?.model || '' }`.trim()
                })
            }
        }
    ]
})

router.beforeEach(async (to, from) => {
    if (from.name && to.path !== from.path)
        await smoothScrollTo(window.scrollX, 0)
})

export default router