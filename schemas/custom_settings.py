from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from global_constants import StableModels
from . import Base, str_128, str_256, str_8, str_2048, str_16
from .custom_columns import intpk

__all__ = (
    "CustomSettings",
)


class CustomSettings(Base):
    __tablename__ = "users_customsettings"

    id: Mapped[intpk]
    name: Mapped[str_128] = mapped_column(default="Какие-то настройки")
    model_id: Mapped[str_256] = mapped_column(
        default=StableModels.STABLE_DIFFUSION_3
    )
    seed: Mapped[Optional[str_128]] = mapped_column(default="-1")
    num_inference_steps: Mapped[Optional[str_8]] = mapped_column(default="20")
    guidance_scale: Mapped[int] = mapped_column(default=7)
    embeddings_model: Mapped[Optional[str_256]]
    negative_prompt: Mapped[Optional[str_2048]]
    positive_prompt: Mapped[Optional[str_2048]]
    lora_model: Mapped[Optional[str_256]]
    lora_strength: Mapped[Optional[str_128]]
    sampling_method: Mapped[Optional[str_256]]
    algorithm_type: Mapped[Optional[str_256]]
    scheduler: Mapped[Optional[str_256]]
    vary_num_inference_steps: Mapped[Optional[str_16]]
    vary_guidance_scale: Mapped[Optional[float]]
    vary_strength: Mapped[Optional[float]]
    controlnet_model: Mapped[Optional[str_256]]
    controlnet_type: Mapped[Optional[str_256]]
    controlnet_conditioning_scale: Mapped[Optional[float]]
    enhance_style: Mapped[Optional[str_256]]

    users: Mapped[list["User"]] = relationship(back_populates="custom_settings")
