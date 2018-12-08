import xml.etree.ElementTree as ET
import pandas as pd
import os

cwd = os.getcwd()
PATH =  '/'.join(cwd.split('/')[0:-1]) + '/data/raw/'
NUM_REVIEW_THRESH = 300 
OUT_FNAME =  '/'.join(cwd.split('/')[0:-1]) + '/data/labeled_restaurant_data.csv'

# Parse & clearn labeled training data
tree = ET.parse(PATH + 'Restaurants_Train.xml')
root = tree.getroot()

labeled_reviews = []
for sentence in root.findall("sentence"):
    entry = {}
    aterms = []
    aspects = []
    if sentence.find("aspectTerms"):
        for aterm in sentence.find("aspectTerms").findall("aspectTerm"):
            aterms.append(aterm.get("term"))
    if sentence.find("aspectCategories"):
        for aspect in sentence.find("aspectCategories").findall("aspectCategory"):
            aspects.append(aspect.get("category"))
    entry["text"], entry["terms"], entry["aspects"]= sentence[0].text, aterms, aspects
    labeled_reviews.append(entry)
labeled_df = pd.DataFrame(labeled_reviews)
print("there are",len(labeled_reviews),"reviews in this training set")

# Save annotated reviews
labeled_df.to_csv(OUT_FNAME, encoding='utf-8')
