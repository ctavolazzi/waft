import { Color, InstancedMesh, Matrix4, MeshStandardMaterial, PlaneGeometry, SphereGeometry, Vector3 } from 'three';
import type { LatticeBeing, TerrainSettings } from './types';

const tempMatrix = new Matrix4();
const tempPosition = new Vector3();
const tempScale = new Vector3();

function latticeToWorld(value: number, max: number, span: number): number {
	if (max <= 1) return 0;
	const t = value / (max - 1);
	return (t - 0.5) * span;
}

/** Shared seabed heightfield; safe to use under both WebGL and WebGPU stacks. */
export function buildTerrainPlaneGeometry(size: number, segments: number): PlaneGeometry {
	const geometry = new PlaneGeometry(size, size, segments, segments);
	geometry.rotateX(-Math.PI / 2);
	const pos = geometry.attributes.position;
	for (let i = 0; i < pos.count; i++) {
		const x = pos.getX(i);
		const z = pos.getZ(i);
		const height =
			Math.sin(x * 0.011) * 2.8 +
			Math.cos(z * 0.009) * 2.4 +
			Math.sin((x + z) * 0.005) * 4.4 -
			24;
		pos.setY(i, height);
	}
	geometry.computeVertexNormals();
	return geometry;
}

export function createPopulationMesh(settings: TerrainSettings): InstancedMesh {
	const geometry = new SphereGeometry(0.6, 8, 8);
	const material = new MeshStandardMaterial({
		color: new Color('#88ccee'),
		emissive: new Color('#44aadd'),
		emissiveIntensity: 0.8,
		metalness: 0.1,
		roughness: 0.4,
		transparent: true,
		opacity: 0.85,
		fog: true
	});
	const mesh = new InstancedMesh(geometry, material, settings.maxPopulation);
	mesh.instanceMatrix.setUsage(35048); // DynamicDrawUsage
	mesh.count = 0;
	return mesh;
}

export function updatePopulationMesh(
	mesh: InstancedMesh,
	beings: LatticeBeing[],
	settings: TerrainSettings
): void {
	const alive = beings.filter((b) => b.alive).slice(0, settings.maxPopulation);
	const width = Math.max(1, Math.ceil(Math.sqrt(alive.length || 1)));
	const depth = width;
	let i = 0;
	for (const being of alive) {
		const worldX = latticeToWorld(being.x, width, settings.size * 0.95);
		const worldZ = latticeToWorld(being.y, depth, settings.size * 0.95);
		const bob = Math.sin((being.fitness + i) * Math.PI * 2) * 0.5;
		tempPosition.set(worldX, -8 + bob, worldZ);
		tempScale.setScalar(0.5 + being.fitness * 0.8);
		tempMatrix.compose(tempPosition, mesh.quaternion, tempScale);
		mesh.setMatrixAt(i, tempMatrix);
		i += 1;
	}
	mesh.count = i;
	mesh.instanceMatrix.needsUpdate = true;
}
