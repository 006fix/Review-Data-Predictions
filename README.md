# Review-Data-Predictions
Collaborative project to buld ML skills and try out approaches via determining review year of IMBD reviews

The discussion ...

I've been thinking about an example that is based on text analysis as it's new to me [Greg] and I think helps suss out what can and cannot be done in ML Vs. classic stats.  And, what has a good sized data set plus some experience of others playing with it so there are good sources for otherwise tedious data wrangling.

One of the classic ones is the IMDB review corpus, though there a million examples of 'predict if the review is positive or negative' so I was musing on something different.  One that came to mind is predicting the year of the review, as I have a hunch that the language form and words used will change over time.  The data set below might be a good starting point as it has the full reviews along with the date of review.

https://www.kaggle.com/ebiswas/imdb-review-dataset

It might be that there is a solid hint in years written in the data set, so I was thinking of a pre-process step that bulk replaced any years or strings in the format of a date with QQQQQ or similar (practically, it might just be replace with a dictionary token of 'this was a year').

What do you think?  May not be the best ever but it is grounded in real data and would allow e.g. use of pre-canned word relationship models as well as n-gram bag of words type stuff.  And there might be a derivative version that estimates time between film release and review.
