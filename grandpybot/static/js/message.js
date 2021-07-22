import { senders } from './enums.js'

class Message {

  /**
   * Enum of the differents types of actors in a chat.
   *
   * @type {{INTERLOCUTOR: string, SELF: string}}
   */
  static senders = senders

  /**
   * Create a typing loader.
   *
   * @return {HTMLDivElement}
   */
  static typing () {
    const loader = document.createElement('div')
    loader.className = 'dot-typing m-2'

    return loader
  }

  /**
   * Message constructor.
   *
   * @param {string|HTMLElement|null} textContent
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
    this.clear = this.clear.bind(this)
    this.create = this.create.bind(this)
    this.createLine = this.createLine.bind(this)
    this.update = this.update.bind(this)
    this.addLine = this.addLine.bind(this)
    this.addImage = this.addImage.bind(this)
    this.getLayout = this.getLayout.bind(this)
    this.getLinesLayout = this.getLinesLayout.bind(this)
    this.embedMap = this.embedMap.bind(this)
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
  }

  /**
   * Append a line to the end of the message.
   *
   * @param {any} content
   */
  update (content) {
    const lastLine = this.getLinesLayout().lastElementChild

    if (lastLine) {
      lastLine.lastElementChild.classList.remove(this.fromSelf ? 'rounded-br-none' : 'rounded-bl-none')
    }

    this.addLine(this.getLinesLayout(), content)
  }

  /**
   * Create and append a new line to the given container.
   *
   * @param {HTMLDivElement} container
   * @param {any} content
   */
  addLine (container, content) {
    container.appendChild(this.createLine(content))
  }

  /**
   * Create a new message line.
   *
   * @param {any} content
   * @return {HTMLDivElement}
   */
  createLine (content) {
    // Create a div which will wrap the span otherwise the span will shrink as much as it can
    const wrapper = document.createElement('div')
    let line, lineContent = content

    if (content instanceof HTMLElement) {
      line = document.createElement('div')
    } else {
      line = document.createElement('span')
      // A regexp which check if an URL is present in the string.
      const hasUrl = content.match(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*)/)

      if (hasUrl) { // An url has been found by the regexp.
        line.insertAdjacentText('afterbegin', content.replace(hasUrl[0], ""))
        lineContent = this.wrapUrl(content, hasUrl[0])
      } else {
        lineContent = document.createTextNode(content)
      }
    }

    // CSS classes which will be applied on the line(s).
    const styleClasses = ['inline-block', 'px-4', 'py-2', 'rounded-lg', 'whitespace-pre-wrap', 'break-words']

    if (this.fromSelf) { // Means the message(s) comes from the user.
      styleClasses.push('bg-blue-500', 'dark:bg-blue-600', 'text-white', 'rounded-br-none')
    } else { // Means the message(s) comes from the intercolutor.
      styleClasses.push('bg-gray-200', 'dark:bg-gray-700', 'dark:text-white', 'rounded-bl-none')
    }

    line.setAttribute('class', styleClasses.join(' '))
    line.appendChild(lineContent)

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

  embedMap (location, address) {
    const coordinates = [location.lat, location.lng]
    const map_wrap = document.createElement('div')

    map_wrap.id = `msg-${Date.now().toString()}`
    map_wrap.classList.add('flex-grow', 'sm:h-48', 'sm:w-64', 'h-32', 'w-48')
    // Append the map wrapper to the DOM before the instanciation of Leaflet.
    // If the HTML Element given to Leaflet is not present in the DOM,
    // it will raise an exception.
    this.update(map_wrap)

    // Create the Leaflet map
    const map = L.map(map_wrap.id, {
      zoomControl: false
    }).setView(coordinates, 13)

    // Add the marker to the founded place.
    const marker = L.marker(coordinates).addTo(map)
    if (address) {
      marker.bindPopup(address).openPopup()
    }

    // Used google as the tile provider.
    L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
      zoomControl: false,
      zoom: 13,
      subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
    }).addTo(map)
  }

  /**
   * Clear all message lines.
   *
   * @return {Message}
   */
  clear () {
    const lines = this.getLinesLayout()

    while (lines.lastElementChild) {
      lines.removeChild(lines.lastElementChild)
    }

    return this
  }

  /**
   *
   * @param content
   * @param url
   * @return {HTMLAnchorElement}
   */
  wrapUrl (content, url) {
    const link = document.createElement('a')
    link.classList.add('text-blue-600', 'hover:underline')
    link.href = url
    link.innerText = url

    return link
  }
}

export default Message