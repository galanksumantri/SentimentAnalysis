/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: [
    "./templates/*.{html,js}"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#43302b',
        secondary: '#846358',
        tertiary: '#977669'
      }
    },
  },
  plugins: [],
}
