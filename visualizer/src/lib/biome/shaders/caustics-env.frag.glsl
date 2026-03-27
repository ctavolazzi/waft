varying vec3 vWorldPos;
void main() {
	float depth = gl_FragCoord.z;
	gl_FragColor = vec4(vWorldPos, depth);
}
