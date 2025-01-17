import abc

from ray.rllib.core.rl_module import RLModule
from ray.rllib.core.rl_module.apis.value_function_api import ValueFunctionAPI
from ray.rllib.utils.annotations import override
from ray.util.annotations import DeveloperAPI


@DeveloperAPI(stability="alpha")
class MARWILRLModule(RLModule, ValueFunctionAPI, abc.ABC):
    @override(RLModule)
    def setup(self):
        # Build models from catalog
        self.encoder = self.catalog.build_actor_critic_encoder(framework=self.framework)
        self.pi = self.catalog.build_pi_head(framework=self.framework)

        # Build the value head.
        self.vf = self.catalog.build_vf_head(framework=self.framework)

    @override(RLModule)
    def get_initial_state(self) -> dict:
        if hasattr(self.encoder, "get_initial_state"):
            return self.encoder.get_initial_state()
        else:
            return {}
