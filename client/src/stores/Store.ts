import { defineStore } from "pinia";
import type { Car } from "../interfaces/Car.ts";
import { type CarListOrdering, useCarListFilters } from "./CarListFiltersStore.ts";

export const useStore = defineStore('store', {
    state: () => ({
        brands: [] as string[],
        gears: [] as string[],
        colors: [] as string[],
        fuels: [] as string[],
        cars: [] as Car[],
        carsCount: 0,
        orderings: [
            'brand', '-brand',
            'year', '-year',
            'displacement', '-displacement',
            'mileage', '-mileage',
            'power', '-power',
            'price_total_rub', '-price_total_rub'
        ] as CarListOrdering[],
        car: null as Car | null,
        carID: '',

        loading: false,
        brandsLoading: false,
        gearsLoading: false,
        colorsLoading: false,
        fuelsLoading: false,
        carsLoading: false,
        carLoading: false
    }),

    actions: {
        async fetchCar(id: string) {
            this.car = null
            this.carLoading = true

            try {
                const response = await fetch(`/api/client/cars/${ id }`)
                if (!response.ok) throw new Error(`car request failed: ${ response.status }`)
                const data = await response.json() as Car
                if (!Array.isArray(data.images)) throw new Error('car response has no images')
                this.car = data
            }
            catch (e) {
                console.log('fetch car error', e)
                this.car = null
            }
            finally {
                this.carLoading = false
            }
        },

        async fetchCars() {
            this.cars = []
            this.carsLoading = true

            const filters = useCarListFilters()
            const url = new URL('/api/client/cars/', window.location.origin)

            const params: Record<string, string | number | null | undefined> = {
                brand: filters.brand,
                gear: filters.gear,
                color: filters.color,
                fuel: filters.fuel,

                year_min: filters.yearMin,
                year_max: filters.yearMax,

                displacement_min: filters.displacementMin,
                displacement_max: filters.displacementMax,

                mileage_min: filters.mileageMin,
                mileage_max: filters.mileageMax,

                power_min: filters.powerMin,
                power_max: filters.powerMax,

                ordering: filters.ordering,
                page: filters.page
            }

            for (const [key, value] of Object.entries(params))
                if (value !== null && value !== undefined && value !== '')
                    url.searchParams.append(key, String(value))

            try {
                const response = await fetch(url)
                if (!response.ok) throw new Error(`cars request failed: ${ response.status }`)
                const data = await response.json() as { count: number, results: Car[] }
                this.carsCount = data.count
                this.cars = data.results
            }
            catch (e) {
                console.log('fetch cars error', e)
                this.cars = []
                this.carsCount = 0
            }
            finally {
                this.carsLoading = false
            }
        },

        async fetchAvailableBrands() {
            this.brands = []
            this.brandsLoading = true

            try {
                const response = await fetch('/api/brands/?only_available=true')
                if (!response.ok) throw new Error(`brands request failed: ${ response.status }`)
                const data: { name: string }[] = await response.json()
                this.brands = data.map(brand => brand.name)
            }
            catch (e) {
                console.log('fetch brands error', e)
                this.brands = []
            }
            finally {
                this.brandsLoading = false
            }
        },

        async fetchGears() {
            this.gears = []
            this.gearsLoading = true

            try {
                const response = await fetch('/api/gears/')
                if (!response.ok) throw new Error(`gears request failed: ${ response.status }`)
                const data: { name: string }[] = await response.json()
                this.gears = data.map(gear => gear.name)
            }
            catch (e) {
                console.log('fetch gears error', e)
                this.gears = []
            }
            finally {
                this.gearsLoading = false
            }
        },

        async fetchColors() {
            this.colors = []
            this.colorsLoading = true

            try {
                const response = await fetch('/api/colors/')
                if (!response.ok) throw new Error(`colors request failed: ${ response.status }`)
                const data: { name: string }[] = await response.json()
                this.colors = data.map(color => color.name)
            }
            catch (e) {
                console.log('fetch colors error', e)
                this.colors = []
            }
            finally {
                this.colorsLoading = false
            }
        },

        async fetchFuels() {
            this.fuels = []
            this.fuelsLoading = true

            try {
                const response = await fetch('/api/fuels/')
                if (!response.ok) throw new Error(`fuels request failed: ${ response.status }`)
                const data: { name: string }[] = await response.json()
                this.fuels = data.map(fuel => fuel.name)
            }
            catch (e) {
                console.log('fetch fuels error', e)
                this.fuels = []
            }
            finally {
                this.fuelsLoading = false
            }
        }
    }
})
