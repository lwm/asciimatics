from copy import deepcopy
import sys
from asciimatics.exceptions import ResizeScreenError
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Sprite, BannerText

namco = """
88888888b.  8888888b. 8888888888b. .d88888888 .d888888b.
88      88         88 88   88   88 88         88      88
88      88 .d88888888 88   88   88 88         88      88
88      88 88      88 88   88   88 88         88      88
88      88 `888888888 88   88   88 `888888888 `8888888P'
"""

dot = """${7,2,7}####
${7,2,7}####
"""

pac_man = """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
{0}##########################
{0}##########################
{0}##########################
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
{0}##########################
{0}##########################
              {0}############
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
{0}##########################
      {0}####################
              {0}############
      {0}####################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
  {0}############${{4,2,0}}  ${{7,2,7}}  {0}######
      {0}####################
          {0}################
              {0}############
          {0}################
      {0}####################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}############${{7,2,7}}    {0}######
    {0}##########${{4,2,0}}  ${{7,2,7}}  {0}######
        {0}##################
            {0}##############
              {0}############
            {0}##############
        {0}##################
    {0}####################
  {0}######################
    {0}##################
        {0}##########
"""

pac_man_right = """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}##########################
{0}##########################
{0}##########################
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}##########################
{0}##########################
{0}############
{0}##########################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}##########################
{0}####################
{0}############
{0}####################
{0}##########################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}############
{0}####################
{0}################
{0}############
{0}################
{0}#####################
  {0}######################
  {0}######################
    {0}##################
        {0}##########
""", """
        {0}##########
    {0}##################
  {0}######${{7,2,7}}    {0}############
  {0}######${{7,2,7}}  ${{4,2,0}}  {0}##########
{0}##################
{0}##############
{0}############
{0}##############
{0}##################
  {0}####################
  {0}######################
    {0}##################
        {0}##########
"""

ghost = """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}##########################
{0}####${{7,2,0}}  {0}########${{7,2,0}}  {0}########
{0}##${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
{0}######${{7,2,0}}  {0}########${{7,2,0}}  {0}########
{0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
{0}########${{7,2,0}}  {0}########${{7,2,0}}  {0}########
  {0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
  {0}########${{7,2,0}}  {0}########${{7,2,0}}  {0}######
    {0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}####
""", """
          {0}########
      {0}################
    {0}####################
  {0}##${{7,2,7}}....{0}########${{7,2,7}}....{0}######
  ${{7,2,7}}........{0}####${{7,2,7}}........{0}####
  ${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}####
{0}##${{4,2,4}}    ${{7,2,7}}....{0}####${{4,2,4}}    ${{7,2,7}}....{0}######
{0}####${{7,2,7}}....{0}########${{7,2,7}}....{0}########
{0}############################
{0}############################
{0}############################
{0}##${{7,2,0}}  {0}########${{7,2,0}}  {0}########${{7,2,0}}  {0}####
      {0}####${{7,2,0}}      {0}####${{7,2,0}}      {0}##
"""

scared_ghost = """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}####${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}##
${4,2,4}##${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}##${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}####
      ${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}##
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
  ${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}######
    ${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}########${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########
  ${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
""", """
          ${4,2,4}########
      ${4,2,4}################
    ${4,2,4}####################
  ${4,2,4}########################
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
  ${4,2,4}####${7,2,7}    ${4,2,4}########${7,2,7}    ${4,2,4}####
${4,2,4}############################
${4,2,4}############################
${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####
${4,2,4}##${7,2,7}  ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}    ${4,2,4}####${7,2,7}  ${4,2,4}##
${4,2,4}############################
${4,2,4}######${7,2,0}  ${4,2,4}########${7,2,0}  ${4,2,4}########
${4,2,4}####${7,2,0}      ${4,2,4}####${7,2,0}      ${4,2,4}####
"""

eyes = """
    ${4,2,4}####${4,2,0}        ${4,2,4}####
  ${7,2,7}..${4,2,4}####${7,2,7}..${7,2,0}    ${7,2,7}..${4,2,4}####${7,2,7}..
  ${7,2,7}........${7,2,0}    ${7,2,7}........
  ${7,2,7}........${7,2,0}    ${7,2,7}........
    ${7,2,7}....${7,2,0}        ${7,2,7}....


"""

# Globals used for pacman animation
direction = 1
value = 0


def cycle():
    global value, direction
    value += direction
    if value <= 0 or value >= 4:
        direction = -direction
    return value


class PacMan(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        images = []
        images_right = []
        colour = Screen.COLOUR_YELLOW if screen.colours <= 16 else 11
        for image in pac_man:
            images.append(image.format("${%d,2,%d}" % (colour, colour)))
        for image in pac_man_right:
            images_right.append(image.format("${%d,2,%d}" % (colour, colour)))
        super(PacMan, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=images, animation=cycle),
                "left": StaticRenderer(images=images, animation=cycle),
                "right": StaticRenderer(images=images_right, animation=cycle),
            },
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)

    def _update(self, frame_no):
        super(PacMan, self)._update(frame_no)
        for effect in self._scene.effects:
            if isinstance(effect, ScaredGhost) and self.overlaps(effect):
                effect.eaten()


class Ghost(Sprite):
    def __init__(self, screen, path, colour=1, start_frame=0, stop_frame=0):
        images = []
        for image in ghost:
            images.append(image.format("${%d,2,%d}" % (colour, colour)))
        super(Ghost, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=images),
            },
            colour=colour,
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)


class ScaredGhost(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        super(ScaredGhost, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=scared_ghost),
            },
            colour=Screen.COLOUR_BLUE,
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)
        self._eaten = False

    def eaten(self):
        # Already eaten - just ignore
        if self._eaten:
            return

        # Allow one more iteration for this Sprite to clear itself up.
        self._eaten = True
        self._delete_count = 2

        # Spawn the eyes to run away
        path = Path()
        path.jump_to(self._old_x + 12, self._old_y + 4)
        path.move_straight_to(
            self._old_x + 12, -8, (self._old_y + 12) // 2)
        path.wait(100)
        self._scene.add_effect(Eyes(self._screen, path))


class Eyes(Sprite):
    def __init__(self, screen, path, start_frame=0, stop_frame=0):
        super(Eyes, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=[eyes]),
            },
            colour=Screen.COLOUR_BLUE,
            path=path,
            start_frame=start_frame,
            stop_frame=stop_frame)


class EatingScene(Scene):
    def __init__(self, screen):
        super(EatingScene, self).__init__([], 240 + screen.width)
        self._screen = screen
        self._reset_count = 0

    def reset(self, old_scene=None, screen=None):
        super(EatingScene, self).reset(old_scene, screen)

        # Recreate all the elements.
        centre = (self._screen.width // 2, self._screen.height // 2)
        path = Path()
        path.jump_to(-16, centre[1])
        path.move_straight_to(
            self._screen.width + 16, centre[1], (self._screen.width + 16) // 3)
        path.wait(100)
        path2 = Path()
        path2.jump_to(-16, centre[1])
        path2.move_straight_to(
            self._screen.width + 16, centre[1], self._screen.width + 16)
        path2.wait(100)

        # Take a copy of the list before using it to remove all effects.
        for effect in self.effects[:]:
            self.remove_effect(effect)

        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2)))
        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2), start_frame=60))
        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2), start_frame=120))
        self.add_effect(
            ScaredGhost(self._screen, deepcopy(path2), start_frame=180))
        self.add_effect(PacMan(self._screen, path, start_frame=240))


def demo(screen):
    scenes = []
    centre = (screen.width // 2, screen.height // 2)

    # Title
    effects = [
        BannerText(screen,
                   ColourImageFile(screen, "pacman.png", 16, 0, True),
                   (screen.height - 16) // 2,
                   Screen.COLOUR_WHITE),
        Print(screen,
              StaticRenderer(images=["A tribute to the classic 80's "
                                     "video game by Namco."]),
              screen.height - 1)
    ]
    scenes.append(Scene(effects, 0))

    # Scene 1 - run away, eating dots
    path = Path()
    path.jump_to(screen.width + 16, centre[1])
    path.move_straight_to(-16, centre[1], (screen.width + 16) // 3)
    path.wait(100)

    if screen.colours <= 16:
        inky = 6
        pinky = 5
        blinky = 1
        clyde = 2
    else:
        inky = 14
        pinky = 201
        blinky = 9
        clyde = 208

    effects = [
        PacMan(screen, path),
        Ghost(screen, deepcopy(path), inky, start_frame=40),
        Ghost(screen, deepcopy(path), pinky, start_frame=60),
        Ghost(screen, deepcopy(path), blinky, start_frame=80),
        Ghost(screen, deepcopy(path), clyde, start_frame=100),
    ]

    for x in range(5, screen.width, 16):
        effects.insert(0,
                       Print(screen,
                             StaticRenderer(images=[dot]),
                             screen.height // 2,
                             x=x,
                             speed=1,
                             stop_frame=4))

    scenes.append(Scene(effects, 100 + screen.width))

    # Scene 2 - Chase ghosts after a power pill
    scenes.append(EatingScene(screen))

    # Scene 3 - Thanks...
    effects = [
        Print(screen, FigletText("Thank you,"), screen.height // 3 - 3,
              colour=Screen.COLOUR_RED),
        Print(screen,
              StaticRenderer(images=[namco]),
              screen.height * 2 // 3 - 2,
              colour=Screen.COLOUR_RED),
        Print(screen,
              StaticRenderer(images=["< Press X to exit. >"]),
              screen.height - 1)
    ]
    scenes.append(Scene(effects, 0))

    screen.play(scenes, stop_on_resize=True, repeat=False)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
