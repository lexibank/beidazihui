import attr
import lingpy
from clldutils.path import Path
from clldutils.text import strip_chars, split_text_with_context
from clldutils.misc import lazyproperty
from lingpy.sequence.sound_classes import syllabify
from pylexibank.dataset import Concept, Language
from pylexibank.dataset import NonSplittingDataset as BaseDataset
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

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "beidazihui"
    concept_class = BDConcept
    language_class = HLanguage

    def cmd_download(self, **kw):
        self.raw.write("sources.bib", getEvoBibAsBibtex("Zihui", **kw))

    def cmd_install(self, **kw):
        wl = lingpy.Wordlist(self.raw.posix("wordlist.tsv"))

        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            concepts = {}
            for concept in self.concepts:
                if concept['ENGLISH']:
                    ds.add_concept(
                            ID=concept['NUMBER'],
                            Name=concept['ENGLISH'],
                            Chinese=concept['CHINESE'],
                            Concepticon_ID=concept['CONCEPTICON_ID'],
                            Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                            )
                    concepts[concept['CHINESE']] = concept['NUMBER']

            langs = {k['Name']: k['ID'] for k in self.languages}
            ds.add_languages()

            for k in pb(wl, desc="wl-to-cldf", total=len(wl)):
                if wl[k, "value"] and wl[k, 'concept'] in concepts:
                    ds.add_form_with_segments(
                        Language_ID=langs[wl[k, "doculect"]],
                        Parameter_ID=concepts[wl[k, 'concept']],
                        Value=wl[k, "value"],
                        Form=wl[k, "form"],
                        Segments=wl[k, 'tokens'],
                        Source="Zihui",
                    )
