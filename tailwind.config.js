/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#620e86',
          50: '#f4e8fa',
          100: '#e5cff3',
          200: '#d0a7e9',
          300: '#b774dc',
          400: '#9b46cb',
          500: '#822bb2',
          600: '#620e86', // Asosiy rang
          700: '#53106e',
          800: '#461159',
          900: '#391246',
        },
        brand: {
          DEFAULT: '#620e86',
          light: '#a855f7',
        }
      }
    },
  },
  plugins: [],
}
