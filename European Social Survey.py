# The main goal of this file is to show you that I'm able to perfom Data exploratory analysis et statistical analysis in Python. This project was initially 
# based on SAS. With this mini-project, I wanted to provide an exploratory analysis of the European Social Survey and more precisely a study of happiness and
# trust on institutions of French people. This extract investigates the level of happiness and trust based on gender of people.  I wish to complete this 
# study by providing econometric analysis of happiness. This part will come later.


#Packages loading
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# Read DataFrame
Ess_survey = pd.read_csv(".../ESS2.csv")
Ess_survey.head()

######################## Exploratory Data Analaysis

#Nationality
Ess_survey.cntry.unique()

#Filter of french people
Ess_survey_wk = Ess_survey[Ess_survey.cntry == "FR"]

#Selection of subset of colums 
col_keep = ["happy", "gndr",
"trstlgl", "trstplc", "trstplt", "trstprl", "trstprt", ]
Ess_survey_wk = Ess_survey_wk[col_keep]
Ess_survey_wk.columns

#Rename Variables
col_name = ["Bonheur", "Genre",
 "Confiance_système_légal", "Confiance_police", "Confiance_politicien",
"Confiance_parlement", "Confiance_parti_pol"]
Ess_survey_wk.columns = col_name
Ess_survey_wk.columns

#Check the presence of NaN
Ess_survey_wk.isnull().sum(axis=0) # No NaN

#Summary statistics
Ess_survey_wk.describe()

#Responses "Don't knwow" take the number 88 in the questionnary. Scales of variable are from 0 to 10
non_rep = ["Bonheur", "Confiance_système_légal",
"Confiance_police", "Confiance_politicien", "Confiance_parlement", "Confiance_parti_pol"]
for col in non_rep:
    Ess_survey_wk.drop(Ess_survey_wk[Ess_survey_wk[col] > 80].index, inplace=True)
Ess_survey_wk.describe() # absence of outliers

#Add categorical variables for "Bonheur" (happiness)
def Bonheur_group(Bonheur):
    if Bonheur <= 2:
        return "Pas heureux"
    elif Bonheur > 2 and Bonheur <= 5:
        return "Peu heureux"
    elif Bonheur >= 5 and Bonheur <= 8:
        return "Assez Heureux"
    else: return "Très Heureux"

Ess_survey_wk['Bonheur_group'] = Ess_survey_wk['Bonheur'].apply(Bonheur_group)

#Add Categorical Variable for "Genre" (Gender)
Ess_survey_wk['Genre'] = np.where(Ess_survey_wk['Genre'] == 1, "Homme", "Femme")
Ess_survey_wk.Genre.value_counts(normalize= True) #Proportion of women and men in population not respected in the sample

#Add variable "Confiance_moyenne" which is the average of trust in institution including politics
Ess_survey_wk['Confiance_moyenne'] = Ess_survey_wk[['Confiance_police', 'Confiance_parlement','Confiance_politicien',
'Confiance_parti_pol']].mean(axis=1)


######################## Statistical Analysis

### 1. Analysis of Happiness
Ess_survey_wk["Bonheur"].describe() # On average, french people are "Assez heureux".

# Ploting density
sns.distplot(Ess_survey_wk['Bonheur'], hist=False) #Distribution of "Bonheur" not normal. We observe a left asymetrie.

### 2. Happiness by gender

#Difference of average happiness
Ess_survey_wk.groupby('Genre')['Bonheur'].mean() # On average, Mens are happier than womens, but is it significant ?
Homme = Ess_survey_wk[Ess_survey_wk['Genre']== "Homme"]
Femme = Ess_survey_wk[Ess_survey_wk['Genre'] == "Femme"]
stats.ttest_ind(Homme['Bonheur'], Femme['Bonheur']) #Difference not significative following p_values. We reject the alternative hypothesis

#Bar plot
Bonheur_genre = Ess_survey_wk.groupby(['Genre', 'Bonheur_group']).size().reset_index()
Bonheur_genre = Bonheur_genre.pivot(index = 'Genre', columns = 'Bonheur_group', values = 0)
Bonheur_genre = Bonheur_genre.apply(lambda x : x*100/sum(x), axis = 1)
Bonheur_genre.plot(kind = "bar", stacked = True, figsize = (10,5), width = 0.5).legend(bbox_to_anchor=(1., 1))

### 3. Trust by gender
Ess_survey_wk.groupby('Genre')['Confiance_moyenne'].mean() #On average, mens have more confidence in institutions than women
# is it significative ?
stats.ttest_ind(Homme['Confiance_moyenne'], Femme['Confiance_moyenne']) # The mean difference is significative at 95%. 

#Bar plot
Confiance_genre = Ess_survey_wk.groupby(['Genre', 'Confiance_group']).size().reset_index()
Confiance_genre = Confiance_genre.pivot(index = 'Genre', columns = 'Confiance_group', values = 0)
Confiance_genre = Confiance_genre.apply(lambda x : x*100/sum(x), axis = 1)
Confiance_genre.plot(kind = "bar", stacked = True, figsize = (10,5), width = 0.5).legend(bbox_to_anchor=(1., 1))
