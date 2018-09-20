#import logging
from gym.envs.registration import register

#logger = logging.getLogger(__name__)

register(
    id='MinGenericEnv-v1',
    entry_point='min_generic_env.envs:MinGenericEnv',
)

