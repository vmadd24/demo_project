/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        bg: "#F9F6F0",
        surface: "#FFFFFF",
        primary: "#C86B3C",
        primaryHover: "#A8532A",
        ink: "#3A2E2A",
        sub: "#6B5A53",
        line: "#E8E2D9",
        sage: "#8A9A86",
      },
      fontFamily: {
        serif: ['"Playfair Display"', "serif"],
        sans: ['"Manrope"', "sans-serif"],
      },
    },
  },
  plugins: [],
};
