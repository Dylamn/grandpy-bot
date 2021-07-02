module.exports = {
  purge: [
    './grandpybot/templates/**/*.html',
    './grandpybot/static/js/message.js',
  ],
  darkMode: 'class', // false, 'media' or 'class'
  theme: {
    extend: {
      height: theme => ({
        'screen-3/4': '75vh',
        'screen/2': '50vh',
        'screen/3': 'calc(100vh / 3)',
        'screen/4': 'calc(100vh / 4)',
        'screen/5': 'calc(100vh / 5)',
      }),
    },
  },
  variants: {
    extend: {
      textColor: ['visited'],
    },
  },
  plugins: [],
}
