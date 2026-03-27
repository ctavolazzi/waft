varying float vHeight;
varying vec2 vUv;
void main() {
	vUv = uv;
	vHeight = position.y;
	gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
