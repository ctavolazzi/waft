// Shader barrel — keeps GLSL in separate files for syntax highlighting
// while providing TS-compatible exports.

export const terrainVert = `\
varying float vHeight;
varying vec2 vUv;
void main() {
	vUv = uv;
	vHeight = position.y;
	gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;

export const terrainFrag = `\
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
}`;

export const dioramaVert = `\
varying float vHeight;
void main() {
	vHeight = position.y;
	gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;

export const dioramaBaseFrag = `\
varying float vHeight;
uniform vec3 baseColor;
uniform vec3 shallowColor;
void main() {
	float t = smoothstep(-10.0, 10.0, vHeight);
	vec3 color = mix(baseColor, shallowColor, t);
	gl_FragColor = vec4(color, 1.0);
}`;

export const dioramaFrameFrag = `\
varying float vHeight;
uniform vec3 baseColor;
uniform vec3 shallowColor;
void main() {
	float t = smoothstep(-6.0, 6.0, vHeight);
	gl_FragColor = vec4(mix(baseColor, shallowColor, t), 1.0);
}`;

export const causticsEnvVert = `\
varying vec3 vWorldPos;
void main() {
	vec4 world = modelMatrix * vec4(position, 1.0);
	vWorldPos = world.xyz;
	gl_Position = projectionMatrix * viewMatrix * world;
}`;

export const causticsEnvFrag = `\
varying vec3 vWorldPos;
void main() {
	float depth = gl_FragCoord.z;
	gl_FragColor = vec4(vWorldPos, depth);
}`;

export const causticsPassVert = `\
varying vec2 vUv;
void main() {
	vUv = uv;
	gl_Position = vec4(position.xy, 0.0, 1.0);
}`;

export const causticsMarchFrag = `\
precision highp float;
varying vec2 vUv;
uniform sampler2D envMapTex;
uniform sampler2D waterNormalTex;
uniform vec3 sunDirection;
uniform float eta;
uniform float maxSteps;
uniform float intensity;
uniform vec2 texel;
uniform float time;

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

void main() {
	vec3 n = normalize(texture2D(waterNormalTex, vUv + vec2(time * 0.01, time * 0.015)).xyz * 2.0 - 1.0);
	vec3 refracted = normalize(refract(-normalize(sunDirection), n, 1.0 / eta));
	vec2 rayUv = vUv;
	float prevDepth = 0.0;
	float found = 0.0;
	float converged = 0.0;
	for (float i = 0.0; i < 256.0; i++) {
		if (i > maxSteps) break;
		rayUv += refracted.xy * texel;
		if (rayUv.x < 0.0 || rayUv.y < 0.0 || rayUv.x > 1.0 || rayUv.y > 1.0) break;
		vec4 env = texture2D(envMapTex, rayUv);
		float envDepth = env.a;
		float rayDepth = prevDepth + max(refracted.z * 0.01, 0.0005);
		if (rayDepth >= envDepth) {
			found = 1.0;
			converged = 1.0 - clamp(length(rayUv - vUv) * 2.0, 0.0, 1.0);
			break;
		}
		prevDepth = rayDepth;
	}
	float noise = hash(vUv * 712.0 + time * 0.2) * 0.12;
	float c = (converged + noise) * intensity * found;
	gl_FragColor = vec4(vec3(c), 1.0);
}`;

export const rainOverlayVert = `\
void main() {
	gl_Position = vec4(position.xy, 0.0, 1.0);
}`;

export const rainOverlayFrag = `\
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
}`;
