
# for child in root:
#     print(child.tag, child.attrib)


# # on Linux, parsing these xml files is super fast.
# tags = set({})
# for child in root:
#     tags.add(child.tag)

# for t in tags:
#     w = root.find(t)
#     print(w.tag)
#     pprint(w.attrib)
#     print()


# def get_node(n):
#     if n:
#         yield n.tag, n.attrib
#         for m in n:
#             yield from get_node(m)


# # get all existing tags
# tags = set({})
# for tag, attrib in get_node(root):
#     tags.add(tag)


# prot = root.find('.//PROTEIN[@ID="2104"]')
# prot.attrib
# for k in prot:
#     print(k)

# SM = prot.find('SEQUENCE_MATCH')
# SM.attrib
# FI = SM.find('FRAGMENT_ION')


# def test_pet_matches_correct(root):
#     """Testing if peptide matches are as many as reported in the info on peptide."""
#     for prot in root.iter('PROTEIN'):
#         pep_matches = int(prot.attrib['FRAG_MATCHES'])
#         m = 0
#         for SM in prot.findall('SEQUENCE_MATCH'):
#             for FI in SM:
#                 g = FI.attrib['IDS'].split(', ')
#                 m += len(g)
#         assert pep_matches == m
# # test_pet_matches_correct(root)





# list(root.iter('SEQUENCE_MATCH'))
# # Good, so the 818 should match the proteins hits?


# len(prot.findall('SEQUENCE_MATCH'))