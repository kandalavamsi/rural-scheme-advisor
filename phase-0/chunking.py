def chunk_text(text,chunk_size=200, chunk_overlap=40):
    if chunk_size <=0:
        raise ValueError("chunk size must be greater than zero")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and smaller than chunk size")
    
    chunks=[]
    start=0
    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        if end >= len(text):
            break

        start += chunk_size - chunk_overlap
    return chunks

document="""
PM-KISAN is a Central Sector Scheme that provides income
support to eligible landholding farmer families.

Under the scheme, eligible farmer families receive financial
assistance subject to the applicable exclusion criteria.
The assistance is transferred directly to beneficiaries
through Direct Benefit Transfer.

Farmers can register through the official PM-KISAN portal.
They need to provide the required personal details and
land ownership records during the registration process.

Beneficiaries can check their payment status through the
official portal using the available beneficiary services.
"""
#split document into chunks
chunks=chunk_text(document,chunk_size=200, chunk_overlap=40)
# Display results
print("Total characters:", len(document))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):

    print(f"\n--- Chunk {i + 1} ---")
    print("Characters:", len(chunk))
    print(chunk)
