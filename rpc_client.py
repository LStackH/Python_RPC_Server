import xmlrpc.client
from datetime import datetime

port = 8000

def main():
    # Connection to the server
    proxy = xmlrpc.client.ServerProxy(f"http://localhost:{port}/")
    print(f"Connection to http://localhost:{port}\n")

    while True:
        print("Notebook - What would you like to do?")
        print("1) Add a note to a topic")
        print("2) View notes by a topic")
        print("3) Search Wikipedia and append result")
        print("4) Exit")
        
        choice = input("Enter your choice: ").strip()
        
        match choice:

            # Add notes by topic
            case "1":
                topic = input("Topic name: ").strip()
                if not topic:
                    print("Topic name cannot be empty.\n")
                    continue

                text = input("Note text: ").strip()
                if not text:
                    print("Note text cannot be empty.\n")
                    continue

                # Generate timestamp automatically
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Try to pass the information to the server
                try:
                    result = proxy.add_note_to_topic(topic, text, timestamp)
                    print("[Server Response]:", result)
                except Exception as e:
                    print("Error calling add_note_to_topic:", e)

            # View notes by topic
            case "2":
                topic = input("Topic name: ").strip()
                if not topic:
                    print("Topic name cannot be empty.\n")
                    continue
                
                # Try to pass the information to the server
                try:
                    notes = proxy.get_notes_by_topic(topic)
                    if notes:
                        print(f"\nNotes for topic '{topic}':")
                        for i, note in enumerate(notes, start=1):
                            print(f"{i}. {note['text']} (timestamp: {note['timestamp']})")
                    else:
                        print(f"No notes found for topic '{topic}'.")
                except Exception as e:
                    print("Error calling get_notes_by_topic:", e)
            
            # Sarch wikipedia for link
            case "3": 
                topic = input("Topic name: ").strip()
                if not topic:
                    print("Topic name cannot be empty.\n")
                    continue
                search_term = input("Wikipedia search term: ").strip()
                if not search_term:
                    print("Search term cannot be empty.\n")
                    continue
                
                # Generate timestamp automatically
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Try to pass the information to the server
                try:
                    result = proxy.search_wikipedia(topic, search_term, timestamp)
                    print("[Server Response]:", result)
                except Exception as e:
                    print("Error:", e)
                    
            case "4":
                print("Exiting client.")
                break

            case _:
                print("Invalid choice. Please try again.")
        
        print("\n")

if __name__ == "__main__":
    main()