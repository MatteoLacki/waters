from collections import Counter
from io import StringIO
import numpy as np
import pandas as pd
import xml.etree.cElementTree as ET


class XMLparser(object):
    """General xml parsing capabilities."""
    def __init__(self, data_path):
        self.tree = ET.parse(data_path)
        self.root = self.tree.getroot()

    def get_tag_counts(self):
        """Count the top level tags.

        Returns:
            Counter: count of each first-level tag.
        """
        return Counter(c.tag for c in self.root)

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
                             **kwds)

    def write(self, path):
        """Write back the xml file."""
        path = str(path)
        self.tree.write(path)


#TODO: it might make sense to change row.astype(str) to something that uses the proper numbers of digits.
def df2text2(df):
    return "\n      "+"\n      ".join(" ".join(row.astype(str)) for row in df.values)


def df2text3(df):
    x = df.iloc[:,0].astype(str).str.cat(df.iloc[:,1:].astype(str), sep=" ")
    return "\n      "+"\n      ".join(x)


def df2text(df, col2format={}, copy=True):
    if copy:
        df = df.copy()
    cols = df.columns
    for col, formatter in col2format.items():
        df.loc[:,col] = df.loc[:,col].apply(lambda x: formatter % x)
    cols_simple2str = [c for c in cols if c not in col2format]
    df.loc[:,cols_simple2str] = df[cols_simple2str].astype(np.str)
    df = df.iloc[:,0].astype(str).str.cat(df.iloc[:,1:].astype(str), sep=" ")
    return "\n      "+"\n      ".join(df)



class Pep3Dparser(XMLparser):
    def LE(self):
        """Get low energy ions, or the unfragmented spectra."""
        elem = next(self.root.iter('DATA'))
        column_names = [f.attrib['NAME'] for f in self.root.findall("FORMAT[@FRAGMENTATION_LEVEL='0']/*")]
        return self.element2df(elem, column_names)

    def HE(self):
        """Get high energy ions, or the spectra of fragments."""
        elem = next(self.root.iter('HE_DATA'))
        column_names = [f.attrib['NAME'] for f in self.root.findall("FORMAT[@FRAGMENTATION_LEVEL='1']/*")]
        return self.element2df(elem, column_names)

    def update_data(self, element, df, df_foo=df2text):
        """Update the text data in the column."""
        element.text = df_foo(df)



class Apex3Dparser(XMLparser):
    def LE(self):
        """Get low energy ions, or the unfragmented spectra."""
        elem = next(self.root.iter('LE'))
        column_names = [f.attrib['NAME'] for f in self.root.findall('DATAFORMAT/FIELD')]
        return self.element2df(elem, column_names)

    def HE(self):
        """Get high energy ions, or the spectra of fragments."""
        elem = next(self.root.iter('HE'))
        column_names = [f.attrib['NAME'] for f in self.root.findall('DATAFORMAT/FIELD')]
        return self.element2df(elem, column_names)



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

    def parameters(self):
        """Get iaDBs parameters.

        Returns:
            dict: Parameter-value.
        """
        return dict(p.attrib.values() for p in self.root.findall('PARAMS/PARAM'))

    def query_masses(self):
        """Get all query mass information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(p.attrib for p in self.root.findall('QUERY_MASS'))

    def count_proteins_per_hit(self):
        """Count how many times a given number of proteins were assigned to one hit.

        Returns:
            Counter: Distribution of proteins number per hit.
        """
        return Counter(len(h) for h in self.root.iter('HIT'))

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
    return iaDBsXMLparser(iadbs_out).info()    
