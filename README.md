# qran

Quran structured text API.

Python package to extract Quranic text in graphemic and archigraphemic representations, different Quranic encodings and Latin transliteration. The package works as a an API for the stuctured Quran.

This package can be very helpful for semiautomating the transcription of old Quranic manuscripts or fast lookups of script and typographic analysis.

## Installation

```bash
pip install qran
```

## Usage

As a python library

```python
from qran import get_text, Index

>>> text = get_text(
...     ini_index=Index(sura=1, verse=1, word=4, block=2),
...     end_index=Index(sura=1, verse=2, word=2, block=-1),
...     args={"blocks": True},
... )
... 
>>> for grapheme_ar, grapheme, lt, archigrapheme_ar, arhigrapheme_lt in text:
...     print(grapheme_ar, grapheme, lt, archigrapheme_ar, arhigrapheme_lt)
...     
لرَّ LRᵚᵃ لر LR 1:1:4:2
حِيمِ GᵢB₂Mᵢ حٮم GBM 1:1:4:3
ا A ا A 1:2:1:1
لْحَمْدُ LᵒGᵃMᵒDᵘ لحمد LGMD 1:2:1:2
لِلَّهِ LᵢLᵚᵃHᵢ لله LLH 1:2:2:1
```

Alternatively, you can use a tuple of integers instead of an Index object:

```python
>>> text = get_text(
...     ini_index=(1, 1, 4, 2),
...     end_index=(1, 2, 2, -1),
...     args={"blocks": True},
... )
```

As a unix-like command:

```bash
$ qran 1:1:4:2-1:2:2 --blocks
لرَّ	LRᵚᵃ	لر	LR	1:1:4:2
حِيمِ	GᵢB₂Mᵢ	حٮم	GBM	1:1:4:3
ا	A	ا	A	1:2:1:1
لْحَمْدُ	LᵒGᵃMᵒDᵘ	لحمد	LGMD	1:2:1:2
لِلَّهِ	LᵢLᵚᵃHᵢ	لله	LLH	1:2:2:1
```

## License

This project is licensed under the [MIT License](./LICENSE) for its source code.

It includes Quran text from the [Tanzil Project](http://tanzil.net/), 
which is licensed under the [Creative Commons Attribution 3.0 License](https://creativecommons.org/licenses/by/3.0/).

© 2007–2021 Tanzil Project. The text is unmodified and used under Tanzil's terms of use: http://tanzil.net/docs/license

## Author

Alicia González Martínez
