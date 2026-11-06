import { onMounted, onUnmounted } from 'vue'

type ShortcutHandler = (e: KeyboardEvent) => void

interface Shortcut {
  key: string
  ctrl?: boolean
  meta?: boolean
  handler: ShortcutHandler
  description: string
}

export function useKeyboardShortcuts(shortcuts: Shortcut[]) {
  function handleKeyDown(e: KeyboardEvent) {
    // Don't trigger in input/textarea
    const target = e.target as HTMLElement
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
      // Only allow Escape in inputs
      if (e.key !== 'Escape') return
    }

    for (const shortcut of shortcuts) {
      const ctrlMatch = shortcut.ctrl
        ? (e.ctrlKey || e.metaKey)
        : true
      const keyMatch = e.key.toLowerCase() === shortcut.key.toLowerCase()

      if (ctrlMatch && keyMatch) {
        if (shortcut.ctrl || shortcut.meta) {
          e.preventDefault()
        }
        shortcut.handler(e)
        return
      }
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeyDown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown)
  })
}
