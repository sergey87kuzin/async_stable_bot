class StableMessageTypeChoices:
    FIRST = "first"
    U = "u"
    UPSCALED = "upscaled"
    ZOOM = "zoom_out"
    VARY = "vary"
    DOUBLE = "double"

    CHOICES = (
        (FIRST, "Первоначальная генерация"),
        (U, "Одно из 4 U-сообщений"),
        (UPSCALED, "Увеличенное изображение"),
        (ZOOM, "Отдалена"),
        (VARY, "Изменена"),
        (DOUBLE, "Двойная отправка")
    )


class StableModels:
    JUGGERNAUT = "juggernaut-xl"
    DELIBERATE = "deliberate-v3"
    SDXL = "sdxl"
    STABLE_DIFFUSION_3 = "stable-diffusion-3-medium"

    CHOICES = (
        (JUGGERNAUT, "Джаггернаут"),
        (DELIBERATE, "Делиберейт"),
        (SDXL, "sdxl"),
        (STABLE_DIFFUSION_3, "Стэйбл 3")
    )
