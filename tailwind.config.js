module.exports = {
  purge: [
    './grandpybot/templates/**/*.html',
    './grandpybot/static/js/*.js',
  ],
  darkMode: 'class', // false, 'media' or 'class'
  theme: {
    extend: {
      keyframes: {
        dotTyping: {
          '0%': {
            boxShadow: '9984px 0 0 0 #9880ff, 9999px 0 0 0 #9880ff, 10014px 0 0 0 #9880ff;'
          },
          '16.667%': {
            boxShadow: '9984px -10px 0 0 #9880ff, 9999px 0 0 0 #9880ff, 10014px 0 0 0 #9880ff;'
          },
          '33.333%': {
            boxShadow: '9984px 0 0 0 #9880ff, 9999px 0 0 0 #9880ff, 10014px 0 0 0 #9880ff;'
          },
          '50%': {
            boxShadow: '9984px 0 0 0 #9880ff, 9999px -10px 0 0 #9880ff, 10014px 0 0 0 #9880ff;'
          },
          '66.667%': {
            boxShadow: '9984px 0 0 0 #9880ff, 9999px 0 0 0 #9880ff, 10014px 0 0 0 #9880ff;'
          },
          '83.333%': {
            boxShadow: '9984px 0 0 0 #9880ff, 9999px 0 0 0 #9880ff, 10014px -10px 0 0 #9880ff;'
          },
          '100%': {
            boxShadow: '9984px 0 0 0 #9880ff, 9999px 0 0 0 #9880ff, 10014px 0 0 0 #9880ff;'
          },
        }
      },
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
