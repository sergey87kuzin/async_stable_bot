from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from global_constants import StableModels
from schemas import Base, str_256, str_128, str_8, str_2048, str_16

__all__ = ['StableSettings']

from schemas.custom_columns import intpk


class StableSettings(Base):
    __tablename__ = 'stable_messages_stablesettings'

    id: Mapped[intpk]
    model_id: Mapped[Optional[str_256]] = mapped_column(default=StableModels.STABLE_DIFFUSION_3)
    seed: Mapped[Optional[str_128]] = mapped_column(default="-1")
    num_inference_steps: Mapped[Optional[str_8]] = mapped_column(default="21")
    guidance_scale: Mapped[Optional[int]]
    embeddings_model: Mapped[Optional[str_256]]
    negative_prompt: Mapped[Optional[str_2048]]
    positive_prompt: Mapped[Optional[str_2048]]
    algorithm_type: Mapped[Optional[str_256]]
    lora_model: Mapped[Optional[str_256]]
    lora_strength: Mapped[Optional[str_128]]
    sampling_method: Mapped[Optional[str_256]]
    scheduler: Mapped[Optional[str_256]]
    vary_guidance_scale: Mapped[Optional[float]]
    vary_num_inference_steps: Mapped[Optional[str_16]]
    vary_strength: Mapped[Optional[float]]
    controlnet_model: Mapped[Optional[str_256]]
    controlnet_type: Mapped[Optional[str_256]]
    controlnet_conditioning_scale: Mapped[Optional[float]]
