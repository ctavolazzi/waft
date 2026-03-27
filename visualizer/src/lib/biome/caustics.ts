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
import {
	causticsEnvVert as envVertex,
	causticsEnvFrag as envFragment,
	causticsPassVert as passVertex,
	causticsMarchFrag as causticsFragment
} from './shaders';

/**
 * WAFT `/biome` primary optics path (Phase 4): **env-depth + bounded screen-space march**
 * implemented in this module (Renou-style grounding plane), not Evan Wallace's
 * derivative caustics mesh. For MLS-MPM + SSFR see `/biome/fluid-research`.
 */

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
	private _scratchVec3 = new Vector3();
	private _savedVisibility: boolean[] = [];

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
		this._scratchVec3.copy(sunDirection).normalize().multiplyScalar(-280);
		this.lightCamera.position.copy(this._scratchVec3);
		this.lightCamera.lookAt(0, -20, 0);

		this._savedVisibility.length = underwater.length;
		for (let i = 0; i < underwater.length; i++) {
			this._savedVisibility[i] = underwater[i].visible;
			underwater[i].visible = true;
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

		for (let i = 0; i < underwater.length; i++) {
			underwater[i].visible = this._savedVisibility[i];
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
