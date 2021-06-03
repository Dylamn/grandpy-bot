class Message {
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
    this.fromSelf = sender.toLowerCase() === 'self'

    this.messagesRoot = document.getElementById('messages')

    if (! this.messagesRoot) {
      throw new DOMException('No Element with `messages` ID (#messages) found in the document.')
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

    return (messageLayout.classList.contains('justify-end') && this.fromSelf)
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
    linesLayoutDiv.classList.add('flex', 'flex-col', 'space-y-4', 'max-w-xs', 'mx-2', 'py-2')

    if (typeof textContent === 'string') {
      this.addLine(linesLayoutDiv, textContent)
    }

    // Append div together...
    layoutDiv.appendChild(linesLayoutDiv)
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

    this.messagesRoot.appendChild(this.HTMLStructure)
  }

  /**
   *
   * @param {string} textContent
   */
  update (textContent) {
    if (this.recentlyCreated) {
      return
    }

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
      styleClasses.push('bg-blue-500', 'rounded-br-none')
    } else { // Means the message(s) comes from the intercolutor.
      styleClasses.push('bg-gray-200', 'rounded-bl-none')
    }

    line.setAttribute('class', styleClasses.join(' '))

    // Create a node for the text content of the line
    const text = document.createTextNode(content)

    line.appendChild(text)

    // Append the line to the wrapper
    wrapper.appendChild(line)

    return wrapper
  }
}

export default Message