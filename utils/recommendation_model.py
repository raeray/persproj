from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import Reader

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(lda_class.review_df[['city','relevant_topic', 'review_stars']], reader)

# Use the famous SVD algorithm.
algo = SVD()

# Run 5-fold cross-validation and print results.
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)