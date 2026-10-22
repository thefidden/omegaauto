import { useDark, useToggle } from "@vueuse/core"

export function useTheme() {
	const isDark = useDark({
		selector: "html",
		attribute: "class",
		valueDark: "dark",
		valueLight: "light",
		initialValue: 'light'
	})
	const toggleDark = useToggle(isDark)

	function toggleTheme() {
		const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
		const apply = () => {
			toggleDark()
		}

		if (reducedMotion || typeof document.startViewTransition !== "function") {
			const root = document.documentElement
			root.classList.add("theme-animating")
			apply()
			window.setTimeout(() => root.classList.remove("theme-animating"), 400)
			return
		}

		document.startViewTransition(apply)
	}

	return { isDark, toggleTheme }
}
