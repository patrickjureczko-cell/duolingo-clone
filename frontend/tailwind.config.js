/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  theme: {
    extend: {
      colors: {
        duo: {
          green: '#58CC02',
          'green-dark': '#46A302',
          blue: '#1CB0F6',
          red: '#FF4B4B',
          orange: '#FF9600',
          purple: '#CE82FF',
          yellow: '#FFD900',
          gray: '#AFAFAF',
          'light-gray': '#E5E5E5',
          dark: '#3C3C3C',
        },
      },
      fontFamily: {
        sans: ['Nunito', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
