varying float vHeight;
varying vec2 vUv;
uniform vec3 baseColor;
uniform vec3 shallowColor;
uniform sampler2D seabedMap;
uniform float useSeabedMap;
void main() {
	float t = smoothstep(-32.0, -15.0, vHeight);
	vec3 proc = mix(baseColor, shallowColor, t);
	proc += vec3(0.04 * sin(vUv.x * 40.0), 0.03 * cos(vUv.y * 32.0), 0.05);
	vec3 color = proc;
	if (useSeabedMap > 0.5) {
		vec3 sampled = texture2D(seabedMap, vUv * 6.0).rgb;
		color = mix(proc, sampled, 0.88);
	}
	gl_FragColor = vec4(color, 1.0);
}
