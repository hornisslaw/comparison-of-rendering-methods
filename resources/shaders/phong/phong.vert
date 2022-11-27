#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 mvp;
uniform mat4 model_matrix;

out vec3 normal;
out vec3 world_position;

void main() {
    gl_Position = mvp * vec4(in_position, 1);
    normal = in_normal;
    world_position = (model_matrix * vec4(in_position, 1)).xyz;
}