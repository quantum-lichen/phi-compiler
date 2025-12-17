from setuptools import setup, find_packages

setup(
    name="phi-compiler",
    version="1.1.0",
    description="Geometric compiler: Φ-Code → FC-496 binary",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Bryan Ouellette & Lichen Team",
    author_email="lmc.theory@gmail.com",
    url="https://github.com/quantum-lichen/phi-compiler",
    py_modules=["phi_compiler"],
    entry_points={
        'console_scripts': [
            'phi-c=phi_compiler:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
```

### **Action 3.4: Fichier `LICENSE`**
```
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

[Full AGPL-3.0 text - copie depuis https://www.gnu.org/licenses/agpl-3.0.txt]
```

### **Action 3.5: Fichier `.gitignore`**
```
__pycache__/
*.py[cod]
*.496
*.phi
.DS_Store
*.egg-info/
dist/
build/
