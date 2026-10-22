import type { RouteLocationRaw, Router } from "vue-router"
import { smoothScrollTo } from "./smoothScroll.ts"

/** Scroll to hash even when the route is already on that hash (router.push is a no-op then). */
export async function navigateToHash(
	router: Router,
	hash: string,
	location: RouteLocationRaw = { name: "main" },
) {
	const normalized = hash.startsWith("#") ? hash : `#${hash}`
	const current = router.currentRoute.value
	const targetLocation = typeof location === "string"
		? location
		: { ...location, hash: normalized }

	const samePath = typeof location === "string"
		? current.fullPath.split("#")[0] === location.split("#")[0]
		: (location.name == null || current.name === location.name)
			&& (location.path == null || current.path === location.path)

	if (samePath && current.hash === normalized) {
		const id = decodeURIComponent(normalized.slice(1))
		const target = document.getElementById(id)
		if (!target) return
		await smoothScrollTo(window.scrollX, window.scrollY + target.getBoundingClientRect().top)
		return
	}

	await router.push(targetLocation)
}
