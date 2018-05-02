from minigrid import *


def extended_dic(obj_names=[]):
    """
    Extend the OBJECT_TO_IDX dictionaries with additional objects
    :param obj_names: list of strings
    :return: OBJECT_TO_IDX extended
    """
    latest_key = list(OBJECT_TO_IDX)[-1]
    latest_idx = OBJECT_TO_IDX[latest_key]
    new_obj_idx = latest_idx + 1
    for obj_name in obj_names:
        OBJECT_TO_IDX.update({obj_name: new_obj_idx})
        new_obj_idx = new_obj_idx + 1
    # Update index mapping with new object keys
    IDX_TO_OBJECT.update(dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys())))


extended_dic(['water'])


class Water(WorldObj):
    def __init__(self):
        super(Water, self).__init__('water', 'blue')

    def can_overlap(self):
        return True

    def render(self, r):
        self._set_color(r)
        r.drawPolygon([
            (0          , CELL_PIXELS),
            (CELL_PIXELS, CELL_PIXELS),
            (CELL_PIXELS,           0),
            (0          ,           0)
        ])

class UnsafeGrid(Grid):
    """
    Extending Grid methods to support the new objects
    """
    def decode(array):
        width = array.shape[0]
        height = array.shape[1]
        assert array.shape[2] == 3

        grid = UnsafeGrid(width, height)

        for j in range(0, height):
            for i in range(0, width):

                type_idx = array[i, j, 0]
                color_idx = array[i, j, 1]
                open_idx = array[i, j, 2]

                if type_idx == 0:
                    continue

                obj_type = IDX_TO_OBJECT[type_idx]
                color = IDX_TO_COLOR[color_idx]
                is_open = True if open_idx == 1 else 0

                if obj_type == 'wall':
                    v = Wall(color)
                elif obj_type == 'ball':
                    v = Ball(color)
                elif obj_type == 'key':
                    v = Key(color)
                elif obj_type == 'box':
                    v = Box(color)
                elif obj_type == 'door':
                    v = Door(color, is_open)
                elif obj_type == 'locked_door':
                    v = LockedDoor(color, is_open)
                elif obj_type == 'goal':
                    v = Goal()
                elif obj_type == 'water':
                    v = Water()
                else:
                    assert False, "unknown obj type in decode '%s'" % obj_type

                grid.set(i, j, v)

        return grid


class UnsafeMiniGridEnv(MiniGridEnv):

    # Enumeration of possible actions
    class Actions(IntEnum):
        # Turn left, turn right, move forward
        left = 0
        right = 1
        forward = 2

        # Pick up an object
        pickup = 3
        # Drop an object
        drop = 4
        # Toggle/activate an object
        toggle = 5

        # Wait/stay put/do nothing
        wait = 6

    def world_object_type_in_front_of_agent(self, distance=1):

        ax, ay = self.agent_pos
        grid_x, grid_y = ax, ay

        if self.agent_dir == self.agent_directions.right:
            grid_x += distance
        elif self.agent_dir == self.agent_directions.down:
            grid_y += distance
        elif self.agent_dir == self.agent_directions.left:
            grid_x -= distance
        elif self.agent_dir == self.agent_directions.up:
            grid_y -= distance

        if (grid_x >= 0 <= grid_x <= AGENT_VIEW_SIZE) and (grid_y >= 0 <= grid_y < AGENT_VIEW_SIZE):
            world_object = self.grid.get(grid_x, grid_y)
            return world_object if world_object is not None else None
        return None

    def __init__(self, grid_size=16, max_steps=100):
        super().__init__(grid_size, max_steps)
