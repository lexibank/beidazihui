import attr
import lingpy
from pathlib import Path
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar, getEvoBibAsBibtex

from lingpy.sequence.sound_classes import syllabify
from pylexibank.models import Concept, Language, Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb, getEvoBibAsBibtex

@attr.s
class CustomConcept(Concept):
    Chinese = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default="Sinitic")
    Family = attr.ib(default="Sino-Tibetan")
    DialectGroup = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Partial_Cognacy = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "beidazihui"
    lexeme_class = CustomLexeme
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(
          missing_data=[""],
          separators=";/,",
          brackets={"(": ")", "[": "]"},
          strip_inside_brackets=True,
          first_form_only=True
      )
    def cmd_download(self, **kw):
        self.raw_dir.write("sources.bib", getEvoBibAsBibtex("Zihui", **kw))

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
