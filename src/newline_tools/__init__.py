from .shuffle import Shuffle
from .dedupe import Dedupe
from .split import Split
from .sample import Sample

__program__ = "newline_tools"
__version__ = "0.1.1"
__url__ = "https://github.com/philiporange/newline_tools"
__description__ = "Tools for working with large datasets"
__author__ = "Philip Orange"
__email__ = "git" + "@" + "philiporange.com"
__license__ = "CC0-1.0"

__all__ = ["Shuffle", "Dedupe", "Split", "Sample"]
