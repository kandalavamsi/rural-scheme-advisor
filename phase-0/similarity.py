import numpy as np 

def cosine_similarity(vector_a, vector_b):
    dot_product=np.dot(vector_a,vector_b)
    magnitude_a=np.linalg.norm(vector_a)
    magnitude_b=np.linalg.norm(vector_b)

    similarity=dot_product/(magnitude_a*magnitude_b)
    return similarity

vector_a=np.array([1,0])
vector_b=np.array([-1,0])
result=cosine_similarity(vector_a,vector_b)
print("vector_a:", vector_a)
print("vector_b:", vector_b)
print("Cosine Similarity:", result)

