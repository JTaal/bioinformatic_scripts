from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Combine the provided word lists into one
combined_words = '''
Cancer, Genomics, cfDNA, Cancer immunotherapy, Cancer classification, Immuno-oncology, Immunology 
Immunotherapy, Antibiotic resistance, Artificial intelligence, Machine learning 
Chromosome conformation, Transcription factors, Computational biology, Prediction, Computer vision, Rare disease genomics,
DNA, Genomics, Imaging, Whole-genome sequencing, Nanopore sequencing, Epigenetics, RNA-seq, Single-cell sequencing, Hematology, DNA methylation, TCR sequencing, BCR sequencing, Transcriptomics, minimal change disease
'''

# Define the size of the image
width, height = 800, 400

# Generate a word cloud without any mask
combined_wordcloud = WordCloud(background_color='black', width=width, height=height).generate(combined_words)

# Display the combined word cloud
plt.figure(figsize=(10, 5))
plt.imshow(combined_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
