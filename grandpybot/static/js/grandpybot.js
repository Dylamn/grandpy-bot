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
}

export default GrandpyBot