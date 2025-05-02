module.exports = {
  content: [
    './templates/**/*.html', // Include your templates
    './static/js/**/*.js', // Include your JavaScript files if necessary
  ],
  theme: {
    extend: {
      colors: {
        'custom-purple': '#9B7ED4', // Adding custom color in the Tailwind config
      },
    },
  },
  plugins: [
    require('@tailwindcss/postcss'),
    require('postcss-simple-vars'),
    require('postcss-nested'),
  ],
}
