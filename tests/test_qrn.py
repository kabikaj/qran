import pytest
from qrn import get_text, Index

class TestMushaf:
    """Test suite for module1 functionality."""

    def test_general(self):
        """Test basic functionality."""
        
        result = get_text(
            ini_index=Index(sura=1, verse=1, word=1, block=1),
            end_index=Index(sura=1, verse=1, word=1, block=1),
        )

        res = list(result)
        assert len(res) == 1

        graph_ar, graph_lt, arch_ar, arch_lt, ind = res[0]

        assert graph_ar == "بِسْمِ"
        assert graph_lt == "B₁ᵢSᵒMᵢ"
        assert arch_ar == "ٮسم"
        assert arch_lt == "BSM"
        assert ind == "1:1:1"


class TestMushafBlocks:
    """Test suite for module1 functionality."""

    def test_1111_1111(self):
        """Test index combination"""
        
        result = get_text(
            ini_index=Index(sura=1, verse=1, word=1, block=1),
            end_index=Index(sura=1, verse=1, word=1, block=1),
            args={"blocks": True}
        )

        res = list(result)
        assert res[0][-1] == "1:1:1:1"


    def test_1111_111_(self):
        """Test index combination"""
        
        result = get_text(
            ini_index=Index(sura=1, verse=1, word=1, block=1),
            end_index=Index(sura=1, verse=1, word=1, block=-1),
            args={"blocks": True}
        )

        res = list(result)
        assert res[0][-1] == "1:1:1:1"


    def test_112__112_(self):
        """Test index combination"""
        
        result = get_text(
            ini_index=Index(sura=1, verse=1, word=2, block=0),
            end_index=Index(sura=1, verse=1, word=2, block=-1),
            args={"blocks": True}
        )
        res = list(result)
        assert len(res) == 2
        assert res[0][-1] == "1:1:2:1"
        assert res[1][-1] == "1:1:2:2"


    def test_1622_171_(self):
        """Test index combination"""
        
        result = get_text(
            ini_index=Index(sura=1, verse=6, word=2, block=2),
            end_index=Index(sura=1, verse=7, word=1, block=-1),
            args={"blocks": True}
        )
        res = list(result)
        assert len(res) == 8
        assert res[0][-1] == "1:6:2:2"
        assert res[-1][-1] == "1:7:1:3"
        assert " ".join(r[-2] for r in res) == "LCR A T A LMSBFBM CR A T"


    # @pytest.mark.parametrize("a,b,expected", [
    #     (1, 1, 2),
    #     (0, 0, 0),
    #     (-1, 1, 0),
    # ])
    # def test_some_function_with_parameters(self, a, b, expected):
    #     """Test with multiple input combinations."""
    #     assert some_function(a, b) == expected

    # def test_some_function_error_case(self):
    #     """Test that errors are raised appropriately."""
    #     with pytest.raises(ValueError):
    #         some_function(None, None)

    # @pytest.mark.skip(reason="Not implemented yet")
    # def test_unimplemented_feature(self):
    #     """Mark tests that are not yet implemented."""
    #     assert False