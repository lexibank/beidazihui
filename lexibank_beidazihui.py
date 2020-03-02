import attr
import lingpy
from pathlib import Path
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar, getEvoBibAsBibtex

from lingpy.sequence.sound_classes import syllabify

@attr.s
class CustomConcept(Concept):
    Chinese = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default='Sinitic')
    Family = attr.ib(default='Sino-Tibetan')
    DialectGroup = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "beidazihui"
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(
          missing_data=[''],
          separators=";/,",
          brackets={'(': ')', '[': ']'},
          strip_inside_brackets=True,
          first_form_only=True
      )
    # delet or update???
    def cmd_download(self, **kw):
        self.raw_dir.write("sources.bib", getEvoBibAsBibtex("Zihui", **kw))

    def cmd_makecldf(self, args):
        # add sources
        args.writer.add_sources()
        # read in data
        ds = self.raw_dir / 'wordlist.tsv'
        wl = lingpy.Wordlist(ds.as_posix())
        # add concepts
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            args.writer.add_concept(
                ID='_'.join([concept.number, slug(concept.gloss)]),
                Name=concept.gloss,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
                Chinese=concept.attributes["chinese"]
            )
            concepts[concept.attributes["chinese"]] = '_'.join([concept.number, slug(concept.gloss)])
        # add languages
        languages = args.writer.add_languages(lookup_factory="Name")
        # add forms
        for idx in progressbar(wl, desc = 'cldfify the data'):
            cogid = idx
            if wl[idx, 'concept'] in concepts.keys():
                args.writer.add_form_with_segments(
                    Language_ID=languages[wl[idx, 'doculect']],
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'value'],
                    Form=wl[idx, 'form'],
                    Segments=wl[idx, 'tokens']
                )
