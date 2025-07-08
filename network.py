class Network:
    def __init__(self):
        self.is_online = False
    
    def offline(self):
        self.is_online = False
        print("You're offline.")
    
    def online(self):
        self.is_online = True
        print("You're online")

    def status(self):
        return "online" if self.is_online else "offline"
    
    def online_check(self, action_name="send"): #this is used when user wants to send a msg but they're offline
        if not self.is_online:
            response = input(f"You're offline. Do you want to go online? (y/n): ")
            if response.lower() == 'y':
                self.online()
                return True
            else:
                return False
        return True