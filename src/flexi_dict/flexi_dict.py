from typing import Dict, List, Optional
import dill

from .config import MAX_CORRECTION_RATE

from .utils import validate_symbol_weights
from .search_engine import SearchEngine
from .flexi_trie import FlexiTrie


class FlexiDict:

    _trie: FlexiTrie
    _search_engine: SearchEngine
    _symbol_weights: Optional[Dict[str, float]] = None

    def __init__(
        self,
        search_engine: SearchEngine,
        symbol_weights: Optional[Dict[str, float]] = None,
    ):

        self._trie = FlexiTrie()

        validate_symbol_weights(symbol_weights)
        self._symbol_weights = symbol_weights

        self._search_engine = search_engine

    def __setitem__(self, keyname: str, value_id: int):
        """
        Adds a value to the prefix tree under the specified key.

        Args:
            keyname (str): The key under which to store the value.
            value_id (int): The identifier of the value.

        """
        self._trie.add(keyname, value_id, self._symbol_weights)

    def __getitem__(self, query: str) -> Optional[int]:
        """
        Retrieves the first value associated with the specified key.

        Args:
            query (str): The key for which to retrieve the value.

        Returns:
            int: The first value associated with the specified key.

        Raises:
            TypeError: If `query` is not a string.
            KeyError: If the `query` key is not found in the dictionary.
        """
        exact_match_values = self._trie.find(query)
        if exact_match_values:
            return next(iter(exact_match_values))

        fuzzy_match_values = self.get(query)
        if fuzzy_match_values:
            return fuzzy_match_values[0]

        return None

    def get(self, query: str, max_correction_rate: Optional[float] = None) -> List[int]:

        if max_correction_rate is None:
            max_correction_rate = MAX_CORRECTION_RATE

        fuzzy_match_items = self._search_engine.search(
            trie=self.trie,
            query=query,
            max_correction_rate=max_correction_rate)
        return [item.value for item in fuzzy_match_items]

    def search(self, query: str, max_correction_rate: Optional[float] = None) -> List[int]:

        if max_correction_rate is None:
            max_correction_rate = MAX_CORRECTION_RATE

        fuzzy_match_items = self._search_engine.search(
            trie=self.trie,
            query=query,
            max_correction_rate=max_correction_rate,
            max_correction_rate_for_leaves=1.)
        return [item.value for item in fuzzy_match_items]

    @property
    def trie(self):
        return self._trie

    def save_trie(self, filename: str):
        with open(filename, "wb") as f:
            dill.dump(file=f, obj=self.trie, recurse=True)

    def load_trie(self, filename: str) -> None:
        with open(filename, "rb") as f:
            trie = dill.load(file=f)
            self._trie = trie
