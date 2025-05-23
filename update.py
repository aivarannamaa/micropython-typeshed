import shutil
import os.path
import sys
import subprocess

if os.path.exists("src"):
    shutil.rmtree("src")
os.makedirs("src")

# I'm keeping the copy of input stubs, to be able to monitor the changes also in the parts not included in src

input_mp_stubs_path = f"input_micropython_stubs"
if os.path.exists(input_mp_stubs_path):
    shutil.rmtree(input_mp_stubs_path)

subprocess.run([sys.executable, "-m", "pip", "install",
                "--target", input_mp_stubs_path,
                "--no-user",
                "micropython-rp2-rpi_pico2_w-stubs==1.25.0.post1",
                "micropython-esp32-stubs==1.25.0.post2",
                "micropython-stm32-pybv11-stubs==1.25.0.post1",
                "micropython-samd-stubs==1.25.0.post1"])


# Copy MicroPython's stdlib
for name in ["stdlib", "stubs"]:
    full_path = os.path.join(input_mp_stubs_path, name)
    shutil.copytree(full_path, os.path.join("src", name))

# Copy MicroPython's helpers under stdlib (don't know why they are outside stlib in the input)
shutil.copytree(os.path.join("input_micropython_stubs", "_mpy_shed"), "src/stdlib/_mpy_shed")

# Copy MicroPython's stubs under stdlib
for name in os.listdir(input_mp_stubs_path):
    full_path = os.path.join(input_mp_stubs_path, name)
    if name.endswith(".pyi"):
        shutil.copy(full_path, f"src/stdlib/{name}")
    elif os.path.exists(os.path.join(input_mp_stubs_path, name, "__init__.pyi")):
        dest = os.path.join("src", "stdlib", name)
        shutil.copytree(os.path.join(input_mp_stubs_path, name), f"src/stdlib/{name}",
                        dirs_exist_ok=True)

# delete plain pyi-files, which have corresponding package
for name in os.listdir("src/stdlib"):
    if name.endswith(".pyi") and os.path.exists(os.path.join("src", "stdlib", name.removesuffix(".pyi"), "__init__.pyi")):
        print("Removing plain", name)
        os.remove(os.path.join("src", "stdlib", name))



# merge MicroPython's __builtins__.pyi with builtins.pyi
with open("src/stdlib/builtins.pyi", "a", encoding="utf-8") as f1:
    with open(os.path.join(input_mp_stubs_path, "__builtins__.pyi"), "r", encoding="utf-8") as f2:
        f1.write("\n\n")
        f1.write(f2.read())

