from os import path
from rx.subject import BehaviorSubject


class Settings:
    resource_dir = path.join(__file__, "../resources")
    objects_dir = path.join(resource_dir, "objects")
    programs_dir = path.join(resource_dir, "programs")
    textures_dir = path.join(resource_dir, "textures")

    default_object = "objects/suzanne.obj"
    default_skybox = "textures/skybox_desert.png"
    default_use_hard_shadow = True
    default_use_soft_shadow = False

    object = BehaviorSubject(default_object)
    skybox = BehaviorSubject(default_skybox)
    use_hard_shadow = BehaviorSubject(default_use_hard_shadow)
    use_soft_shadow = BehaviorSubject(default_use_soft_shadow)


settings = Settings()
