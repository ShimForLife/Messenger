import json
import os

class Queue_manager:
    def __init__(self):
        #keeps track of all messages
        self.history = []
        self.urgent = []
        self.default = []
        
        #figures out where to save the messages file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.h_json = os.path.join(script_dir, "messages.json")
        self.load_history()
    
    def load_history(self):
        #loads old messages if the file exists
        if os.path.exists(self.h_json):
            with open(self.h_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    self.history.append({
                        'message': item['message'],
                        'receiver': item['receiver']
                    })
            print(f"History loaded from: {self.h_json}")
    
    def save_history(self):
        #saves all messages to the JSON file
        history_data = []
        for i, item in enumerate(self.history):
            history_data.append({
                'index': i,
                'message': item['message'],
                'receiver': item['receiver']
            })
            
        with open(self.h_json, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        print(f"History saved to: {self.h_json}")
    
    def save(self, command, full_msg):
        #parses the command to see if it's urgent and who it's for
        if command.startswith("save-u-"):
            is_urgent = True
            receiver = command[7:]  #gets the name after "save-u-"
        elif command.startswith("save-"):
            is_urgent = False
            receiver = command[5:]  #gets the name after "save-"

        msg_data = {
            'message': full_msg,
            'receiver': receiver
        }
        
        #puts it in the right queue
        if is_urgent:
            self.urgent.append(msg_data)
        else:
            self.default.append(msg_data)
        
        print(f"You saved one message: {msg_data['message']}")
        return True
    
    def send(self): #sends one message - urgent ones go first
        if self.urgent:
            msg_data = self.urgent.pop(0)
            self.history.append(msg_data)
            self.save_history()
            print(f"You sent an urgent message to: {msg_data['receiver']}: {msg_data['message']}")
            return True
        elif self.default:
            msg_data = self.default.pop(0)
            self.history.append(msg_data)
            self.save_history()
            print(f"You sent a message to: {msg_data['receiver']}: {msg_data['message']}")
            return True
        else:
            print("You haven't saved a message yet. Use: save")
            return False
    
    def send_all(self):
        #sends everything - urgent first, then regular ones
        has_messages = self.urgent or self.default
    
        if not has_messages:
            print("Nothing to send.")
            return
    
        #empties the urgent queue first
        while self.urgent:
            msg_data = self.urgent.pop(0)
            self.history.append(msg_data)
    
        #then empties the default queue
        while self.default:
            msg_data = self.default.pop(0)
            self.history.append(msg_data)
    
        self.save_history()
        print("Sent all.")

    def delete(self, index): #deletes a message from history by its number
        index = int(index)
        if 0 <= index < len(self.history):
            deleted_msg = self.history.pop(index) 
            print(f"Message deleted: {deleted_msg['message']}")
            self.save_history()
            return True
        else:
            print("Invalid index!")
            return False
    
    def show_last_5(self): #shows the last 5 messages with their index numbers
        if not self.history:
            print("Empty history!")
            return

        for i, msg_data in enumerate(self.history[-5:]): #calculate the real index in the full list
            actual_index = len(self.history) - len(self.history[-5:]) + i
            print(f"[{actual_index}]: to {msg_data['receiver']}: {msg_data['message']}")
    
    def has_messages(self): #checks if there's anything waiting to be sent
        return bool(self.urgent or self.default)