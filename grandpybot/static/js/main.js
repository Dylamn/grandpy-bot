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

  // Launch a loader to wait for the bot to respond.
  const bot_msg_loader = new Message(Message.typing(), Message.senders.INTERLOCUTOR)
  bot_msg_loader.push()
  // Ask the question to GrandPy
  const response = await grandpy.answerQuestion(data)

  if (response.status >= 500) {
    return bot_msg_loader.clear()
      .update('Une erreur est survenue. Veuillez réessayez plus tard.')
  }
  const result = await response.json()

  displayAnswer(result, bot_msg_loader)
}

function displayVerboseError (msg, json) {
  const error = json.error

  // Display the error message
  msg.update(error.message)

  if (error.status === 'wiki_not_found') { // We have atleast the location
    msg.update(`Voici l'adresse :\n${json.address}`)
    msg.embedMap(json.location, json.address)
  }
}

function displayAnswer (json, bot_msg) {
  // Clear the typing loader...
  bot_msg.clear()

  if (json.error) { // An error occurred.
    return displayVerboseError(bot_msg, json)
  }

  // Write grandpy messages...
  bot_msg.update(`Voici l'adresse mon poussin :\n${json.address}`)
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