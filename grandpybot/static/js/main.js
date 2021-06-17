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
  const gbresponse = grandpy.answerQuestion(data)
  const response = await fetch('/api/questions/answer', {
    method: 'POST',
    body: data
  })

  const result = await response.json()

  displayAnswer(result, response.status)
}

function displayAnswer (json, status_code) {
  if (status_code !== 200) {
    console.error('An error occurred. Please try again later.')
    return
  }

  if (json.status !== 'ok') {
    return console.error('Not found?')
  }

  new Message(json.wiki_text, Message.senders.INTERLOCUTOR).push()
}
