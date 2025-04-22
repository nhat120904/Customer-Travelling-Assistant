import os
 
from dataclasses import dataclass, field
from dotenv import load_dotenv, find_dotenv
 
from utils.utils import load_yaml
from utils.logging import setup_logging

# Determine the absolute path to the configs directory
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
 
# Paths to configuration files
CONFIG_YAML_PATH = os.path.join(CONFIG_DIR, "config.yaml")
LLM_YAML_PATH = os.path.join(CONFIG_DIR, "llm.yaml")
LOGGER_INI_PATH = os.path.join(CONFIG_DIR, "logger.ini")
DATABASE_YAML_PATH = os.path.join(CONFIG_DIR, "database.yaml")
VECTORDB_YAML_PATH = os.path.join(CONFIG_DIR, "vectordb.yaml")
API_YAML_PATH = os.path.join(CONFIG_DIR, "api.yaml")
 
# Load YAML configurations
llm_config = load_yaml(LLM_YAML_PATH)
db_config = load_yaml(DATABASE_YAML_PATH)
vectordb_config = load_yaml(VECTORDB_YAML_PATH)
api_config = load_yaml(API_YAML_PATH)
config = load_yaml(CONFIG_YAML_PATH)
 
# Setup logging directories
log_dir = config["log_dir"]
 
logger = setup_logging(
    log_dir=log_dir,
    log_ini_path=LOGGER_INI_PATH,
)
 
@dataclass
class LLMConfig:
    model_type: str = llm_config["model"]["type"]
    model_name: str = llm_config["model"]["name"]
   
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    azure_openai_key: str = os.getenv("AZURE_OPENAI_KEY")
    azure_openai_version: str = os.getenv("AZURE_OPENAI_VERSION")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
   
    def __post_init__(self):
        if self.model_type.lower() == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY must be set for OpenAI model type.")
        elif self.model_type.lower() == "azure_openai":
            missing_fields = []
            if not self.azure_openai_key:
                missing_fields.append("AZURE_OPENAI_KEY")
            if not self.azure_openai_version:
                missing_fields.append("AZURE_OPENAI_VERSION")
            if not self.azure_openai_deployment:
                missing_fields.append("AZURE_OPENAI_DEPLOYMENT")
            if not self.azure_openai_endpoint:
                missing_fields.append("AZURE_OPENAI_ENDPOINT")
           
            if missing_fields:
                raise ValueError(f"The following Azure OpenAI configuration(s) must be set for Azure OpenAI model type: {', '.join(missing_fields)}")
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")

__all__ = [
    "LLMConfig",
    "get_logger",
    "config",
    "llm_config",
    "logger",
]