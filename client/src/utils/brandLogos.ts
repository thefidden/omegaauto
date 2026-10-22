const logosLight = import.meta.glob("../assets/car-logos-light/*", {
	eager: true,
	import: "default",
}) as Record<string, string>

const logosDark = import.meta.glob("../assets/car-logos-dark/*", {
	eager: true,
	import: "default",
}) as Record<string, string>

function logoKey(folder: "car-logos-light" | "car-logos-dark", brand: string) {
	const name = brand.toLowerCase()
	const extension = name === "great wall" ? "png" : "svg"
	return `../assets/${folder}/${name}.${extension}`
}

export function getBrandLogoHref(brand: string, darkTheme: boolean): string {
	const map = darkTheme ? logosLight : logosDark
	const folder = darkTheme ? "car-logos-light" : "car-logos-dark"
	return map[logoKey(folder, brand)] ?? ""
}
