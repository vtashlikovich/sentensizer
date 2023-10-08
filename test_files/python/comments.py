import json, os
import spacy
from spacy import displacy

text = ''' this text
sdfef '''

"""
....
"""

nlp = spacy.load('en_core_web_sm')

# nlp = nlp.from_disk('vocabby')
# # bytes_data = nlp.to_bytes()
# # 

# # with open('myvocab.voc', 'wb') as file:
# #     file.write(bytes_data)

doc = nlp('Application should output this information to console')
# displacy.render(doc, style='ent', jupyter=True)
html = displacy.render(doc, style="dep")
# displacy.serve(doc, style="dep")

# output_path = Path(os.path.join("./", "sentence.svg"))
open('test2.svg', 'w', encoding="utf-8").write(html)

# id = nlp.vocab[word].orth

# print(type(id))

# print(nlp.vocab[id])
# print(nlp.vocab[id].text)
# print(nlp.vocab[id].orth)
# print(nlp.vocab[id].norm)