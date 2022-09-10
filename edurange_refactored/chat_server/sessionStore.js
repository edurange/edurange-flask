/* abstract */ class SessionStore {
  findSession(id) {}
  saveSession(id, session) {}
  findAllSessions() {}
}

class InMemorySessionStore extends SessionStore {
  constructor() {
    super();
    this.sessions = new Map();
  }

  findSession(id) {
    return this.sessions.get(id);
  }

  saveSession(id, session) {
    this.sessions.set(id, session);
  }

  findAllSessions() {
    return [...this.sessions.values()];
  }
}

module.exports = {
  InMemorySessionStore
};
/* abstract */ class MessageStore {
    saveMessage(message) {}
    findMessagesForUser(userID) {}
  }
  
  class InMemoryMessageStore extends MessageStore {
    constructor() {
      super();
      this.messages = [];
    }
  
    saveMessage(message) {
      this.messages.push(message);
    }
  
    findMessagesForUser(userID) {
      return this.messages.filter(
        ({ from, to }) => from === userID || to === userID
      );
    }
  }
  
  module.exports = {
    InMemoryMessageStore,
  };
  