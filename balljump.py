from ursina import *

app = Ursina()

# Basic environment
Sky()
DirectionalLight()

# Ground
ground = Entity(model='cube', scale=(50, 1, 50), color=color.green, position=(0, -0.5, 0), collider='box')

# Platforms
platforms = [
    Entity(model='cube', color=color.azure, scale=(4, 0.5, 4), position=(5, 1, 0), collider='box'),
    Entity(model='cube', color=color.azure, scale=(4, 0.5, 4), position=(10, 2.5, 2), collider='box'),
    Entity(model='cube', color=color.azure, scale=(4, 0.5, 4), position=(15, 4, 0), collider='box'),
    Entity(model='cube', color=color.azure, scale=(4, 0.5, 4), position=(20, 5.5, -2), collider='box'),
]

# Goal (with trigger collider for precise detection)
goal = Entity(
    model='sphere',
    color=color.yellow,
    scale=1,
    position=(24, 7, -2),
    collider='sphere',
    name="Goal"
)

# Player setup
player = Entity(model='cube', color=color.orange, scale=(1, 1, 1), position=(0, 2, 0), collider='box')

# Camera follow
camera.parent = player
camera.position = (0, 10, -20)
camera.rotation_x = 30
camera.fov = 80

# Physics
velocity_y = 0
gravity = 9.8
jump_force = 6
speed = 5
is_grounded = False

# UI message
win_text = Text(text="", origin=(0, 0), scale=2, color=color.red, visible=False)

def update():
    global velocity_y, is_grounded

    # Movement
    move = Vec3(held_keys['d'] - held_keys['a'], 0, held_keys['w'] - held_keys['s']).normalized()
    player.position += move * speed * time.dt

    # Gravity
    velocity_y -= gravity * time.dt
    player.y += velocity_y * time.dt
    is_grounded = False

    # Collision with ground/platforms
    hit = player.intersects()
    if hit.hit and velocity_y <= 0:
        player.y = hit.entity.world_y + hit.entity.scale_y / 2 + player.scale_y / 2
        velocity_y = 0
        is_grounded = True

    # Jumping
    if is_grounded and held_keys['space']:
        velocity_y = jump_force

    # Check win condition
    if player.intersects(goal).hit:
        win_text.text = "🎉 YOU WIN!"
        win_text.visible = True
        invoke(application.quit, delay=2)

app.run()
