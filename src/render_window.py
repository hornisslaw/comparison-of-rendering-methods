import config
import numpy as np
from pathlib import Path

from moderngl import TRIANGLE_STRIP, DEPTH_TEST
from moderngl_window import WindowConfig, run_window_config
from moderngl_window import geometry

from pyrr import Matrix44, Vector3
from shaders.shader_utils import get_shaders


class BaseWindowConfig(WindowConfig):
    gl_version = config.GL_VERSION
    title = config.WINDOW_TITLE
    resource_dir = (Path(__file__).parent.parent / "resources" / "models").resolve()

    def __init__(self, **kwargs):
        super(BaseWindowConfig, self).__init__(**kwargs)

        shaders_dir_path = "../resources/shaders/robot"
        shader_name = "robot"
        # shaders_dir_path = "../resources/shaders/robot"
        # shader_name = "robot"
        shaders = get_shaders(shaders_dir_path)

        self.program = self.ctx.program(
            vertex_shader=shaders[shader_name].vertex_shader,
            geometry_shader=shaders[shader_name].geometry_shader,
            fragment_shader=shaders[shader_name].fragment_shader,
        )
        # print(self.program)
        self.model_load()
        self.init_shaders_variables()

    def model_load(self):
        self.obj_color = None
        if self.argv.model_name:
            self.obj = self.load_scene(self.argv.model_name)
            if self.obj.materials:
                self.obj_color = self.obj.materials[0].color
            self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.program)
        else:
            self.vao = geometry.quad_2d().instance(self.program)

    def init_shaders_variables(self):
        pass

    @classmethod
    def add_arguments(cls, parser):
        # parser.add_argument('--shaders_dir_path', type=str, required=True, help='Path to the directory with shaders')
        # parser.add_argument('--shader_name', type=str, required=True,
        #                     help='Name of the shader to look for in the shader_path directory')
        parser.add_argument(
            "--model_name", type=str, required=False, help="Name of the model to load"
        )

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0, 0.0)
        self.vao.render(TRIANGLE_STRIP)
        pass


class RobotWindow(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(RobotWindow, self).__init__(**kwargs)

    def model_load(self):
        self.objects = {}
        self.objects["head"] = (
            self.load_scene("sphere.obj").root_nodes[0].mesh.vao.instance(self.program)
        )
        self.objects["body"] = (
            self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        )
        self.objects["right_arm"] = (
            self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        )
        self.objects["left_arm"] = (
            self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        )
        self.objects["right_leg"] = (
            self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        )
        self.objects["left_leg"] = (
            self.load_scene("cube.obj").root_nodes[0].mesh.vao.instance(self.program)
        )

    def init_shaders_variables(self):
        # mvp is Model View Projection
        self.mvp = self.program["mvp"]
        self.color = self.program["color"]

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(DEPTH_TEST)
        # self.ctx.enable(moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(
            45.0, self.aspect_ratio, 0.1, 1000.0
        )
        lookat = Matrix44.look_at(
            (-20.0, -15.0, 5.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
        )

        PxL = projection * lookat
        # Head
        # Set shader color variable
        self.color.value = (0, 1, 0)
        head_translation = Matrix44.from_translation(Vector3([0, 0, 5]))
        self.mvp.write((PxL * head_translation).astype("f4"))
        # Render head
        self.objects["head"].render()

        # Body
        self.color.value = (1, 0, 0)
        body_translation = Matrix44.from_translation(Vector3([0, 0, 2]))
        body_scale = Matrix44.from_scale(Vector3([1, 1, 2]))
        self.mvp.write((PxL * body_translation * body_scale).astype("f4"))
        self.objects["body"].render()

        # Arms
        arms_scale = Matrix44.from_scale(Vector3([0.5, 0.5, 1.25]))
        # Right Arm
        self.color.value = (0, 0, 1)
        right_arm_translation = Matrix44.from_translation(Vector3([0, 3, 3]))
        right_arm_rotation = Matrix44.from_x_rotation(-np.pi / 4)
        self.mvp.write(
            (PxL * right_arm_translation * right_arm_rotation * arms_scale).astype("f4")
        )
        self.objects["right_arm"].render()
        # Render left arm
        self.color.value = (0, 1, 1)
        left_arm_translation = Matrix44.from_translation(Vector3([0, -3, 3]))
        arm_left_rotation = Matrix44.from_x_rotation(np.pi / 4)
        self.mvp.write(
            (PxL * left_arm_translation * arm_left_rotation * arms_scale).astype("f4")
        )
        self.objects["left_arm"].render()

        # Legs
        scale_leg = Matrix44.from_scale(Vector3([0.5, 0.5, 1.75]))
        # Right leg
        self.color.value = (1, 0, 1)
        right_leg_translation = Matrix44.from_translation(Vector3([0, 2, -1.5]))
        right_leg_rotation = Matrix44.from_x_rotation(-np.pi / 6)
        self.mvp.write(
            (PxL * right_leg_translation * right_leg_rotation * scale_leg).astype("f4")
        )
        self.objects["right_leg"].render()
        # Left leg
        self.color.value = (1, 1, 0)
        left_leg_translation = Matrix44.from_translation(Vector3([0, -2, -1.5]))
        left_leg_rotation = Matrix44.from_x_rotation(np.pi / 6)
        self.mvp.write(
            (PxL * left_leg_translation * left_leg_rotation * scale_leg).astype("f4")
        )
        self.objects["left_leg"].render()
