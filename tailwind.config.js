/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./boilerplate/**/*.html",
    "./boilerplate/**/*.py",  // For dynamic class generation in Python
    // Add any other templates or JS files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
} 