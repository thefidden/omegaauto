let cancelActiveScroll: (() => void) | null = null

export function smoothScrollTo(left: number, top: number): Promise<void> {
	cancelActiveScroll?.()

	const startLeft = window.scrollX
	const startTop = window.scrollY
	const distance = Math.hypot(left - startLeft, top - startTop)

	if (!distance || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
		window.scrollTo({ left, top })
		return Promise.resolve()
	}

	const duration = Math.min(700, Math.max(300, distance * .15))
	const startedAt = performance.now()

	return new Promise((resolve) => {
		let animationFrame = 0
		let finished = false

		const finish = () => {
			if (finished) return

			finished = true
			cancelAnimationFrame(animationFrame)
			cancelActiveScroll = null
			resolve()
		}

		cancelActiveScroll = finish

		const animate = (now: number) => {
			const progress = Math.min(1, (now - startedAt) / duration)
			const eased = progress < .5
				? 4 * progress ** 3
				: 1 - (-2 * progress + 2) ** 3 / 2

			window.scrollTo({
				left: startLeft + (left - startLeft) * eased,
				top: startTop + (top - startTop) * eased
			})

			if (progress === 1) {
				finish()
				return
			}

			animationFrame = requestAnimationFrame(animate)
		}

		animationFrame = requestAnimationFrame(animate)
	})
}
