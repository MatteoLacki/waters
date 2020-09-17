from waters.parsers import get_search_stats, XMLparser

p = "Y:/RES/2020-092/I200725_16/I200725_16_IA_workflow.xml"
X = XMLparser(p)
del X

ss = get_search_stats(p)