varying float vHeight;
uniform vec3 baseColor;
uniform vec3 shallowColor;
void main() {
	float t = smoothstep(-10.0, 10.0, vHeight);
	vec3 color = mix(baseColor, shallowColor, t);
	gl_FragColor = vec4(color, 1.0);
}
