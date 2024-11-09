from concrete import fhe

@fhe.compiler({"x": "encrypted"})
def f(x):
    return x + 42

inputset = range(10)
circuit = f.compile(inputset)

assert circuit.encrypt_run_decrypt(10) == f(10)
print(f"Result: {circuit.encrypt_run_decrypt(10)}")
print(f"Result Assertion: {circuit.encrypt_run_decrypt(10) == f(10)}")