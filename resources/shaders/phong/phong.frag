#version 330

in vec3 normal;
in vec3 world_position;

uniform mat4 mvp;
uniform vec3 material_diffuse;
uniform vec3 material_specular;
uniform float shininess;

const vec3 light_position = vec3(-6, 5, 2);
// const vec3 light_position = vec3(6, 3, -2);
const vec3 light_ambient = vec3(0.2, 0.2, 0.2);
const vec3 light_diffuse = vec3(1, 1, 1);
const vec3 light_specular = vec3(1, 1, 1);

out vec4 f_color;

void main()
{
    //BLINN PHONG
    vec3 ambient = vec3(0, 0, 0);
    vec3 diffuse = vec3(0, 0, 0);
    vec3 specular = vec3(0, 0, 0);

    //ambient
    ambient = light_ambient * material_diffuse;

    //diffuse
    float cosNL = 0;
    vec3 N = normalize(normal);
    vec3 L = normalize(light_position - world_position);
    cosNL = max(dot(N, L), 0.0);

    diffuse = light_diffuse * material_diffuse * cosNL;

    //specular
    float cosNH = 0;
    vec3 V = normalize(-world_position);
    vec3 H = normalize(L + V);
    cosNH = pow(max(dot(H, N), 0.0), shininess);

    specular = light_specular * material_specular * cosNH;

    f_color = vec4(ambient + diffuse + specular, 1);
}
