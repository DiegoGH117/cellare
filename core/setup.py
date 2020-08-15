from setuptools import setup

with open('README.md', 'r') as f:
      long_description = f.read() 
setup(
      name = 'CellARE',
      version = '0.0.2',
      description = 'A cellular automaton based implementation to run SIR simulations',
      py_modules = ['cellare'],
      package_dir = {'':'src'},
      classifiers = [
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent'
      ],
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      install_requires=[
            "numpy",
            "matplotlib"
      ],
      url = 'https://github.com/DiegoGH117/cellare',
      project_urls = {
            'Documentation': 'https://cellare.readthedocs.io/en/latest/',
      },
)