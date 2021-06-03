import { senders } from './enums.js'

class Message {

  /**
   * Enum of the differents types of actors in a chat.
   *
   * @type {{INTERLOCUTOR: string, SELF: string}}
   */
  static senders = senders

  /**
   * Message constructor.
   *
   * @param {string|null} textContent
   * @param {string} sender
   * @return void
   */
  constructor (textContent = null, sender) {
    // Determines if the message already exists within the DOM.
    this.recentlyCreated = false

    // Determines if the message is sent by this client or from the interlocutor.
    this.fromSelf = sender.toLowerCase() === Message.senders.SELF

    this.messagesRoot = document.getElementById('messages')

    if (! this.messagesRoot) {
      throw new DOMException('No Element with ID `messages` (#messages) found in the document.')
    }

    const lastMessage = this.messagesRoot.lastElementChild

    if (this.sameSender(lastMessage)) { // Append a line to the existing message.
      this.HTMLStructure = this.messagesRoot.lastElementChild
      this.update(textContent)
    } else { // Create a new message
      this.HTMLStructure = this.create(textContent)
      this.recentlyCreated = true
    }

    this.push = this.push.bind(this)
    this.create = this.create.bind(this)
    this.createLine = this.createLine.bind(this)
    this.update = this.update.bind(this)
    this.addLine = this.addLine.bind(this)
    this.addImage = this.addImage.bind(this)
    this.getLayout = this.getLayout.bind(this)
    this.getLinesLayout = this.getLinesLayout.bind(this)
  }

  /**
   * Get the layout Element.
   *
   * @return {HTMLDivElement}
   */
  getLayout () {
    return this.HTMLStructure.firstElementChild
  }

  /**
   * Get the lines layout Element.
   *
   * @return {HTMLDivElement}
   */
  getLinesLayout () {
    return this.getLayout().firstElementChild
  }

  /**
   * Determines if the last messages if from the same sender of the current message.
   *
   * @param chatMessage
   * @return {boolean}
   */
  sameSender (chatMessage) {
    if (! chatMessage) {
      return false
    }

    const messageLayout = chatMessage.firstElementChild
    const justifyEnd = messageLayout.classList.contains('justify-end')

    return justifyEnd && this.fromSelf || (! justifyEnd && ! this.fromSelf)
  }

  /**
   * Create a message.
   *
   * @param {string|null} textContent
   * @return {HTMLDivElement}
   */
  create (textContent = null) {
    // Create the div which will wrap all the message structure
    const chatMessageDiv = document.createElement('div')
    chatMessageDiv.setAttribute('class', 'chat-message')

    // Defines the layout of a message. More specifically,
    // if the message is on the left or right (depending which issued the message).
    const layoutDiv = document.createElement('div')
    layoutDiv.classList.add('flex', 'items-end', this.fromSelf ? 'justify-end' : 'justify-start')

    // This div defines the layout of message lines.
    const linesLayoutDiv = document.createElement('div')
    linesLayoutDiv.classList.add(
      'flex', 'flex-col', 'space-y-4', 'max-w-xs', 'mx-2', 'py-2', this.fromSelf ? 'order-1' : 'order-2'
    )

    if (textContent !== null) {
      this.addLine(linesLayoutDiv, textContent)
    }

    // Append div together...
    layoutDiv.appendChild(linesLayoutDiv)
    layoutDiv.appendChild(this.addImage())

    chatMessageDiv.appendChild(layoutDiv)

    return chatMessageDiv
  }

  /**
   * Push the message to the DOM.
   *
   * @return void
   */
  push () {
    if (! this.recentlyCreated) {
      return
    }

    // Mount the Element in the DOM
    this.messagesRoot.appendChild(this.HTMLStructure)
    // Scroll down to the last message
    this.messagesRoot.scrollTop = this.messagesRoot.scrollHeight
  }

  /**
   *
   * @param {string} textContent
   */
  update (textContent) {
    if (this.recentlyCreated) {
      return
    }

    const lastLine = this.getLinesLayout().lastElementChild // lastLine is a HTML
    lastLine.lastElementChild.classList.remove(this.fromSelf ? 'rounded-br-none' : 'rounded-bl-none')

    this.addLine(this.getLinesLayout(), textContent)
  }

  /**
   * Create and append a new line to the given container.
   *
   * @param {HTMLDivElement} container
   * @param {string} text
   */
  addLine (container, text) {
    container.appendChild(this.createLine(text))
  }

  /**
   * Create a new message line.
   *
   * @param {string} content
   * @return {HTMLDivElement}
   */
  createLine (content) {
    // Create a div which will wrap the span otherwise the span will shrink as much as it can
    const wrapper = document.createElement('div')
    const line = document.createElement('span')

    // CSS classes which will be applied on the line(s).
    const styleClasses = ['inline-block', 'px-4', 'py-2', 'rounded-lg']

    if (this.fromSelf) { // Means the message(s) comes from the user.
      styleClasses.push('bg-blue-500', 'dark:bg-blue-600', 'text-white', 'rounded-br-none')
    } else { // Means the message(s) comes from the intercolutor.
      styleClasses.push('bg-gray-200', 'dark:bg-gray-300', 'dark', 'rounded-bl-none')
    }

    line.setAttribute('class', styleClasses.join(' '))

    // Create a node for the text content of the line
    const text = document.createTextNode(content)

    line.appendChild(text)

    // Append the line to the wrapper
    wrapper.appendChild(line)

    return wrapper
  }

  addImage () {
    const imgPath = this.fromSelf
      ? '/static/images/me.png'
      : '/static/images/robot.png'

    const img = document.createElement('img')

    img.src = imgPath
    img.alt = 'profile image'
    img.classList.add('w-8', 'h-8', 'rounded-full', 'order-1')

    return img
  }
}

export default Message