# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_analyzer.ipynb.

# %% auto 0
__all__ = ['Analyzer']

# %% ../nbs/01_analyzer.ipynb 3
import pandas as pd
from unidecode import unidecode
import regex as re
from .Loader import Loader 
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt



# %% ../nbs/01_analyzer.ipynb 4
class Analyzer:
    def __init__(self,
                 loader:Loader,
                 ):
        """Constructor of the Analyzer class"""
        if loader.processed_bool == False:
            self.methods_available = False
        else:
            self.methods_available = True
        self.loader = loader

    def moral_words_count(self, message_col: str) -> pd.DataFrame:
        """Returns a dataframe with the count of virtue and vice words in each message in the message_col column"""
        if not self.methods_available:
            print('You need to process the data first')
            return None
        
        vice_d = self.loader.vice_dict
        virtue_d = self.loader.virtue_dict
        df = self.loader.processed

        vice = set(vice_d.keys())
        virtue = set(virtue_d.keys())

        def count_words(text, set_of_words):
            words_in_text = text.lower().split()
            word_count = 0
            word_list = []
            for word in words_in_text:
                if word in set_of_words:
                    word_count += 1
                    word_list.append(word)
            return word_count, word_list

        # Agregar las columnas 'Vice words' y 'Virtue words' utilizando apply y la función count_words
        df[['Vice words count', 'Vice words']] = df[message_col].apply(lambda x: pd.Series(count_words(str(x), vice)))
        df[['Virtue words count', 'Virtue words']] = df[message_col].apply(lambda x: pd.Series(count_words(str(x), virtue)))

        df.sort_values(by=['Vice words count', 'Virtue words count'], ascending=False)

        df['Total words'] = df[message_col].apply(lambda x: len(x.split()))

        df = df[df['Total words'] != 0] # Remove rows with empty messages
        df = df[df['Total words'] > 3] # Remove rows with less than 3 words 

        df['Sum vice and virtue'] = df['Vice words count'] + df['Virtue words count']

        return df
    
    def get_moral_df(self,
                     df:pd.DataFrame): #DataFrame with the moral words count
        """Returns a dataframe with moral words in the message, and gives a series of ratios."""

        df_moral = df[(df ['Vice words count'] > 0) | (df['Virtue words count'] > 0)]
        df_moral['VVRate'] = df.apply(lambda row: (row['Virtue words count'] + row['Vice words count']) / row['Total words'], axis=1)
        df_moral['Vice Rate'] = df.apply(lambda row: row['Vice words count'] / row['Total words'], axis=1)
        df_moral['Virtue Rate'] = df.apply(lambda row: row['Virtue words count'] / row['Total words'], axis=1)

        df_moral['Category'] = df_moral.apply(lambda row: 'Vice' if row['Vice Rate'] > row['Virtue Rate'] else 'Virtue', axis=1)
        df_moral['Original Message'] = self.loader.original['Message'].loc[self.loader.original.index]

        df_moral = df_moral.round({'VVRate': 2, 'Vice Rate': 2, 'Virtue Rate': 2})
        df_moral = df_moral.sort_values(by=['VVRate'], ascending=False)
    
        return df_moral
    
    def moral_words_wc(self,
                       message_col:str, #Column with the messages
                       media_names:str = None, #Column with media names
                        media_list:list = None): 

        """Creates a wordcloud with the virtue and vice words in the message_col column"""
        if self.methods_available == False:
            print('You need to process the data first')
            return None
        df = self.loader.processed
        stop_words_es = set(stopwords.words('spanish'))
        morales = set()
        morales.update(self.loader.vice_dict.keys())
        morales.update(self.loader.virtue_dict.keys())

        if media_list:
            page_names = media_list
        else:   
            page_names = df[media_names].unique()


        for name in page_names:
            page_df = df[df[media_names] == name]
            
            # Remove rows with empty messages
            page_df = page_df[page_df[media_names].apply(lambda x: isinstance(x, str))]
            
            # Tokenize the messages and remove stop words
            messages = ' '.join([word for sentence in page_df[message_col] for word in sentence.split() if word.lower() not in stop_words_es])
            
            # Filter only the words that are in the moral words set
            moral_words = ' '.join([word for word in messages.split() if word.lower() in morales])

            # Create wordclouds for general words and moral words
            wordcloud_general = WordCloud(width=800, height=400).generate(messages)
            wordcloud_morales = WordCloud(width=800, height=400).generate(moral_words)

            # Show wordcloud for general words
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud_general, interpolation='bilinear')
            plt.title(f'Most Common Words in {name}')
            plt.axis("off")
            plt.show()

            # Show wordcloud for moral words
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud_morales, interpolation='bilinear')
            plt.title(f'Most Common Moral Words in {name}')
            plt.axis("off")
            plt.show()

