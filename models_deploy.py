import sagemaker as sage
from sagemaker import get_execution_role
from sagemaker import ModelPackage

# Let's first create the configuration for each of the models that we are going use.

SUMMARIZER_MODEL_CONFIG = {
    'name': 'summarizer',
    'content_type':'text/plain',
    'instance_type': 'ml.m4.xlarge',
    'arn': 'arn:aws:sagemaker:us-east-1:865070037744:model-package/marketplace-text-summarizer-e316c0bc7da2305368d5493465af0802'
}
EXPERT_TICKETS_MODEL_CONFIG = {
    'name': 'expert-tickets',
    'content_type':'text/csv',
    'instance_type': 'ml.m5.xlarge',
    'arn': 'arn:aws:sagemaker:us-east-1:865070037744:model-package/marketplace-expert-b3bae5926e152cd3c0e2e783cc50f837'
}
ADDRESS_MODEL_CONFIG = {
    'name': 'address-extract',
    'content_type':'text/plain',
    'instance_type': 'ml.m4.xlarge',
    'arn': 'arn:aws:sagemaker:us-east-1:865070037744:model-package/address-extraction-update-copy-2842b75335671181216be9b46aec2af6'
}
WIREFRAME_CONFIG = {
    'name': 'wireframe',
    'content_type':'image/jpeg',
    'instance_type': 'ml.m5.xlarge',
    'arn': 'arn:aws:sagemaker:us-east-1:865070037744:model-package/wireframetocode-01-30-517aa954c6cea79683836daa20955a5c'
}

PASSPORT_CONFIG = {
    'name': 'passport',
    'content_type':'image/jpeg',
    'instance_type': 'ml.m4.xlarge',
    'arn': 'arn:aws:sagemaker:us-east-1:865070037744:model-package/gtriip-passport-ic-m5-7-62ae9e20b9779c8073d3393d0d93b5fe'
}


# Here we create a generic class called **Model** to create a model based on its configuration.
class Model():
    def __init__(self, config):
        self.name = config['name']
        self.instance_type =  config['instance_type']
        self.content_type =  config['content_type']
        self.model_package_arn =  config['arn']
    
    def _predict_wrapper(self, endpoint, session):
        return sage.RealTimePredictor(endpoint, session, self.content_type)
    
    def remove_endpoint(self):
        self.predictor.delete_endpoint(delete_endpoint_config=True)

    def create_and_deploy(self, role, session):
        #create a deployable model from the model package.
        self.model_package = ModelPackage(role=role,
                            model_package_arn=self.model_package_arn,
                            sagemaker_session=session,
                            predictor_cls=self._predict_wrapper)

        #Deploy the model
        self.predictor = self.model_package.deploy(1, self.instance_type, endpoint_name=self.name)
        return self.predictor


# ### Deploy passport model
model_passport = Model(PASSPORT_CONFIG)
model_passport.create_and_deploy(role, session)

# ### Deploy wireframe model
model_wireframe = Model(WIREFRAME_CONFIG)
model_wireframe.create_and_deploy(role, session)

# ### Deploy summarizer model
model_summarizer = Model(SUMMARIZER_MODEL_CONFIG)
model_summarizer.create_and_deploy(role, session)

# ### Deploy address extractor model
model_address = Model(ADDRESS_MODEL_CONFIG)
model_address.create_and_deploy(role, session)

# ### Deploy expert ticket suggestion model
model_experts = Model(EXPERT_TICKETS_MODEL_CONFIG)
model_experts.create_and_deploy(role, session)
