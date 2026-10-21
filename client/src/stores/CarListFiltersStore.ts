import { defineStore } from "pinia";
import type { CarListFilterSet } from "../interfaces/CarListFilterSet.ts";
import type { LocationQuery } from "vue-router";
import router from "../router.ts";

export type CarListOrdering =
    | 'brand' | '-brand'
    | 'year' | '-year'
    | 'displacement' | '-displacement'
    | 'mileage' | '-mileage'
    | 'power' | '-power'
    | 'price_total_rub' | '-price_total_rub'

export const useCarListFilters = defineStore('car-list-filters', {
    state: (): CarListFilterSet => ({
        brand: null,
        gear: null,
        color: null,
        fuel: null,
        yearMin: null,
        yearMax: null,
        displacementMin: null,
        displacementMax: null,
        mileageMin: null,
        mileageMax: null,
        powerMin: null,
        powerMax: null,
        ordering: null,
        page: 1
    }),

    actions: {
        validate(): boolean {
            try {
                if (
                    this.yearMin != null &&
                    this.yearMax != null &&
                    this.yearMin > this.yearMax
                )
                    throw new Error(`Поле "Год, от" не должно быть больше поля "Год, до"`)

                else if (
                    this.displacementMin != null &&
                    this.displacementMax != null &&
                    this.displacementMin > this.displacementMax
                )
                    throw new Error(`Поле "Объем, от" не должно быть больше поля "Объем, до"`)

                else if (
                    this.mileageMin != null &&
                    this.mileageMax != null &&
                    this.mileageMin > this.mileageMax
                )
                    throw new Error(`Поле "Пробег, от" не должно быть больше поля "Пробег, до"`)

                else if (
                    this.powerMin != null &&
                    this.powerMax != null &&
                    this.powerMin > this.powerMax
                )
                    throw new Error(`Поле "Мощность, от" не должно быть больше поля "Мощность, до"`)
            }
            catch (e) {
                alert(e)
                return false
            }

            return true
        },

        fetchFromRouteQuery(query: LocationQuery = router.currentRoute.value.query): void {
            if (query.brand) this.brand = query.brand as string
            if (query.gear) this.gear = query.gear as string
            if (query.color) this.color = query.color as string
            if (query.fuel) this.fuel = query.fuel as string
            if (query.yearMin) this.yearMin = Number(query.yearMin)
            if (query.yearMax) this.yearMax = Number(query.yearMax)
            if (query.displacementMin) this.displacementMin = Number(query.displacementMin)
            if (query.displacementMax) this.displacementMax = Number(query.displacementMax)
            if (query.mileageMin) this.mileageMin = Number(query.mileageMin)
            if (query.mileageMax) this.mileageMax = Number(query.mileageMax)
            if (query.powerMin) this.powerMin = Number(query.powerMin)
            if (query.powerMax) this.powerMax = Number(query.powerMax)
            if (query.ordering) this.ordering = String(query.ordering) as CarListOrdering
            this.page = query.page ? Number(query.page) : 1
        },

        apply(): void {
            if (!this.validate()) return

            const query: Record<string, string> = {}

            for (const [key, value] of Object.entries(this.$state))
                if (value != null && value !== '')
                    query[key] = String(value)

            router.push({ name: 'car-list', query })
        },

        reset(): void {
            this.brand = null
            this.gear = null
            this.color = null
            this.fuel = null
            this.yearMin = null
            this.yearMax = null
            this.displacementMin = null
            this.displacementMax = null
            this.mileageMin = null
            this.mileageMax = null
            this.powerMin = null
            this.powerMax = null
            this.ordering = null
            this.page = 1
        }
    }
})