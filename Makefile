build-fhe:
	(cd SEAL-Python && docker build -t custom-simple-fhe:latest -f Dockerfile .)