import viz
import vizfx
import vizact
import vizconnect
import vizproximity
import tools.grabber
import random
import math

# Basic setup

viz.go()

# PC mode
vizconnect.go('vizconnect_config.py')
movement_tracker = vizconnect.getTracker('mouse_and_keyboard_walking').getNode3d()

# VR mode
# vizconnect.go('headset_config.py')
# movement_tracker = vizconnect.getTracker('head_tracker').getNode3d()

viz.MainView.collision(viz.ON)

# Constants

ORIGINAL_ROOM_POS = [0.0, 0.0, 2.0]

# Target positions in the original unshifted villa world.
# These are eye positions, not floor positions.

# 3ds Max box position is X=4.844, Y=19.634, Z=5.770
# Vizard uses X, Z, Y.
# The villa has plus 2 on Vizard Z.
# Eye height is about 1.5 meters above the upper floor.
UPPER_FLOOR_EYE_POS = [4.844, 7.300, 21.634]

# Return target on the ground floor.
# Change this if you want to return to another ground-floor position.
GROUND_FLOOR_EYE_POS = [0.0, 1.82, 0.0]

current_room_pos = ORIGINAL_ROOM_POS[:]
movable_world_nodes = []

# Utility functions

def addVec(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def subVec(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def registerMovableWorldNode(node):
    if node is not None:
        movable_world_nodes.append(node)
    return node

def moveNodeByDelta(node, delta):
    try:
        old_pos = node.getPosition()
        node.setPosition(addVec(old_pos, delta))
    except Exception as e:
        print("Could not move node:", node, e)

def setVillaPosition(new_room_pos):
    global current_room_pos

    delta = subVec(new_room_pos, current_room_pos)

    room.setPosition(new_room_pos)

    for node in movable_world_nodes:
        moveNodeByDelta(node, delta)

    current_room_pos = new_room_pos[:]

def getRoomPositionForTarget(target_eye_pos):
    player_pos = viz.MainView.getPosition(viz.ABS_GLOBAL)

    target_local_offset = subVec(target_eye_pos, ORIGINAL_ROOM_POS)

    return [
        player_pos[0] - target_local_offset[0],
        player_pos[1] - target_local_offset[1],
        player_pos[2] - target_local_offset[2]
    ]

def teleportToUpperFloor():
    print("Moving villa so player appears upstairs")
    new_room_pos = getRoomPositionForTarget(UPPER_FLOOR_EYE_POS)
    print("New room position:", new_room_pos)
    setVillaPosition(new_room_pos)

def teleportToGroundFloor():
    print("Moving villa so player appears downstairs")
    new_room_pos = getRoomPositionForTarget(GROUND_FLOOR_EYE_POS)
    print("New room position:", new_room_pos)
    setVillaPosition(new_room_pos)

# Environment

env = viz.addEnvironmentMap('sunset.jpg')
sky = viz.add('skydome.dlc')
sky.texture(env)

room = viz.addChild('Roman Villa.gltf')
room.setPosition(ORIGINAL_ROOM_POS)

# Keyboard teleport controls
vizact.onkeydown('u', teleportToUpperFloor)
vizact.onkeydown('j', teleportToGroundFloor)

# Positional sound

sound_node = viz.addGroup(pos=[0, 0, 0])
center_sound = sound_node.playsound('bird sound.wav', viz.LOOP)
center_sound.minmax(4, 5)

# Keep bird sound attached to the shifted villa world.
registerMovableWorldNode(sound_node)

# Footstep sound

footstep_sound = viz.addAudio('footsteps.wav', loop=viz.ON)
footstep_sound.volume(0.8)

last_position = [0, 0, 0]
is_playing = False
MOVEMENT_THRESHOLD = 0.001

def checkFootsteps():
    global last_position, is_playing

    current_pos = movement_tracker.getPosition()

    dx = current_pos[0] - last_position[0]
    dz = current_pos[2] - last_position[2]
    distance = (dx ** 2 + dz ** 2) ** 0.5

    if distance > MOVEMENT_THRESHOLD:
        if not is_playing:
            footstep_sound.play()
            is_playing = True
    else:
        if is_playing:
            footstep_sound.stop()
            is_playing = False

    last_position = list(current_pos)

vizact.onupdate(viz.PRIORITY_INPUT, checkFootsteps)

# Transparent objects

transparent_names = [
    'FixedWindow1', 'FixedWindow2',
    'Plane002', 'Plane013',
    'Box201', 'Box202', 'Box203', 'Box204', 'Box205'
]

for name in transparent_names:
    obj = room.getChild(name)
    if obj:
        obj.alpha(0.6)
        obj.enable(viz.BLEND)
        obj.drawOrder(100)

# Lighting

headLight = viz.MainView.getHeadLight()
headLight.disable()
vizact.onkeydown(' ', headLight.enable)

sun = vizfx.addDirectionalLight(euler=(45, 120, 0))
sun.color([1.0, 0.95, 0.85])
sun.intensity(0.6)
sun.ambient([0.15, 0.15, 0.18])

# Torches and fires
# 3ds Max format is X, Y, Z.
# Vizard format is X, Z, Y.
# Room has ORIGINAL_ROOM_POS equal to [0, 0, 2].
# Because of this, plus 2 is added to Vizard Z.

torch_coords = [
    [16.152, 1.999, 27.855 + 2],
    [-16.113, 1.999, 28.939 + 2],
    [-7.814, 1.999, -0.091 + 2],
    [7.793, 1.999, -0.114 + 2],
    [16.152, 1.999, -0.206 + 2],
    [-16.095, 1.999, 0.720 + 2],
    [-5.852, 2.511, -32.298 + 2],
    [-16.095, 1.999, -12.853 + 2],
]

fire_only_coords = [
    [16.152, 1.999, -12.937 + 2],
    [-6.127, 1.999, 23.782 + 2],
    [6.000, 1.999, 23.427 + 2],
    [13.167, 1.999, 15.250 + 2],
    [-11.362, 1.999, 15.250 + 2],
    [-12.045, 1.999, 14.200 + 2],
    [11.932, 1.999, 14.200 + 2],
]

torch_lights = []
torch_fires = []
fire_only = []

print("Setting up {} torches with lights and {} fire only locations".format(
    len(torch_coords), len(fire_only_coords)
))

def createTorchLight(coord, index):
    light = vizfx.addPointLight(pos=coord)
    light.color([1.0, 0.55, 0.2])

    if index == 6:
        light.intensity(4.5)
        light.linearAttenuation(0.08)
    else:
        light.intensity(2.5)
        light.linearAttenuation(0.15)

    registerMovableWorldNode(light)
    return light

def createFire(coord, scale):
    fire_obj = viz.add('fire.osg', pos=coord)
    fire_obj.hasparticles()
    fire_obj.enable(viz.EMITTERS)
    fire_obj.setScale(scale)
    registerMovableWorldNode(fire_obj)
    return fire_obj

for i, coord in enumerate(torch_coords):
    try:
        torch_lights.append(createTorchLight(coord, i))
        print("Torch light created")
    except Exception as e:
        print("Error creating torch light:", e)

    try:
        torch_fires.append(createFire(coord, [0.3, 0.3, 0.3]))
        print("Torch fire created")
    except Exception as e:
        print("Error creating torch fire:", e)

for coord in fire_only_coords:
    try:
        fire_only.append(createFire(coord, [0.3, 0.3, 0.3]))
        print("Fire only object created")
    except Exception as e:
        print("Error creating fire only object:", e)

print("Total torches created: {} lights, {} fires with light, {} fires without light".format(
    len(torch_lights), len(torch_fires), len(fire_only)
))

def flickerTorch(light):
    intensity_variation = random.uniform(1.4, 1.6)
    light.intensity(intensity_variation)

def updateTorches():
    for light in torch_lights:
        flickerTorch(light)

vizact.ontimer(0.15, updateTorches)

# Fire pit

fire_pit_pos = [-0.095, 0.5, 23.682]

fire_pit_light = vizfx.addPointLight(pos=fire_pit_pos)
fire_pit_light.color([1.0, 0.4, 0.1])
fire_pit_light.intensity(4)
fire_pit_light.linearAttenuation(0.1)
registerMovableWorldNode(fire_pit_light)

fire_pit_fire = viz.add('fire.osg', pos=fire_pit_pos)
fire_pit_fire.hasparticles()
fire_pit_fire.enable(viz.EMITTERS)
fire_pit_fire.setScale([2.0, 2.0, 2.0])
registerMovableWorldNode(fire_pit_fire)

# Grabbable items

amphorae_names = ['Amphorae{}'.format(i) for i in range(1, 8)]
harp_names = ['Harp 1', 'Harp 2']
vase_names = ['Vase{}'.format(i) for i in range(1, 26)]
helmet_names = ['helmet glad', 'Chalcidian', 'helmet', 'IllyriaHelmet']
other_items = ['Atlas', 'Pharaoh', 'Xylospongium', 'Bowl with grapes']

item_names = amphorae_names + harp_names + ['Gladius'] + vase_names + helmet_names + other_items

grabber = vizconnect.getRawTool('grabber')

items = []
harps = []
harp_sounds = {}
item_text_objects = {}

item_descriptions = {
    'helmet glad': "Gladiatorial helmet.\nA prize of honor from a skilled fighter.\nHandle with care - may inspire sudden heroic acts!",
    'Chalcidian': "Chalcidian helmet.\nGreek war trophy from campaigns in the eastern Mediterranean.\nStylish and battle tested.",
    'helmet': "Attic helmet.\nWar trophy, possibly from the Battle of Actium.\nPerfect for dramatic entrances.",
    'IllyriaHelmet': "Illyrian helmet.\nTrophy from northern Balkan campaigns.\nA little more barbaric than the rest.",
    'Gladius': "Roman gladius.\nStandard short sword used by legionaries in battle.\nCaution: may provoke sudden urges for heroism.",
    'Atlas': "Statuette of Atlas, a gift from a Greek in Athens.\nThe Earth was lost on the journey back home.",
    'Pharaoh': "Spoil of war following Cleopatra and Mark Antony defeat,\nat the Battle of Actium. Probably portrait of Ptolemy I Soter.\nProperty status: no longer Egyptian.",
    'Bowl with grapes': "A bowl of fresh Mediterranean grapes.\nA symbol of wealth and the primary source\nfor the Empire favorite beverage: wine.",
    'Xylospongium': "The Xylospongium, ancient sponge on a stick.\nThe Roman solution for personal hygiene in communal latrines,\nshared among all visitors and kept in a bucket of vinegar."
}

def makeItemDescription(item_name):
    display_name = ''.join([char for char in item_name if not char.isdigit()])
    return item_descriptions.get(item_name, display_name + "\nAncient Roman artifact")

def createItemText(description):
    text3d = viz.addText3D(description, pos=[0, 0, 0])
    text3d.setScale([0.05, 0.05, 0.05])
    text3d.color(viz.WHITE)
    text3d.font('Times New Roman')
    text3d.resolution(2.0)
    text3d.alignment(viz.ALIGN_CENTER_CENTER)
    text3d.billboard(viz.BILLBOARD_VIEW)
    text3d.visible(viz.OFF)
    text3d.drawOrder(1000)
    text3d.disable(viz.DEPTH_TEST)

    registerMovableWorldNode(text3d)
    return text3d

for item_name in item_names:
    item = room.getChild(item_name)
    if not item:
        continue

    items.append(item)

    if item_name in harp_names:
        harps.append(item)
        harp_sounds[item] = viz.addAudio('Harp Sound.wav')
        harp_sounds[item].stop()

    description = makeItemDescription(item_name)
    item_text_objects[item] = createItemText(description)

grabber.setItems(items)

# Door system

door_states = {}
door_objects = []
door_transforms = {}
door_sensors = {}
door_initial_angles = {}

grabbed_door = None
grab_start_pos = None
door_grab_angle = None
grab_button_was_pressed = False

manager = vizproximity.Manager()
manager.setDebug(viz.OFF)

target = vizproximity.Target(viz.MainView)
manager.addTarget(target)

door_names = ['Door Leaf {}'.format(i) for i in range(1, 21)]
door_names += [
    'Door Leaf 022',
    'Door Leaf 034',
    'Door Leaf 035',
    'Door Leaf 036',
    'Door Leaf 037',
    'Door Leaf 038',
    'Door Leaf 039',
    'Door Leaf 040',
]

for door_name in door_names:
    door_visual = room.getChild(door_name)
    door_transform = room.getTransform(door_name)

    if door_visual and door_transform:
        door_objects.append(door_visual)
        door_transforms[door_visual] = door_transform
        door_states[door_visual] = 0
        door_initial_angles[door_visual] = door_transform.getEuler()[0]

        sensor = vizproximity.Sensor(vizproximity.Sphere(4), source=door_transform)
        manager.addSensor(sensor)
        door_sensors[door_visual] = sensor
    else:
        print("Door not found:", door_name)

grabber.setItems(items)

# PC and VR mode helpers

try:
    vr_hand_tracker = vizconnect.getTracker('r_hand_tracker')
    IS_VR_MODE = vr_hand_tracker is not None
except:
    IS_VR_MODE = False

if IS_VR_MODE:
    print("Running in VR mode")
else:
    print("Running in PC mode")

def getHandTracker():
    if IS_VR_MODE:
        return vizconnect.getTracker('r_hand_tracker').getNode3d()
    return vizconnect.getTracker('mouse_scroll_wheel').getNode3d()

def getHandPosition():
    try:
        grabber_tool = vizconnect.getTool('grabber')
        if grabber_tool:
            return grabber_tool.getNode3d().getPosition(viz.ABS_GLOBAL)
    except:
        pass

    return getHandTracker().getPosition(viz.ABS_GLOBAL)

def isGrabButtonPressed():
    if IS_VR_MODE:
        try:
            rawInput = vizconnect.getConfiguration().getRawDict('input')
            if 'r_hand_input' in rawInput:
                return rawInput['r_hand_input'].isButtonDown(2)
        except:
            pass
        return False

    return viz.mouse.getState() & viz.MOUSEBUTTON_LEFT

# Door drag logic

def updateGrabbedDoor(button_pressed):
    global grabbed_door, grab_start_pos, door_grab_angle, grab_button_was_pressed

    if not button_pressed:
        print("Door released")
        grabbed_door = None
        grab_start_pos = None
        door_grab_angle = None
        grab_button_was_pressed = False
        return

    current_pos = getHandPosition()
    door_transform = door_transforms[grabbed_door]
    door_pos = door_transform.getPosition(viz.ABS_GLOBAL)

    dx_current = current_pos[0] - door_pos[0]
    dz_current = current_pos[2] - door_pos[2]
    current_angle = math.degrees(math.atan2(dx_current, dz_current))

    dx_start = grab_start_pos[0] - door_pos[0]
    dz_start = grab_start_pos[2] - door_pos[2]
    start_angle = math.degrees(math.atan2(dx_start, dz_start))

    angle_delta = (current_angle - start_angle) * 2.0
    new_angle = door_grab_angle + angle_delta
    new_angle = max(0, min(90, new_angle))

    initial_angle = door_initial_angles[grabbed_door]
    current_euler = door_transform.getEuler()
    door_transform.setEuler([initial_angle + new_angle, current_euler[1], current_euler[2]])

    door_states[grabbed_door] = new_angle

def tryStartDoorGrab():
    global grabbed_door, grab_start_pos, door_grab_angle

    hand_pos = getHandPosition()
    print("Click detected - Hand position: {:.2f}, {:.2f}, {:.2f}".format(
        hand_pos[0], hand_pos[1], hand_pos[2]
    ))

    GRAB_DISTANCE = 1.5
    closest_door = None
    closest_dist = GRAB_DISTANCE

    for door in door_objects:
        door_transform = door_transforms[door]
        door_pos = door_transform.getPosition(viz.ABS_GLOBAL)

        dx = hand_pos[0] - door_pos[0]
        dy = hand_pos[1] - door_pos[1]
        dz = hand_pos[2] - door_pos[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)

        print("Door at {:.2f}, {:.2f}, {:.2f} - distance {:.2f}m".format(
            door_pos[0], door_pos[1], door_pos[2], dist
        ))

        if dist < closest_dist:
            closest_dist = dist
            closest_door = door

    if closest_door is not None:
        grabbed_door = closest_door
        grab_start_pos = hand_pos
        door_grab_angle = door_states[grabbed_door]
        print("Door grabbed - drag to open or close. Distance {:.2f}m".format(closest_dist))
    else:
        print("No door in range. Max distance {:.2f}m".format(GRAB_DISTANCE))

def updateDoorDrag():
    global grab_button_was_pressed

    button_pressed = isGrabButtonPressed()

    if grabbed_door is not None:
        updateGrabbedDoor(button_pressed)
        return

    if button_pressed and not grab_button_was_pressed:
        tryStartDoorGrab()

    grab_button_was_pressed = button_pressed

vizact.onupdate(viz.PRIORITY_INPUT + 1, updateDoorDrag)

# Item grab and release logic

def onGrab(e):
    grabbed_object = e.grabbed

    if grabbed_object in harps:
        harp_sounds[grabbed_object].play()

    if grabbed_object not in item_text_objects:
        return

    text3d = item_text_objects[grabbed_object]
    text3d.visible(viz.ON)

    def updateTextPosition():
        if not text3d.getVisible():
            return

        cam_pos = viz.MainView.getPosition()
        cam_euler = viz.MainView.getEuler()

        forward = viz.Matrix.euler(cam_euler[0], 0, 0).getForward()
        forward_offset = 1.5

        text_pos = [
            cam_pos[0] + forward_offset * forward[0],
            cam_pos[1] - 0.2,
            cam_pos[2] + forward_offset * forward[2]
        ]

        text3d.setPosition(text_pos)

    text3d.update_action = vizact.onupdate(0, updateTextPosition)

def onRelease(e):
    released_object = e.released

    if released_object in harps:
        harp_sounds[released_object].stop()

    if released_object not in item_text_objects:
        return

    text3d = item_text_objects[released_object]
    text3d.visible(viz.OFF)

    if hasattr(text3d, 'update_action'):
        text3d.update_action.remove()

viz.callback(tools.grabber.GRAB_EVENT, onGrab)
viz.callback(tools.grabber.RELEASE_EVENT, onRelease)