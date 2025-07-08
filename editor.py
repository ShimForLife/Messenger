from collections import deque

class Editor:
    def __init__(self):
        self._undo = deque()
        self._redo = deque()
    
    def write(self, message):
        self._undo.append(message) #saves the ungoing msg in undo
        self._redo.clear()
    
    def undo(self):
        if not self._undo: 
            print("You haven't written anything yet. Use: write")
            return False
        self._redo.append(self._undo.pop())
        
    
    def redo(self):
        if not self._redo:
            print("You didn't do anything after this.")
            return False
        self._undo.append(self._redo.pop())
        
    
    def get_full_message(self): #joins parts of the ungoing msg
        return " ".join(self._undo) if self._undo else ""
    
    def clear(self):
        self._undo.clear()
        self._redo.clear()
    
    def has_content(self):
        return bool(self._undo)