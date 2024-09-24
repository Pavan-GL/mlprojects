import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransaformationConfig:
    preprocessor_obj_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransaformation:
    def __init__(self):
        self.data_transformation_config=DataTransaformationConfig()

    def get_data_transformer(self):
        '''
        This function is responsible for data transformation
        
        
        '''
        try:
            numerical_features = ["reading_score","writing_score"]
            categorical_features = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            num_pipeline = Pipeline(steps=[("imputer",SimpleImputer(strategy="median")),
                                           ("scalar",StandardScaler())])
            
            logging.info("numerical pipline is completed")
            cat_pipeline = Pipeline(steps=[("imputer",SimpleImputer(strategy="most_frequent")),
                                           ("one_hot_encoder",OneHotEncoder()),
                                           ("scalar",StandardScaler(with_mean=False))])
            
            logging.info("categorical encoding is completed")
            preprocessor = ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_features),
                ("cat_pipeline",cat_pipeline,categorical_features)
            ])
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("read train and test data completed")
            logging.info("obtaining preprocessing object")
            preprocessor_obj = self.get_data_transformer()
            target_column_name = "math_score"
            numerical_features = ["reading_score","writing_score"]
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
    
            logging.info(f"train,{input_feature_train_df.shape}")

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            logging.info(f"test,{input_feature_test_df.shape}")
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataset")
            input_feature_train_array = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_array,np.array(target_feature_test_df)]

            logging.info("saved the preprocessing objects")
            save_object(file_path = self.data_transformation_config.preprocessor_obj_path,
                        obj = preprocessor_obj)
            return (train_arr,test_arr,
                    self.data_transformation_config.preprocessor_obj_path)


        except Exception as e:
            raise CustomException(e,sys)
