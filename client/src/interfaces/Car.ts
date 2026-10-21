import type { CarImage } from "./CarImage.ts";

export interface Car {
    id: string,
    model: string,
    brand: string,
    year: number,
    mileage: number,
    power: number,
    displacement: number,
    fuel: string,
    gear: string,
    color: string,
    status: string,
    images: CarImage[],
    price_total_rub: number
}
