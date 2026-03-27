uniform float uTime;
uniform float uDensity;
uniform vec2 uResolution;
float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}
void main() {
	vec2 uv = gl_FragCoord.xy / uResolution.xy;
	float dens = clamp(uDensity, 0.0, 1.0);
	float y = uv.y * mix(110.0, 190.0, dens);
	float wind = uTime * 0.35;
	float streak = 0.0;
	for (float k = 0.0; k < 4.0; k++) {
		vec2 cell = vec2(uv.x * mix(90.0, 160.0, dens) + wind * 0.15 + k * 13.7, y + uTime * mix(28.0, 48.0, dens) + k * 41.0);
		vec2 id = floor(cell);
		vec2 f = fract(cell) - 0.5;
		float h = hash(id);
		float w = mix(0.004, 0.012, dens) * (0.5 + h);
		if (abs(f.x) < w && f.y > -0.35 && f.y < 0.42) {
			float a = (1.0 - smoothstep(0.15, 0.42, abs(f.y))) * dens * (0.28 + 0.72 * h);
			streak += a * 0.45;
		}
	}
	float fog = streak * mix(0.55, 0.95, dens);
	gl_FragColor = vec4(0.75, 0.82, 0.95, clamp(fog, 0.0, 0.55));
}
