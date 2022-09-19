/* Contains the list of chat sessions and the 'Everyone' chat session.
 * Represent the chat sessions as: 
 * 'Everyone' is always at the top
 * Students are displayed in a queue which is updated based on students
 *      entering the chat session and new messages.
 *      Each student that is popped from the queue is re-pushed immediately.
 */ 