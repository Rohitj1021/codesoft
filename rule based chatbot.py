def simple_chatbot():
    print("ChatBot: Hi! I'm a rule-based chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ").strip().lower()
        
        if not user_input:
            print("ChatBot: Say something!")
            continue
            
        # Exit condition
        if any(word in user_input for word in ["bye", "goodbye", "exit", "quit"]):
            print("ChatBot: Goodbye! Have a great day.")
            break
            
        # Greeting patterns
        elif any(word in user_input for word in ["hi", "hello", "hey", "hola"]):
            print("ChatBot: Hello there!")
            
        # How are you patterns
        elif "how are you" in user_input:
            print("ChatBot: I'm a bot, so I'm always operational! How about you?")
            
        # Name patterns
        elif any(word in user_input for word in ["your name", "who are you"]):
            print("ChatBot: I'm a simple rule-based chatbot. You can call me RB-Chat!")
            
        # Time/Date patterns
        elif any(word in user_input for word in ["time", "date", "day", "today"]):
            print("ChatBot: I don't have real-time access, but I can respond to rules!")
            
        # Help patterns
        elif "help" in user_input:
            print("ChatBot: I can respond to greetings, name questions, 'how are you', and exit commands.")
            
        # Thank you patterns
        elif any(word in user_input for word in ["thank", "appreciate", "grateful"]):
            print("ChatBot: You're welcome!")
            
        # Default response for unrecognized input
        else:
            print("ChatBot: I'm still learning! Try asking about my name or saying hello.")

# Start the chatbot
if __name__ == "__main__":
    simple_chatbot()