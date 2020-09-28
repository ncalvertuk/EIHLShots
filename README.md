# EIHLShots
Python scripts to analyse EIHL shot data from the 2019-20 season. Data analysis is performed on the shot data to look at the trends in shooting distance, angle, situation, etc. I built a shot quality model, prediciting the probability that a shot results in a goal or not using a Logistic Regression model and a Random Forest.

The accompanying blogpost can be found here: https://www.ncalvert.uk/posts/eihlshots/

The contained files are:

shotplots.py - Some functions to perform plotting, I moved these to a separate .py file to save code repitition in the Jupyter Notebooks
GetPenaltiesAndGoals.ipynb - This Jupyter notebook scrapes the gamesheet data from the EIHL website (www.eliteleague.co.uk) to get the penalty and goal data. You have to run this prior to performing the analysis.
ShotAnalysis.ipynb - This notebook performs the Data Analysis on the shot data.
