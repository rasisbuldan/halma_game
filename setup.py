import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="halma-game",
    package=['halma-game'],
    version="0.3.6",
    license='MIT',
    author="Rasis Syauqi Buldan",
    author_email="rasisbuldan@gmail.com",
    description="Halma game created with python (pygame)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rasisbuldan/halma_game",
    download_url="https://github.com/rasisbuldan/halma_game/archive/v0.3.6.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=[
        'pygame',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[
        ('gui', ['assets/gui/*.png']),
        ('board', ['assets/board/*.png']),
        ('button', ['assets/button/*.png']),
        ('fonts', ['assets/fonts/*.ttf']),
        ('info', ['assets/info/*.png']),
        ('pieces', ['assets/pieces/*.png']),
        ('screenshot', ['assets/screenshot/*.png'])
    ]
)