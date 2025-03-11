from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
import os
import requests

port = 8000
NOTES_FILE = "notes.xml"

# Pythons ThreadingMixIn should let our server handle each client request in its own thread
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def add_note_to_topic(topic_name, note_text, timestamp):
    tree = load_notesData()
    root = tree.getroot()

    # Try to find if the <topic> already exists
    topic_elem = None
    for t in root.findall("topic"):
        if t.get("name") == topic_name:
            topic_elem = t
            break

    # If not found, create a new one
    if topic_elem is None:
        topic_elem = ET.SubElement(root, "topic", {"name": topic_name})

    # Create a new <note> element
    note_elem = ET.SubElement(topic_elem, "note", {"name": note_text[:20]})
    
    # Create <text> and <timestamp> child elements
    text_elem = ET.SubElement(note_elem, "text")
    text_elem.text = note_text

    ts_elem = ET.SubElement(note_elem, "timestamp")
    ts_elem.text = timestamp

    # Save changes
    save_notesData(tree)
    return (f"Note added to topic '{topic_name}'.")

def get_notes_by_topic(topic_name):
    tree = load_notesData()
    root = tree.getroot()

    # Go through every <topic> element
    for t in root.findall("topic"):
        if t.get("name") == topic_name:
            # Topic matches, create list to hold notes
            notes_data = []
            for note in t.findall("note"):
                text_elem = note.find("text")
                ts_elem = note.find("timestamp")

                # Check that the elements exits and have text, add them to the list
                note_text = text_elem.text if (text_elem is not None and text_elem.text is not None) else ""
                note_ts = ts_elem.text if (ts_elem is not None and ts_elem.text is not None) else ""
                notes_data.append({"text": note_text, "timestamp": note_ts})
            return notes_data
    # If topic not found, return an empty list
    return []

def search_wikipedia(topic_name, search_term, timestamp):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": search_term,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    # 4th element in data is thelist of url's, pick the first one if available
    wiki_link = data[3][0] if data and len(data) >= 4 and data[3] else "No article found."
    
    # Create a note text that includes the wikipedia link
    note_text = f"Wikipedia result for '{search_term}': {wiki_link}"
    # append this note
    result = add_note_to_topic(topic_name, note_text, timestamp)
    return result
    #print(data)

def load_notesData():
    if not os.path.exists(NOTES_FILE):
        # If file does not exist, create a root <data> element
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(NOTES_FILE)
    # Parse the file
    return ET.parse(NOTES_FILE)

def save_notesData(tree):
    tree.write(NOTES_FILE)

def main():
    # Create the threaded server, to port
    server = ThreadedXMLRPCServer(("localhost", port))
    print(f"Server listening on http://localhost:{port}")

    # Function register for client
    server.register_function(add_note_to_topic, "add_note_to_topic")
    server.register_function(get_notes_by_topic, "get_notes_by_topic")
    server.register_function(search_wikipedia, "search_wikipedia")
    # Run the server's main loop
    server.serve_forever()

if __name__ == "__main__":
    main()