import {
	Camera,
	HalfFloatType,
	Mesh,
	OrthographicCamera,
	PlaneGeometry,
	RGBAFormat,
	Scene,
	ShaderMaterial,
	Uniform,
	Vector2,
	Vector3,
	Timer,
	WebGLRenderer,
	WebGLRenderTarget
} from 'three';
import type { CausticsSettings } from './types';

/**
 * WAFT `/biome` primary optics path (Phase 4): **env-depth + bounded screen-space march**
 * implemented in this module (Renou-style grounding plane), not Evan Wallace’s
 * derivative caustics mesh. For MLS-MPM + SSFR see `/biome/fluid-research`.
 */

const envVertex = /* glsl */ `
varying vec3 vWorldPos;
void main() {
	vec4 world = modelMatrix * vec4(position, 1.0);
	vWorldPos = world.xyz;
	gl_Position = projectionMatrix * viewMatrix * world;
}
`;

const envFragment = /* glsl */ `
varying vec3 vWorldPos;
void main() {
	float depth = gl_FragCoord.z;
	gl_FragColor = vec4(vWorldPos, depth);
}
`;

const passVertex = /* glsl */ `
varying vec2 vUv;
void main() {
	vUv = uv;
	gl_Position = vec4(position.xy, 0.0, 1.0);
}
`;

const causticsFragment = /* glsl */ `
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
`;

export class CausticsPipeline {
	private envTarget: WebGLRenderTarget;
	private causticsTarget: WebGLRenderTarget;
	private envMaterial: ShaderMaterial;
	private causticsMaterial: ShaderMaterial;
	private passScene: Scene;
	private passCamera: OrthographicCamera;
	private passMesh: Mesh;
	private lightCamera: OrthographicCamera;
	private timer = new Timer();

	constructor(settings: CausticsSettings) {
		const size = settings.resolution;
		this.envTarget = new WebGLRenderTarget(size, size, {
			type: HalfFloatType,
			format: RGBAFormat
		});
		this.causticsTarget = new WebGLRenderTarget(size, size, {
			type: HalfFloatType,
			format: RGBAFormat
		});

		this.envMaterial = new ShaderMaterial({
			vertexShader: envVertex,
			fragmentShader: envFragment
		});

		this.causticsMaterial = new ShaderMaterial({
			vertexShader: passVertex,
			fragmentShader: causticsFragment,
			uniforms: {
				envMapTex: new Uniform(this.envTarget.texture),
				waterNormalTex: new Uniform(null),
				sunDirection: new Uniform(new Vector3(0.707, 0.707, 0)),
				eta: new Uniform(settings.eta),
				maxSteps: new Uniform(settings.maxSteps),
				intensity: new Uniform(settings.intensity),
				texel: new Uniform(new Vector2(1 / size, 1 / size)),
				time: new Uniform(0)
			}
		});

		this.passScene = new Scene();
		this.passCamera = new OrthographicCamera(-1, 1, 1, -1, 0, 1);
		this.passMesh = new Mesh(new PlaneGeometry(2, 2), this.causticsMaterial);
		this.passScene.add(this.passMesh);

		this.lightCamera = new OrthographicCamera(-260, 260, 260, -260, 0.1, 1000);
		this.lightCamera.position.set(0, 260, 0);
		this.lightCamera.lookAt(0, 0, 0);
	}

	get texture() {
		return this.causticsTarget.texture;
	}

	updateSettings(settings: CausticsSettings): void {
		if (this.envTarget.width !== settings.resolution) {
			this.envTarget.setSize(settings.resolution, settings.resolution);
			this.causticsTarget.setSize(settings.resolution, settings.resolution);
			this.causticsMaterial.uniforms.texel.value.set(1 / settings.resolution, 1 / settings.resolution);
		}
		this.causticsMaterial.uniforms.maxSteps.value = settings.maxSteps;
		this.causticsMaterial.uniforms.intensity.value = settings.intensity;
		this.causticsMaterial.uniforms.eta.value = settings.eta;
	}

	update(
		renderer: WebGLRenderer,
		scene: Scene,
		underwater: Mesh[],
		waterNormalMap: WebGLRenderTarget['texture'] | null,
		sunDirection: Vector3
	): void {
		if (!waterNormalMap || underwater.length === 0) return;

		this.timer.update();
		this.causticsMaterial.uniforms.time.value = this.timer.getElapsed();
		this.causticsMaterial.uniforms.waterNormalTex.value = waterNormalMap;
		this.causticsMaterial.uniforms.sunDirection.value.copy(sunDirection).normalize();
		this.lightCamera.position.copy(sunDirection.clone().normalize().multiplyScalar(-280));
		this.lightCamera.lookAt(0, -20, 0);

		const visibility = new Map<Mesh, boolean>();
		for (const obj of underwater) {
			visibility.set(obj, obj.visible);
			obj.visible = true;
		}

		const previous = scene.overrideMaterial;
		scene.overrideMaterial = this.envMaterial;
		renderer.setRenderTarget(this.envTarget);
		renderer.clear();
		renderer.render(scene, this.lightCamera as Camera);
		scene.overrideMaterial = previous;

		renderer.setRenderTarget(this.causticsTarget);
		renderer.clear();
		renderer.render(this.passScene, this.passCamera);
		renderer.setRenderTarget(null);

		for (const [obj, isVisible] of Array.from(visibility.entries())) {
			obj.visible = isVisible;
		}
	}

	dispose(): void {
		this.envTarget.dispose();
		this.causticsTarget.dispose();
		this.envMaterial.dispose();
		this.causticsMaterial.dispose();
		(this.passMesh.geometry as PlaneGeometry).dispose();
	}
}

export function applyCausticsToMaterial(
	material: ShaderMaterial,
	texture: WebGLRenderTarget['texture'] | null,
	intensity: number
): void {
	if (!texture) {
		delete material.userData.caustics;
		material.onBeforeCompile = () => {};
		material.needsUpdate = true;
		return;
	}
	if (!material.userData.caustics) {
		material.userData.caustics = {
			texture,
			intensity
		};
	} else {
		material.userData.caustics.texture = texture;
		material.userData.caustics.intensity = intensity;
	}
	material.onBeforeCompile = (shader) => {
		shader.uniforms.causticsMap = new Uniform(material.userData.caustics.texture);
		shader.uniforms.causticsIntensity = new Uniform(material.userData.caustics.intensity);
		shader.fragmentShader = shader.fragmentShader
			.replace(
				'#include <common>',
				`#include <common>
uniform sampler2D causticsMap;
uniform float causticsIntensity;`
			)
			.replace(
				'#include <dithering_fragment>',
				`float caustic = texture2D(causticsMap, vUv).r * causticsIntensity;
gl_FragColor.rgb += vec3(caustic);
#include <dithering_fragment>`
			);
	};
	material.needsUpdate = true;
}
