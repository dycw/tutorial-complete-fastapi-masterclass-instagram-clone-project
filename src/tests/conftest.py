from os import getenv

from dycw_utilities.hypothesis import setup_hypothesis_profiles
from hypothesis import settings


setup_hypothesis_profiles()
settings.load_profile(getenv("HYPOTHESIS_PROFILE", "default"))
