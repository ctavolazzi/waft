varying float vHeight;
uniform vec3 baseColor;
uniform vec3 shallowColor;
void main() {
	float t = smoothstep(-6.0, 6.0, vHeight);
	gl_FragColor = vec4(mix(baseColor, shallowColor, t), 1.0);
}
