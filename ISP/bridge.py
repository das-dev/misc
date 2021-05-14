class Timer: 
    def register(self, timeout, client):
        client.lock()

    
class TimerClient:
    def timeout(self):
        raise NotImplementedError


class TimerAdapter(TimerClient):
    def __init__(self, door):
        self.door = door
    
    def timeout(self):
        Timer().register(5, self.door)

    
class Door:
    STATE_LOCKED = 1
    STATE_UNLOCKED = 0
  
    def __init__(self):
        self._state = self.STATE_LOCKED

    def lock(self):
        self._state = self.STATE_LOCKED

    def unlock(self):
        self._state = self.STATE_UNLOCKED

    def is_open(self):
        return self._state == self.STATE_UNLOCKED


class TimedDoor(Door):
    def __init__(self):
        super().__init__()
        self.timer_adapter = TimerAdapter(self)

    def timeout(self):
        self.timer_adapter.timeout()


if __name__ == '__main__':
    door = TimedDoor()
    door.unlock()
    print(door.is_open())
    door.timeout()
    print(door.is_open())
