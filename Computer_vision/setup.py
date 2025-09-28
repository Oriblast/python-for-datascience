from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

ls_cy_file = ["distribution.pyx", "ls_file_in_dir.pyx", "Augmentation.pyx"]
ls_cy_file.append("Transformation.pyx")
extensions = [
    Extension(
        name=file.replace(".pyx", ""),  # nom du module
        sources=[file],
        include_dirs=[numpy.get_include()]
    )
    for file in ls_cy_file
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"}
    )
)
