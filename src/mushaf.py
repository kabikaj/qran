#!/usr/bin/env python3
#
#    mushaf.py
#
# retrieve Quranic text
#
# Alicia González Martínez
#
#  __  __           _            __ 
# |  \/  |_   _ ___| |__   __ _ / _|
# | |\/| | | | / __| '_ \ / _` | |_ 
# | |  | | |_| \__ \ | | | (_| |  _|
# |_|  |_|\__,_|___/_| |_|\__,_|_|  
#                                   
#
################################################

import sys
import textwrap
import orjson as json
from pydantic import BaseModel
from typing import Generator
from itertools import groupby
from argparse import ArgumentParser, ArgumentTypeError, FileType, RawTextHelpFormatter


class Index(BaseModel):
    """ Quranic index.
    """
    sura: int
    verse: int
    word: int
    block: int | None


class IndexRange(BaseModel):
    """ Quranic index range.
    """
    ini: Index
    end: Index


class Block(BaseModel):
    """ Quranic block with corresponding index.
    """
    grapheme_ar: str
    grapheme_lt: str
    archigrapheme_ar: str
    archigrapheme_lt: str 
    index: Index


def _parse_index(index: str, default: int) -> Index:
    """ convert string containing an index into an Index object.

    Args:
        index: index to parse.
        default: default value if not included in index.

    Return:
        splited index.

    Raise:
        ValueError: if index is ill-formed.

    """
    try:
        indexes = iter(index.split(":"))
        sura, verse, word, block = (next(indexes, None) for _ in range(4))
        return Index(
            sura=int(sura)-1 if sura else default,
            verse=int(verse)-1 if verse else default,
            word=int(word)-1 if word else default,
            block=int(block)-1 if block else default
        )
    except ValueError:
        raise


def parse_quran_range(arg: str) -> IndexRange:
    """ Parse index range contained in arg. Complete format:

        "sura,verse,word,block-sura,verse,word,block"

        All individual indexes are optional

    Args:
        arg: string containing the quranic index range or single index.

    Return:
        range of indexes.

    Raise:
        ArgumentTypeError: if arg does not follow the expected format.

    """
    ini, _, end = arg.partition("-")

    try:
        return IndexRange(
            ini=_parse_index(index=ini if ini else "", default=0),
            end=_parse_index(index=end if end else "", default=-1)
        )

    except ValueError:
        raise ArgumentTypeError(
            "argument format must be sura:verse:word:block-sura:verse:word:block, eg. 2:3-2:10:2"
        )


def _extract_seq(data: dict, ind: Index) -> Generator[Block, None, None]:
    """ Extracts the sequece of Quranic blocks indicated in index range ind.

    Args:
        data: Quran data
        ind: index range.

    Yield:
        Quranic block together with its index.

    """
    ini_sura = ind.ini.sura
    ini_verse = ind.ini.verse
    ini_word = ind.ini.word
    ini_block = ind.ini.block

    end_sura = ind.end.sura
    end_verse = ind.end.verse
    end_word = ind.end.word
    end_block = ind.end.block

    for isura in range(ini_sura, end_sura+1):
        for iverse in range(len(data["indexes"][isura])):
            if isura == ini_sura and iverse < ini_verse:
                continue
            if isura == end_sura and iverse > end_verse:
                return
            for iword in range(len(data["indexes"][isura][iverse])):
                if isura == ini_sura and iverse == ini_verse and iword < ini_word:
                    continue
                if isura == end_sura and iverse == ini_verse and iword > end_word:
                    return
                for iblock in range(len(data["indexes"][isura][iverse][iword])):
                    if isura == ini_sura and iverse == ini_verse and \
                        iword == ini_word and iblock < ini_block:
                        continue
                    if isura == end_sura and iverse == end_verse and \
                        iword == end_word and iblock > end_block:
                        return

                    block_index = data["indexes"][isura][iverse][iword][iblock]

                    graph_ar, graph_lt, arch_ar, arch_lt = data["blocks"][block_index]
                    
                    yield Block(
                        grapheme_ar=graph_ar,
                        grapheme_lt=graph_lt,
                        archigrapheme_ar=arch_ar, 
                        archigrapheme_lt=arch_lt,
                        index=Index(
                            sura=isura+1,
                            verse=iverse+1,
                            word=iword+1,
                            block=iblock+1
                        )
                    )


if __name__ == "__main__":

    parser = ArgumentParser(
        description="Retrieve Quranic text",
        formatter_class=RawTextHelpFormatter,
        epilog="Ya Kabikaj, protect this code from bugs!"
    )
    parser.add_argument(
        "index",
        type=parse_quran_range,
        nargs="?",
        default=((None, None, None, None), (None, None, None, None)),
        help=textwrap.dedent(""" \
            Quranic index range to retrieve [DEFAULT WHOLE TEXT]. 
             A complete range must have the following format:
                ini_sura:ini_verse:ini_word:ini_block-end_sura:end_verse:end_word:end_block
             Both beginning and end indexes are inclusive. All indexes are optional.
        """))
    parser.add_argument(
        "--blocks",
        action="store_true",
        help="retrieve text as letterblocks instead of words"
    )
    parser.add_argument(
        "--source", "-s",
        choices=["tanzil-simple", "tanzil-uthmani", "decotype"],
        default="tanzil-simple",
        help="text encoding"
    )
    script = parser.add_mutually_exclusive_group()
    script.add_argument(
        "--no_lat",
        action="store_true",
        help="omit Latin traslineration in output"
    )
    script.add_argument(
        "--no_ara",
        action="store_true",
        help="omit Arabic script in output"
    )
    layer = parser.add_mutually_exclusive_group()
    layer.add_argument(
        "--no_arch",
        action="store_true",
        help="omit archigraphemic representations in output"
    )
    layer.add_argument(
        "--no_graph",
        action="store_true",
        help="omit graphemic representations in output"
    )
    parser.add_argument(
        "--sep",
        default="\t",
        help="field separator for text output [DEFAULT \\t]"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print output in json instead of plain text"
    )
    parser.add_argument(
        "--out",
        type=FileType("w"),
        help="write output in file instead of stdin"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1",  #FIXME avoid literal for version
        help="prints the program version number and exits successfully"
    )
    args = parser.parse_args()

    with open("../data/sample.json", "rb") as fp:
        data = json.loads(fp.read())

    ind = args.index
    
    # correct final indexes
    end = ind.end

    if end.sura == -1:
        end.sura = len(data["indexes"])
    if ind.end.verse == -1:
        end.verse = len(data["indexes"][end.sura])
    if ind.end.word == -1:
        end.word = len(data["indexes"][end.sura][end.verse])
    if ind.end.block == -1:
        end.block = len(data["indexes"][end.sura][end.verse][end.block])

    sequence = _extract_seq(data, ind)

    if not args.blocks:
        
        _seq = ((k, list(g)) for k, g in groupby(
            sequence,
            key=lambda b: (b.index.sura, b.index.verse, b.index.word)
        ))
        
        sequence = (
            Block(
                grapheme_ar="".join(b.grapheme_ar for b in blocks_group),
                grapheme_lt="".join(b.grapheme_lt for b in blocks_group),
                archigrapheme_ar="".join(b.archigrapheme_ar for b in blocks_group),
                archigrapheme_lt="".join(b.archigrapheme_lt for b in blocks_group),
                index=Index(
                    sura=ind[0],
                    verse=ind[1],
                    word=ind[2],
                    block=None
                )
        ) for ind, blocks_group in _seq)

    results = []

    for block in sequence:
    
        if args.no_lat:
            if args.no_graph:
                res = block.archigrapheme_ar,
            elif args.no_arch:
                res = block.grapheme_ar,
            else:
                res = block.grapheme_ar, block.archigrapheme_ar
        elif args.no_ara:
            if args.no_graph:
                res = block.archigrapheme_lt,
            elif args.no_arch:
                res = block.grapheme_lt,
            else:
                res = block.grapheme_lt, block.archigrapheme_lt
        else:
            if args.no_graph:
                res = block.archigrapheme_ar, block.archigrapheme_lt
            elif args.no_arch:
                res = block.grapheme_ar, block.grapheme_lt
            else:
                res = block.grapheme_ar, block.grapheme_lt, block.archigrapheme_ar, block.archigrapheme_lt

        ind = f"{block.index.sura}:{block.index.verse}:{block.index.word}"
        if block.index.block:
            ind = f"{ind}:{block.index.block}"

        res = res + (ind,)

        results.append(res)

    out = args.out or sys.stdout

    if args.json:
        data = [{"tok": res[:-1], "ind": res[-1]} for res in results]
        out.write(json.dumps(data).decode("utf-8"))
    
    else:
        for res in results:
            print(args.sep.join(res), file=out)

