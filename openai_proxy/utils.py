import os, litellm
import yaml
import dotenv
from typing import Optional
dotenv.load_dotenv() # load env variables

def set_callbacks():
    ## LOGGING
    if len(os.getenv("SET_VERBOSE", "")) > 0: 
        if os.getenv("SET_VERBOSE") == "True": 
            litellm.set_verbose = True
            print("\033[92mLiteLLM: Switched on verbose logging\033[0m")
        else: 
            litellm.set_verbose = False

    ### LANGFUSE
    if (len(os.getenv("LANGFUSE_PUBLIC_KEY", "")) > 0 and len(os.getenv("LANGFUSE_SECRET_KEY", ""))) > 0 or len(os.getenv("LANGFUSE_HOST", "")) > 0:
        litellm.success_callback = ["langfuse"] 
        print("\033[92mLiteLLM: Switched on Langfuse feature\033[0m")
    
    ## CACHING 
    ### REDIS
    if len(os.getenv("REDIS_HOST", "")) >  0 and len(os.getenv("REDIS_PORT", "")) > 0 and len(os.getenv("REDIS_PASSWORD", "")) > 0: 
        from litellm.caching import Cache
        litellm.cache = Cache(type="redis", host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PASSWORD"))
        print("\033[92mLiteLLM: Switched on Redis caching\033[0m")



def load_router_config(router: Optional[litellm.Router]):
    config = {}
    config_file = 'config.yaml'

    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    else:
        print(f"Config file '{config_file}' not found.")

    ## MODEL LIST
    model_list = config.get('model_list', None)
    if model_list: 
        router = litellm.Router(model_list=model_list)
    
    ## ENVIRONMENT VARIABLES
    environment_variables = config.get('environment_variables', None)
    if environment_variables: 
        for key, value in environment_variables.items(): 
            os.environ[key] = value

    return router
