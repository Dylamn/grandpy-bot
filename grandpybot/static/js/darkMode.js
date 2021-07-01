const toggle = document.getElementById('toggle-dark-mode')
const moon = document.getElementById('moon-dark-mode'),
  sun = document.getElementById('sun-dark-mode')

if (localStorage.theme === 'dark') {
  toggleButtons()
}

toggle.addEventListener('click', () => {
  const darkMode = document.documentElement.classList.toggle('dark')
  toggleButtons()

  if (darkMode) {
    localStorage.theme = 'dark'
  } else {
    localStorage.theme = 'light'
  }
})

/**
 * Switch the visibility of the dark mode icons.
 *
 * @return void
 */
function toggleButtons () {
  moon.classList.toggle('hidden')
  sun.classList.toggle('hidden')
}