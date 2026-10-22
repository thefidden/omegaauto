import type { RouteRecordName, Router } from "vue-router"
import { smoothScrollTo } from "./smoothScroll.ts"

/** Scroll to hash even when the route is already on that hash (router.push is a no-op then). */
export async function navigateToHash(
	router: Router,
	hash: string,
	name: RouteRecordName = "main",
) {
	const normalized = hash.startsWith("#") ? hash : `#${hash}`
	const current = router.currentRoute.value

	if (current.name === name && current.hash === normalized) {
		const id = decodeURIComponent(normalized.slice(1))
		const target = document.getElementById(id)
		if (!target) return
		await smoothScrollTo(window.scrollX, window.scrollY + target.getBoundingClientRect().top)
		return
	}

	await router.push({ name, hash: normalized })
}
