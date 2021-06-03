import Message from './message.js'

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

  // Insert user question
  new Message(data.get('user_input'), Message.senders.SELF).push()

  let response = await fetch('/api/ask-question', {
    method: 'POST',
    body: data
  })

  const result = await response.json()

  displayAnswer(result)
}

function displayAnswer (json) {
  const answer = json['answer']

  if (! answer) {
    console.error('An error occurred. Please try again later.')
    return
  }

  new Message(answer, Message.senders.INTERLOCUTOR).push()
}
