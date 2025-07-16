from threading import Lock, Thread
from time import time, sleep

from controller.inputs import PlayerInputs, MouseInputs


class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    ATTACKING = 6
    CLIMBING = 3  # New state for ladder climbing

class MapleBot:
    INITIALIZING_SECONDS = 3
    ATTACKING_SECONDS = 5
    TARGET_MEMORY_SECONDS = 3

    stopped = True
    lock = None
    state = None
    monster_targets = []
    player_targets = []
    ladder_targets = []
    screenshot = None
    timestamp = None
    window_offset = (0,0)
    window_w = 0
    window_h = 0
    last_known_monster_target = None
    last_target_time = 0
    attack_start_time = None
    climbing_start_time = None
    climbing_duration = 5.0
    max_ladder_height = 50

    def __init__(self, window_offset, window_size):
        # create a thread lock object
        self.lock = Lock()
        self.timestamp = time()
        # for translating window positions into screen positions
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]
        # start bot in the initializing mode to allow us time to get setup
        self.state = BotState.INITIALIZING
        self.timestamp = time()
        self.player_inputs = PlayerInputs()
        self.mouse_inputs = MouseInputs()

    def get_my_position(self):
        """Get the player's position from player_targets or use window center as fallback"""
        if self.player_targets and len(self.player_targets) > 0:
            return self.player_targets[0]
        else:
            return None

    def calculate_monster_to_player_distance(self):
        """Calculate the distance between the player and the nearest monster"""
        if self.last_known_monster_target is not None:
            player_position = self.get_my_position()
            if player_position is not None:
                distance = abs(player_position[0] - self.last_known_monster_target[0]) + abs(player_position[1] - self.last_known_monster_target[1])
                return distance


    def attack(self):
        """Execute an attack command"""
        print("Executing attack command...")
        for _ in range(self.ATTACKING_SECONDS):
            self.player_inputs.attack()
        sleep(0.01)

    def search_targets(self):
        """ Execute movements to search for targets """
        print("Searching for monsters...")
        self.player_inputs.move_right()
        self.player_inputs.move_right()
        self.player_inputs.move_right()
        self.player_inputs.jump_down()


        self.player_inputs.move_left()
        self.player_inputs.move_left()
        self.player_inputs.move_left()
        self.player_inputs.jump_down()


    def update_targets(self, player_targets, monster_targets, ladder_targets=None):
        """Update the bot's target lists with new detection results"""
        self.lock.acquire()
        self.player_targets = player_targets
        self.monster_targets = monster_targets

        # Update last known monster target if we have valid targets
        if monster_targets and len(monster_targets) > 0:
            self.last_known_monster_target = monster_targets[0]
            self.last_target_time = time()

        if ladder_targets is not None:
            self.ladder_targets = ladder_targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        """Update the bot's screenshot"""
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        """Start the bot in a new thread"""
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        """Stop the bot"""
        self.stopped = True

    def run(self):
        """Main bot loop that handles state transitions"""
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                # Wait for initialization period to complete
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    # Start searching when the waiting period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                    print("Initialization complete - transitioning to SEARCHING state")

            elif self.state == BotState.SEARCHING:
                # Simple state transition logic - if monsters are detected, switch to ATTACKING
                if len(self.monster_targets) > 0:
                    print("Monsters detected - transitioning to ATTACKING state")
                    self.lock.acquire()
                    self.state = BotState.ATTACKING
                    self.attack_start_time = time()
                    self.lock.release()
                else:
                    # No monsters detected
                    print("Searching for targets...")
                    self.search_targets()

            elif self.state == BotState.ATTACKING:
                # Simple attacking logic
                if len(self.monster_targets) > 0:
                    print(f"ATTACKING state: Found {len(self.monster_targets)} monster targets")
                    print("Player position: ", self.get_my_position())
                    self.attack()
                    sleep(0.1)

                    # Reset attack timer if needed
                    current_time = time()
                    if current_time - self.attack_start_time >= self.ATTACKING_SECONDS:
                        print("Attack cycle complete - resetting timer")
                        self.attack_start_time = current_time
                else:
                    # No monsters to attack, return to searching
                    print("No monsters detected - returning to SEARCHING state")
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()

            elif self.state == BotState.CLIMBING:
                # Simple climbing state logic
                current_time = time()
                if self.climbing_start_time is None:
                    self.climbing_start_time = current_time

                if current_time - self.climbing_start_time >= self.climbing_duration:
                    print(f"Finished climbing after {self.climbing_duration:.1f} seconds")
                    self.lock.acquire()
                    self.climbing_start_time = None

                    # Return to searching or attacking based on whether monsters are detected
                    if len(self.monster_targets) > 0:
                        print("Monsters detected after climbing - transitioning to ATTACKING state")
                        self.state = BotState.ATTACKING
                    else:
                        print("No monsters detected after climbing - transitioning to SEARCHING state")
                        self.state = BotState.SEARCHING
                    self.lock.release()
                else:
                    # Still climbing
                    elapsed = current_time - self.climbing_start_time
                    remaining = self.climbing_duration - elapsed
                    print(f"Still climbing: {elapsed:.1f}s elapsed, {remaining:.1f}s remaining")
                    sleep(0.5)

            # Short sleep to prevent CPU overuse
            sleep(0.1)
