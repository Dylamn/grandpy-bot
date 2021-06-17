class GrandpyBot {
  async answerQuestion (data) {
    const response = await fetch('/api/questions/answer', {
      method: 'POST',
      body: data
    })
  }
}

export default GrandpyBot