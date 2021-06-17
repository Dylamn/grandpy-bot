import Message from './message.js'
import GrandpyBot from './grandpybot.js'

const form = document.getElementById('form_question')

form.onsubmit = async (ev) => {
  ev.preventDefault()

  // Get the user input
  const data = new FormData(form)

  if (! data.get('user_input')) {
    return
  }
  // Reset the user input
  form.reset()

  // Init GrandPy
  const grandpy = new GrandpyBot()

  // Insert user question
  new Message(data.get('user_input'), Message.senders.SELF).push()

  // Ask the question to GrandPy
  const response = await grandpy.answerQuestion(data)

  if (response.status !== 200) {
    return console.error('An error occurred. Please try again later.')
  }
  const result = await response.json()

  console.log('API response', response.status, result)

  displayAnswer(result)
}

function displayAnswer (json) {
  let msg_content = ''

  if (json.status !== 'ok') {
    msg_content = 'Une erreur est survenue. Veuillez réessayez plus tard.'
  } else {
    msg_content = json.message

    if (json.wiki_text) {
      msg_content += json.wiki_text
    }
  }

  const msg = new Message(msg_content, Message.senders.INTERLOCUTOR)

  if (json.location) {
    msg.embedMap(json.location)
  }

  msg.push()
}
