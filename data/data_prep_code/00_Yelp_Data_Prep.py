
# coding: utf-8

# In[17]:


import json
import pandas as pd
import os

def read_from_json(fpath):
    print ("Reading data from %s ..." % fpath)
    with open(fpath, 'r') as f:
        df = pd.DataFrame([json.loads(r) for r in f.readlines()])

    print ("Done.")
    return df

cwd = os.getcwd()
PATH =  '/'.join(cwd.split('/')[0:-1]) + '/data/raw/'
NUM_REVIEW_THRESH = 300 
OUT_FNAME =  '/'.join(cwd.split('/')[0:-1]) + '/data/yelp_processed.csv'

# PROCESS BUSINESS DATA FRAME
# read in the raw data
business_path = PATH + 'yelp_academic_dataset_business.json'
business_df = read_from_json(business_path)

# only keep necessary columns
keeps = ['name', 'city','attributes', 'stars', 'categories', 'review_count', 'business_id']
business_df = business_df[keeps]

# keep only with many reviews 
business_df = business_df.loc[(business_df['review_count'] > NUM_REVIEW_THRESH)]

# rename a column
business_df.rename(index=str, inplace=True, columns={'stars': 'business_overall_stars', 'name': 'business_name'})

business_df.head()


# In[18]:


# PROCESS REVIEWS DATA FRAME
user_path = PATH + 'yelp_academic_dataset_user.json'
user_df = read_from_json(user_path)

keeps = ['user_id', 'average_stars', 'name']
user_df = user_df[keeps]

user_df.rename(index=str, inplace=True, columns={'average_stars':'user_avg_stars', 'name': 'user_name'})
user_df.head()


# In[ ]:


# PROCESS REVIEWS DATA FRAME 
review_path = PATH + 'yelp_academic_dataset_review.json'
review_df = read_from_json(review_path)

# only keep necessary columns
keeps = ['business_id', 'review_id', 'stars', 'text', 'user_id']
review_df = review_df[keeps]

# rename stars column
review_df.rename(index=str, inplace=True, columns={'stars':'review_stars'})
review_df.head()                                   


# In[ ]:


# MERGE THE DATA FRAMES 
# MERGE review and business dfs
review_business = review_df.merge(business_df, on='business_id', how='inner')

# merge in the user info
review_business_user = review_business.merge(user_df, on='user_id', how='left')

# Write to csv
review_business_user.to_csv(OUT_FNAME, encoding='utf-8')

