import praw
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")

def what_stock_to_buy(limit_of_posts = 15, time_lookback = "week", query_sort = "top" ## or hot?
                , query = ['what stock should I buy'], sub = "wallstreetbets"):
    all_stocks = pd.read_csv('list_of_stocks.csv')
    all_stocks = all_stocks[all_stocks['Country'] == 'United States'].reset_index(drop=True)
    all_stocks = all_stocks[['Symbol', 'Name']]

    secret='iFYDcYUNWwgFPAEwk6_vmA3ZQ2WIbQ'
    client_id='uCLonTkFBuYPaFa_1cRZ3Q'
    user_agent='Love Letters From Macao'
    username='Existing_Dog5489'
    password='kabar bahy'

    # Read-only instance
    reddit_read_only = praw.Reddit(client_id=client_id,         # your client id
                                client_secret=secret,      # your client secret
                                user_agent=user_agent)        # your user agent
    

    subreddit = reddit_read_only.subreddit(sub)

    ## put here main stocks

    for item in query:
        post_dict = {
            "title" : [],   #title of the post
        # "score" : [],   # score of the post
        # "id" : [],      # unique id of the post
        # "url" : [],     #url of the post
        # "comms_num": [],   #the number of comments on the post
        # "created" : [],  #timestamp of the post
            "body" : []         # the descriptionof post
        }
        comments_dict = {
        # "comment_id" : [],      #unique comm id
        # "comment_parent_id" : [],   # comment parent id
            "comment_body" : [],   # text in comment
        # "comment_link_id" : []  #link to the comment
        }
        for submission in (subreddit.search(query, sort = query_sort, time_filter=time_lookback, limit = limit_of_posts)):
            post_dict["title"].append(submission.title)
        # post_dict["score"].append(submission.score)
        # post_dict["id"].append(submission.id)
        # post_dict["url"].append(submission.url)
        # post_dict["comms_num"].append(submission.num_comments)
        # post_dict["created"].append(submission.created)
            post_dict["body"].append(submission.selftext)
            
            ##### Acessing comments on the post
            submission.comments.replace_more(limit = 10)
            for comment in submission.comments.list():
    #            comments_dict["comment_id"].append(comment.id)
    #            comments_dict["comment_parent_id"].append(comment.parent_id)
                comments_dict["comment_body"].append(comment.body)
    #            comments_dict["comment_link_id"].append(comment.link_id)
        
        post_comments = pd.DataFrame(comments_dict)


    BLACKLIST = ['ev', 'covid', 'etf', 'nyse', 'sec', 'spac', 'fda', 'treasury', 'eod', 'fed', 'wsb', ]

    def get_orgs(text):
        doc = nlp(text)
        org_list = []
        for entity in doc.ents:
            # here we modify the original code to check that entity text is not equal to one of our 'blacklisted' organizations
            # (we also add .lower() to lowercase the text, this allows us to match both 'nyse' and 'NYSE' with just 'nyse')
            if entity.label_ == 'ORG' and entity.text.lower() not in BLACKLIST:
                org_list.append(entity.text.lower())
        # if organization is identified more than once it will appear multiple times in list
        # we use set() to remove duplicates then convert back to list
        org_list = list(set(org_list))
        return org_list

    post_comments['organizations'] = post_comments['comment_body'].apply(get_orgs)

    # merge organizations column into one big list
    orgs = post_comments['organizations'].to_list()
    orgs = [org for sublist in orgs for org in sublist]

    from collections import Counter
    # create dictionary of organization mention frequency
    org_freq = Counter(orgs)
    most_common = org_freq.most_common(100)

    for item in most_common:
        if len(all_stocks[all_stocks['Symbol'] == item[0].upper()]) == 0:
            continue
        else:
            final_ticker = item[0].upper()
            break
    return final_ticker

