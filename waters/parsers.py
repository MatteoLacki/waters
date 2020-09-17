from collections import Counter
from io import StringIO
from functools import lru_cache
import numpy as np
import pandas as pd
import xml.etree.cElementTree as ET


col2format = { 'Mass':'{:.4f}',
               'MassSD':'{:.4f}',
               'IntensitySD':'{:.2f}',
               'AverageCharge':'{:.2f}',
               'RT':'{:.4f}',
               'RTSD':'{:.4e}',
               'FWHM':'{:.4f}',
               'Mobility':'{:.3f}',
               'MobilitySD':'{:.3f}',
               'LiftOffRT':'{:.4f}',
               'InfUpRT':'{:.4f}',
               'InfDownRT':'{:.4f}',
               'TouchDownRT':'{:.4f}' }

# IT might be worthwhile to consider the proper way of parsing xmls.
# https://blog.etianen.com/blog/2013/04/14/python-xml/
class XMLparser(object):
    """General xml parsing capabilities."""
    def __init__(self, data_path, col2format=col2format):
        self.data_path = data_path
        self.tree = ET.parse(data_path)
        self.root = self.tree.getroot()
        self.col2format = col2format

    def __del__(self):
        if hasattr(self, 'root'):
            self.root.clear()

    @lru_cache(maxsize=1)
    def get_tag_counts(self):
        """Count the top level tags.

        Returns:
            Counter: count of each first-level tag.
        """
        return Counter(c.tag for c in self.root)

    @lru_cache(maxsize=1)
    def get_all_tag_counts(self):
        """Count all tags.

        Returns:
            Counter: count of each first-level tag.
        """
        return Counter(n.tag for n in self.tree.iter())

    def iter_filter_elements(self, tag, **conditions):
        """Iterate elements with attirbute set to specific values.

        But only recently have I learned, that there is limited reason to use it, as etree now supports XPath from v. 1.03 up, see http://effbot.org/zone/element-xpath.htm

        Args:
            tag (str): which tag to look at?
            **conditions: attribute name and value (str or set),
        Yields:
            xml.etree.cElementTree.Element: consecutive elements meeting the criteria.
        """
        conditions = {k: set([v]) if isinstance(v,str) else v for k,v in conditions.items()}
        for el in self.root.findall(tag):
            OK = True
            for k,v in conditions.items():
                if not (k in el.attrib and el.attrib[k] in v):
                    OK = False
                    break
            if OK:
                yield el
    
    def element2df(self, xml_element, column_names, sep=' ', skipinitialspace=True, **kwds):
        """Represent the text data as a DataFrame.

        Args:
            xml_element (xml.etree.cElementTree.Element): One of the xml tree nodes.
            columns (list): Names of columns for the reported data frame.

        Returns:
            pd.DataFrame: Data contained in the text field of the xml_element, nicely parsed into a data frame.
        """
        return pd.read_table(StringIO(xml_element.text), 
                             names=column_names,
                             sep=' ',
                             skipinitialspace=True,
                             **kwds).dropna()

    def write(self, path):
        """Write back the xml file."""
        path = str(path)
        self.tree.write(path)



def df2text(df, col2format=col2format, copy=True):
    """Translate df to data compatible with the used xml format."""
    if copy:
        df = df.copy()
    cols = df.columns
    col2format = {c:col2format[c] for c in set(cols) & set(col2format)}
    for col, formatter in col2format.items():
        df.loc[:,col] = df.loc[:,col].apply(lambda x: formatter.format(x))
    cols_simple2str = [c for c in cols if c not in col2format]
    df.loc[:,cols_simple2str] = df[cols_simple2str].astype(np.str)
    df = df.iloc[:,0].astype(str).str.cat(df.iloc[:,1:].astype(str), sep=" ")
    return "\n      "+"\n      ".join(df)



def df2text2(df):
    return "\n      "+"\n      ".join(" ".join(row.astype(str)) for row in df.values)


def df2text3(df):
    x = df.iloc[:,0].astype(str).str.cat(df.iloc[:,1:].astype(str), sep=" ")
    return "\n      "+"\n      ".join(x)



class Pep3Dparser(XMLparser):
    @property
    def LE_columns(self):
        """Get low energy column names."""
        return [f.attrib['NAME'] for f in self.root.findall("FORMAT[@FRAGMENTATION_LEVEL='0']/*")]

    @property
    def LE_element(self):
        """Get low energy xml-tree element."""
        return next(self.root.iter('DATA'))

    @property
    def LE(self):
        """Get low energy ions, or the unfragmented spectra."""
        return self.element2df(self.LE_element, self.LE_columns)

    @LE.setter
    def LE(self, df):
        self.LE_element.text = df2text(df, self.col2format)

    @property
    def HE_columns(self):
        """Get high energy column names."""
        return [f.attrib['NAME'] for f in self.root.findall("FORMAT[@FRAGMENTATION_LEVEL='1']/*")]

    @property
    def HE_element(self):
        """Get high energy xml-tree element."""
        return next(self.root.iter('HE_DATA'))

    @property
    def HE(self):
        """Get high energy ions, or the spectra of fragments."""
        return self.element2df(self.HE_element, self.HE_columns)

    @HE.setter
    def HE(self, df):
        self.HE_element.text = df2text(df, self.col2format)



class Apex3Dparser(XMLparser):
    @property
    def columns(self):
        """Get column names."""
        return [f.attrib['NAME'] for f in self.root.findall('DATAFORMAT/FIELD')]

    @property
    def LE_columns(self):
        """Get low energy column names."""
        return self.columns

    @property
    def HE_columns(self):
        """Get low energy column names."""
        return self.columns

    @property
    def LE_element(self):
        """Get low energy xml-tree element."""
        return next(self.root.iter('LE'))

    @property
    def HE_element(self):
        """Get low energy xml-tree element."""
        return next(self.root.iter('HE'))

    @property
    def LE(self):
        """Get low energy ions, or the unfragmented spectra."""
        return self.element2df(self.LE_element, self.LE_columns)

    @property
    def HE(self):
        """Get high energy ions, or the spectra of fragments."""
        return self.element2df(self.HE_element, self.HE_columns)

    @HE.setter
    def HE(self, df):
        raise NotImplementedError

    @LE.setter
    def LE(self, df):
        raise NotImplementedError

    def to_hdf(self):
        """Save to hdf5 as packed as possible."""
        self.LE.to_hdf(path_or_buf=self.data_path.with_suffix('.hd5'), key='LE', complevel=9)
        self.HE.to_hdf(path_or_buf=self.data_path.with_suffix('.hd5'), key='HE', complevel=9)


class iaDBsXMLparser(XMLparser):
    """Parser of iaDBs xml files."""
    def prot_ids(self):
        """Get the number each protein id occured in the XML file.

        Returns:
            Counter: counts of id's.
        """
        return Counter(p.attrib['ID'] for p in self.root.findall('HIT/PROTEIN'))

    def proteins(self):
        """Get all protein information from the XML file.
    
        Returns:
            pd.DataFrame: Protein information.
        """
        return pd.DataFrame(p.attrib for p in self.root.findall('HIT/PROTEIN'))

    def products(self):
        """Get all products information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(p.attrib for p in self.root.findall('PRODUCT'))

    def iter_peptides(self):
        for p in self.root.iter('PEPTIDE'):
            res = p.attrib.copy()
            mods = " ".join(f"{m.attrib['NAME']}__{m.attrib['POS']}" for m in p)
            if mods:
                res['MOD'] = mods
            yield res

    def peptides(self):
        """Get all products information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(self.iter_peptides())

    def parameters(self):
        """Get iaDBs parameters.

        Returns:
            dict: Parameter-value.
        """
        return dict(p.attrib.values() for p in self.root.findall('PARAMS/PARAM'))

    def iter_query_masses(self):
        for p in self.root.iter('QUERY_MASS'):
            res = p.attrib.copy()
            i = 0
            for i, matched_mass in enumerate(p):
                res.update(matched_mass.attrib)
            if i > 0:
                raise NotImplementedError("The case of multiple MASS_MATCH per query is not coded in.")
            yield res

    def query_masses(self):
        """Get all query mass information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(self.iter_query_masses())

    def count_proteins_per_hit(self):
        """Count how many times a given number of proteins were assigned to one hit.

        Returns:
            Counter: Distribution of proteins number per hit.
        """
        return Counter(len(h) for h in self.root.iter('HIT'))

    def iter_hits(self):
        """Get all information on the hits.

        Each hit can consist of multiple proteins.
        Each protein can have several sequence matches.
        Each row of the result corresponds to such match.
        """
        for hit_id, hit in enumerate(self.root.iter('HIT')):
            for prot in hit:
                prot_attrib = {f'PROT_{k}':v for k,v in prot.attrib.items()}
                seq_matches = []
                for node in prot:
                    if node.tag == 'SEQUENCE_MATCH':
                        seq_match = node.attrib
                        seq_match['fragment_ion'] = ";".join(fii.attrib['IDS'] for fii in node.iter('FRAGMENT_ION')).replace(',','')
                        seq_matches.append(seq_match)
                    else:
                        prot_attrib[f'PROT_{node.tag}'] = node.text
                prot_attrib['HIT'] = hit_id
                for seq_att in seq_matches:
                    row = {f"SEQ_{k}":v for k,v in seq_att.items()}
                    row.update(prot_attrib)
                    yield row

    def hits(self):
        return pd.DataFrame(self.iter_hits())


    def info(self):
        """Return core information about the seach outcomes."""
        out = {}
        tag_counts = self.get_tag_counts()
        params = self.parameters()
        out['raw_file'] = params['RawFile']
        out['acquired_name'] = params['AcquiredName']
        out['sample_description'] = params['SampleDescription']
        out['queries_cnt'] = tag_counts['QUERY_MASS']
        out['hits_cnt'] = tag_counts['HIT']
        out['peptides_cnt'] = tag_counts['PEPTIDE']
        out['proteins_cnt'] = len(self.prot_ids())
        return out



def get_search_stats(iadbs_out):
    X = iaDBsXMLparser(iadbs_out)
    info = X.info()
    del X
    return info    
