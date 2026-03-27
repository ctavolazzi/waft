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
}
