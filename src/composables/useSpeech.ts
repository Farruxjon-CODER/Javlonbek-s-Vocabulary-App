import { ref } from 'vue'

export function useSpeech() {
  const isSpeaking = ref(false)
  const isSupported = typeof window !== 'undefined' && 'speechSynthesis' in window

  function speak(text: string, lang = 'en-US', rate = 0.9) {
    if (!isSupported || !text) return

    try {
      window.speechSynthesis.cancel() // Stop any ongoing speech

      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = lang
      utterance.rate = rate

      // Select high quality English voice if available
      const voices = window.speechSynthesis.getVoices()
      const selectedVoice = voices.find(
        (v) => v.lang.startsWith(lang.slice(0, 2)) && (v.name.includes('Google') || v.name.includes('Natural'))
      ) || voices.find((v) => v.lang.startsWith(lang.slice(0, 2)))

      if (selectedVoice) {
        utterance.voice = selectedVoice
      }

      utterance.onstart = () => {
        isSpeaking.value = true
      }

      utterance.onend = () => {
        isSpeaking.value = false
      }

      utterance.onerror = () => {
        isSpeaking.value = false
      }

      window.speechSynthesis.speak(utterance)
    } catch (e) {
      console.warn('SpeechSynthesis error:', e)
      isSpeaking.value = false
    }
  }

  function stop() {
    if (isSupported) {
      window.speechSynthesis.cancel()
      isSpeaking.value = false
    }
  }

  return {
    speak,
    stop,
    isSpeaking,
    isSupported
  }
}

