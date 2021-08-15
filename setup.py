import cx_Freeze

executables = [cx_Freeze.Executable("test.py")]

cx_Freeze.setup(
    name="SpaceGame",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["Assets/background1.png", "Assets/bullet.png", "Assets/enemy.png",
                                             "Assets/heart.png",
                                             "Assets/spaceship.png", "Assets/music.png", "Assets/mute.png",
                                             "Assets/enemy1.png", "Assets/enemy2.png",
                                             "Assets/enemy3.png", "Assets/shot.mp3", "Assets/SpaceGame.mp3"]}},
    executables=executables
)
