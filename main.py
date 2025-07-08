from editor import Editor
from queue_manager import Queue_manager
from network import Network

class My_messenger: #this class refers to essential functions and variables in each module
    def __init__(self):
        self.editor = Editor()
        self.queue_manager = Queue_manager()
        self.network = Network()
    
    def write(self, msg):
        self.editor.write(msg)
    
    def undo(self):
        self.editor.undo()
    
    def redo(self):
        self.editor.redo()
    
    def save(self, command):
        if not self.editor.has_content(): #for when the undo queue is empty 
            print("You haven't written anything yet. Use: write")
            return
        
        full_msg = self.editor.get_full_message()
        if self.queue_manager.save(command, full_msg): #it gets "command" because it shows whether the message is urgent or not
            self.editor.clear()
    
    def send(self):
        if not self.network.online_check():
            return
        
        self.queue_manager.send()
    
    def send_all(self):
        if not self.network.online_check():
            return
    
        self.queue_manager.send_all()
    
    def go_offline(self):
        self.network.offline()
    
    def go_online(self):
        self.network.online()
    
    def delete(self, index):
        self.queue_manager.delete(index)
    
    def show_last_5(self):
        self.queue_manager.show_last_5()
    
    def on_or_off(self):
        status = self.network.status()
        return f"_{status}_: "


def main():
    messenger = My_messenger()
    
    print("WELCOME TO YOUR MESSENGER")
    print("you can use the following commands:")
    print("write: to start a new message or continue with a message you haven't saved.")
    print("undo: to undo changes to a message you haven't saved.")
    print("redo: to redo changes to a message you haven't saved.")
    print("save-receiverID or save-u-receiverID: to save a message.")
    print("send: to send a message.")
    print("send all: to send all messages.")
    print("offline: to go offline.")
    print("online: to go online.")
    print("delete index: have this index deleted from history.")
    print("show last 5: show last 5 messages")

    
    while True:
        command = input(messenger.on_or_off()).strip() #to the online or offline status in prompt 
        
        if command == "undo":
            messenger.undo()
        elif command == "redo":
            messenger.redo()
        elif command == "send":
            messenger.send()
        elif command == "send all":
            messenger.send_all()
        elif command == "go_offline":
            messenger.go_offline()
        elif command == "go_online":
            messenger.go_online()
        elif command == "show last 5":
            messenger.show_last_5()
        elif command == "write": 
            message = input("Enter your message: ")
            messenger.write(message)
        elif command.startswith("save-"):
            messenger.save(command)
        elif command.startswith("delete "):
            index = command[7:] #"delete " has 7 characters so index must be after 
            messenger.delete(index) 
        else:
            print("invalid command.")

if __name__ == "__main__":
    main()