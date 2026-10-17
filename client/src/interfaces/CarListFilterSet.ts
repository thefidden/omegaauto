import type { CarListOrdering } from "../stores/CarListFiltersStore.ts";

export interface CarListFilterSet {
    brand?: string | null
    gear?: string | null
    color?: string | null
    fuel?: string | null
    yearMin?: number | null
    yearMax?: number | null
    displacementMin?: number | null
    displacementMax?: number | null
    mileageMin?: number | null
    mileageMax?: number | null
    powerMin?: number | null
    powerMax?: number | null,
    ordering?: CarListOrdering | null,
    page: number
}
