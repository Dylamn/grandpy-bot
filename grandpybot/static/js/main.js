import Message from './message.js'
import GrandpyBot from './grandpybot.js'

const form = document.getElementById('form_question')
// Init GrandPy
const grandpy = new GrandpyBot()

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

  // Start a loader for waiting the bot response.
  const bot_msg_loader = new Message(Message.typing(), Message.senders.INTERLOCUTOR)
  bot_msg_loader.push()
  // Ask the question to GrandPy
  const response = await grandpy.answerQuestion(data)

  if (response.status !== 200) {
    console.error('An error occurred. Please try again later.')
  }
  const result = await response.json()

  console.log('API response', response.status, result)

  displayAnswer(result, bot_msg_loader)
}

function displayAnswer (json, bot_msg) {
  let error_msg = null

  if (json.error) {
    error_msg = json.error.message
  } else if (json.status !== 'ok') {
    error_msg = 'Une erreur est survenue. Veuillez réessayez plus tard.'
  }

  // Clear the typing loader...
  // bot_msg.clear()

  if (error_msg) { // An error occurred.
    return bot_msg.update(error_msg)
  }

  // Write grandpy messages...
  // bot_msg.update(json.address)
  bot_msg.embedMap(json.location, json.address)
  grandpy.writeMessage(json.message)
  grandpy.writeMessage(json.wiki_text)
}

/**
 * Messages observer.
 * Scroll to the bottom of the messages frame at each messages.
 *
 * @type {MutationObserver}
 */
const messagesObserver = new MutationObserver(function (mutations) {
  const messagesRoot = mutations[0].target
  // Scroll down to the last message
  console.log(messagesRoot)
  messagesRoot.scrollTop = messagesRoot.scrollHeight
})

messagesObserver.observe(document.getElementById('messages'), {
  childList: true
})