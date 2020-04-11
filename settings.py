class Settings():
	
	def __init__(self):

		self.YELP_FUSION_API_KEY = 'YSSLW8HZIPWuU_xxT1ArE0WoIYgyQdyHaZKwUWlm09fkeSI4PhpuncVAUtkkDYNnYdTJpsPF7TK0tj178RicqXfKQPydxkz-WmTk-q1qIqcQQLmD12lnfnUcwi43XnYx'
		
		## DATABASE NAMES
		self.GEO_DATABASE = 'Tags'
		self.BUSINESS_DATABASE = 'Business'

		## COLLECTION NAMES
		self.REVIEW_COLLECTION = 'geo_data'
		self.BUSINESS_COLLECTION = 'Restaurants'
		self.TOPIC_COLLECTION = 'Topics'
		self.TOPIC_VALUES_COLLECTION = 'collection_topics'

		self.model_path = '/Users/mael/mirae_kim/persproj/models/2020_03_23/lda_model_eta_01_ntopics_13.lda'
		self.dictionary_path = '/Users/mael/mirae_kim/persproj/models/2020_03_22/dictionary.dict'

