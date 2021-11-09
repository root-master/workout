from setuptools import setup, find_packages

from features.__init__ import __version__

package_dir = {"workout": "workout"},
setup(
    name="workout",
    version=__version__,
    author="JACOB RAFATI",
    author_email="yrafati@gmail.com",
    url="https://github.com/root-master/workout",
    description="AI-driven Personal Training Workout App",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True)
