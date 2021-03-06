from rect import Rect
from tile import Tile
import libtcodpy as libtcod

MAP_HEIGHT = 200
MAP_WIDTH = 200
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

def create_room(room, dungeon_map):
    #go through the tiles in the rectangle and make them passable
    for x in xrange(room.x1, room.x2 + 1):
        for y in xrange(room.y1, room.y2 + 1):
            dungeon_map[x][y].blocked = False
            dungeon_map[x][y].block_sight = False

    return dungeon_map

def create_h_tunnel(x1, x2, y, dungeon_map):
    for x in xrange(min(x1, x2), max(x1, x2) + 1):
        dungeon_map[x][y].blocked = False
        dungeon_map[x][y].block_sight = False

    return dungeon_map

def create_v_tunnel(y1, y2, x, dungeon_map):
    #vertical tunnel
    for y in xrange(min(y1, y2), max(y1, y2) + 1):
        dungeon_map[x][y].blocked = False
        dungeon_map[x][y].block_sight = False

    return dungeon_map

def center(self):
    center_x = (self.x1 + self.x2) / 2
    center_y = (self.y1 + self.y2) / 2
    return (center_x, center_y)

def intersect(self, other):
    #returns true if this rectangle intersects with another one
    return (self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1)

def make_map():
    num_rooms = 0
    player = {'x' : 0, 'y' : 0}
    dungeon_map = [[], []]

    for r in xrange(MAX_ROOMS):
        #random width and height
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        #random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)


        #"Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        #run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break


        if not failed:
            #this means there are no intersections, so this room is valid

            #"paint" it to the map's tiles
            dungeon_map = create_room(new_room, dungeon_map)

            #center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            #optional: print "room number" to see how the map drawing worked
            #          we may have more than ten rooms, so print 'A' for the first room, 'B' for the next...
            room_no = Object(new_x, new_y, chr(65+num_rooms), libtcod.white)
            objects.insert(0, room_no) #draw early, so monsters are drawn on top`

            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y

        else:
            #all rooms after the first:
            #connect it to the previous room with a tunnel

            #center coordinates of previous room
            (prev_x, prev_y) = rooms[num_rooms-1].center()

            #draw a coin (random number that is either 0 or 1)
            if libtcod.random_get_int(0, 0, 1) == 1:
                #first move horizontally, then vertically
                dungeon_map = create_h_tunnel(prev_x, new_x, prev_y, dungeon_map)
                dungeon_map = create_v_tunnel(prev_y, new_y, new_x, dungeon_map)
            else:
                #first move vertically, then horizontally
                dungeon_map = create_v_tunnel(prev_y, new_y, prev_x, dungeon_map)
                dungeon_map = create_h_tunnel(prev_x, new_x, new_y, dungeon_map)

        #finally, append the new room to the list
        rooms.append(new_room)
        num_rooms += 1