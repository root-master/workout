from setuptools import setup, find_packages

from workout.__init__ import __version__

package_dir = {"workout": "workout"},
packages = {"workout": "workout",
            "workout.ml": "workout/ml",
            "workout.api": "workout/api"}
setup(
    name="workout",
    version=__version__,
    author="JACOB RAFATI",
    author_email="yrafati@gmail.com",
    url="https://github.com/root-master/workout",
    description="AI-based Workout App",
    python_requires=">=3.7",
    packages=packages,
    include_package_data=True)
