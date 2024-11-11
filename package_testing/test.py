from core.feluda import Feluda
from sklearn.metrics.pairwise import cosine_similarity
from  core.models.media_factory import ImageFactory

feluda = Feluda('config.yaml')
feluda.setup()

operator = feluda.operators.get()["image_vec_rep_resnet"]

embeddings = []

for i in range(6):
    file = ImageFactory.make_from_file_on_disk("images/image-"+str(i)+".png")
    embedding = operator.run(file)
    embeddings.append(embedding)

cos_sim = cosine_similarity(embeddings)
print(cos_sim)

sim_sorted_doc_idx = cos_sim.argsort()
# print(sim_sorted_doc_idx.shape)
print(sim_sorted_doc_idx[0][len(embeddings)-1])
match_ix = sim_sorted_doc_idx[0][len(embeddings)-2]

print("closest matches are image-0.png and image-"+str(match_ix)+".png")
