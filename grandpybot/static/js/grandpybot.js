import Message from './message.js'

class GrandpyBot {

  /**
   * Get a response of Grandpy Bot from a question.
   *
   * @param {any} data
   * @return {Promise<Response>}
   */
  async answerQuestion (data) {
    return await fetch('/api/questions/answer', {
      method: 'POST',
      body: data
    })
  }

  /**
   * Send a message.
   *
   * @param msg_content
   * @return {Message}
   */
  writeMessage(msg_content) {
    const msg = new Message(msg_content, Message.senders.INTERLOCUTOR)
    msg.push()

    return msg
  }
}

export default GrandpyBot