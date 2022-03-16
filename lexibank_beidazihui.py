import attr
import lingpy
from clldutils.path import Path
from clldutils.text import strip_chars, split_text_with_context
from clldutils.misc import lazyproperty
from lingpy.sequence.sound_classes import syllabify
from pylexibank.models import Concept, Language, Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb, getEvoBibAsBibtex

@attr.s
class BDConcept(Concept):
    Chinese = attr.ib(default=None)

@attr.s
class HLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default='Sinitic')
    Family = attr.ib(default='Sino-Tibetan')
    DialectGroup = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Partial_Cognacy = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "beidazihui"
    concept_class = BDConcept
    lexeme_class = CustomLexeme
    language_class = HLanguage

    def cmd_download(self, **kw):
        self.raw.write("sources.bib", getEvoBibAsBibtex("Zihui", **kw))

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(self.raw_dir.joinpath("wordlist.tsv").as_posix())
        
        args.writer.add_sources()

        concepts = {}
        for concept in self.concepts:
            if concept['ENGLISH']:
                args.writer.add_concept(
                        ID=concept['NUMBER'],
                        Name=concept['ENGLISH'],
                        Chinese=concept['CHINESE'],
                        Concepticon_ID=concept['CONCEPTICON_ID'],
                        Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                        )
                concepts[concept['CHINESE']] = concept['NUMBER']

        langs = args.writer.add_languages(lookup_factory="Name")
        
        cogidx = 1
        for k in pb(wl, desc="wl-to-cldf", total=len(wl)):
            if wl[k, "value"] and wl[k, 'concept'] in concepts:
                args.writer.add_form_with_segments(
                    Language_ID=langs[wl[k, "doculect"]],
                    Parameter_ID=concepts[wl[k, 'concept']],
                    Value=wl[k, "value"],
                    Form=wl[k, "form"],
                    Segments=wl[k, 'tokens'],
                    Source="Zihui",
                    Partial_Cognacy=str(cogidx)
                )
                cogidx += 1
