
import pandas as pd
import os

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe
from eva_config import Config
import json
from autolabel import LabelingAgent, AutolabelDataset

class AutoLabeller(AbstractFunction):

    @setup(cacheable=False, function_type="FeatureExtraction", batchable=False)
    def setup(self):
        cred_config = Config()
        os.environ['OPENAI_API_KEY'] = cred_config.get_open_ai_key()

    @property
    def name(self) -> str:
        return "AutoLabeller"

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["data"],
                column_types=[NdArrayType.STR],
                column_shapes=[(None, 3)],
            ),

        ],
        output_signatures=[
            PandasDataframe(
                columns=["response"],
                column_types=[NdArrayType.STR],
                column_shapes=[(None,)],
            )
        ],
    )
    def forward(self, df: pd.DataFrame) -> pd.DataFrame:
        with open("config.json", 'r') as file:
            # Load the JSON data into a Python dictionary
            config = json.load(file)

        agent = LabelingAgent(config)
        ds = AutolabelDataset('data/test.csv', config = config)
        print(agent.plan(ds))

        ds = agent.run(ds, max_items=20)

        new_df = ds.df
        new_df = new_df[['example', 'label']]
        new_df.to_csv("data/labeled.csv")

        response  = "created the labelled file in data/labeled.csv"
        df_dict = {"response": [response]}
        
        ans_df = pd.DataFrame(df_dict)
        return ans_df

        



        return df